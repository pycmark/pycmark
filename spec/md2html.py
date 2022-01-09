#!/usr/bin/env python3

import html
import sys

from docutils import nodes
from docutils.core import publish_string
from docutils.readers import standalone
from docutils.transforms.misc import Transitions
from docutils.writers.html5_polyglot import Writer, HTMLTranslator

from pycmark import Parser
from pycmark.transforms import LinebreakFilter, SectionTreeConstructor


class HTMLWriter(Writer):
    def __init__(self):
        Writer.__init__(self)
        self.translator_class = SmartHTMLTranslator

    def apply_template(self):
        subs = self.interpolation_dict()
        return subs.get('body')


class SmartHTMLTranslator(HTMLTranslator):
    special_characters = {
        ord('&'): '&amp;',
        ord('<'): '&lt;',
        ord('"'): '&quot;',
        ord('>'): '&gt;',
    }

    def __init__(self, document):
        super().__init__(document)
        self.initial_header_level = 1

    def depart_Text(self, node):
        pos = node.parent.index(node)
        if isinstance(node.parent, nodes.list_item) and len(node.parent) > pos + 1:
            self.body.append('\n')

    def depart_paragraph(self, node):
        self.body.append('</p>\n')

    def visit_section(self, node):
        self.section_level = node.get('depth', 1)

    def depart_section(self, node):
        self.section_level -= 1

    def visit_target(self, node):
        raise nodes.SkipNode

    def visit_transition(self, node):
        self.body.append(self.emptytag(node, 'hr'))

    def visit_enumerated_list(self, node):
        if node.get('start') != 1:
            self.body.append('<ol start="%s">\n' % node['start'])
        else:
            self.body.append('<ol>\n')

    def visit_list_item(self, node):
        if len(node) == 0:
            self.body.append('<li>')
        elif isinstance(node[0], nodes.Text):
            self.body.append('<li>')
        else:
            self.body.append('<li>\n')

    def visit_literal(self, node):
        self.body.append('<code>')

    def depart_literal(self, node):
        self.body.append('</code>')

    def visit_literal_block(self, node):
        if len(node['classes']) > 1:
            self.body.append('<pre><code class="%s">' % html.escape(node['classes'][1]))
        else:
            self.body.append('<pre><code>')

    def depart_literal_block(self, node):
        self.body.append('</code></pre>\n')

    def visit_reference(self, node):
        atts = []
        if 'refuri' in node:
            atts.append('href="%s"' % html.escape(node['refuri']))
        else:
            atts.append('href="#%s"' % html.escape(node['refid']))
        if 'reftitle' in node:
            atts.append('title="%s"' % html.escape(node['reftitle']))
        self.body.append('<a %s>' % ' '.join(atts))

    def visit_image(self, node):
        atts = ['src="%s"' % html.escape(node['uri'])]
        if 'alt' in node:
            atts.append('alt="%s"' % html.escape(node['alt']))
        if 'title' in node:
            atts.append('title="%s"' % html.escape(node['title']))
        self.body.append('<img %s />' % ' '.join(atts))

    def visit_linebreak(self, node):
        self.body.append('<br />\n')

    def depart_linebreak(self, node):
        pass


class TestReader(standalone.Reader):
    def get_transforms(self):
        transforms = super().get_transforms()
        transforms.remove(Transitions)
        return transforms


class TestCommonMarkParser(Parser):
    def get_transforms(self):
        transforms = super().get_transforms()
        transforms.remove(LinebreakFilter)
        transforms.remove(SectionTreeConstructor)
        return transforms


def convert(source):
    html = publish_string(source=source,
                          source_path='dummy.md',
                          reader=TestReader(),
                          parser=TestCommonMarkParser(),
                          writer=HTMLWriter(),
                          settings_overrides={'embed_stylesheet': False,
                                              'compact_lists': False,
                                              'doctitle_xform': False,
                                              'report_level': 999})
    return html.decode('utf-8')


if __name__ == '__main__':
    result = convert(sys.stdin.read().encode('utf-8'))
    if result:
        print(result)
