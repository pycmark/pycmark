# -*- coding: utf-8 -*-
"""
    pycmark.transforms
    ~~~~~~~~~~~~~~~~~~

    Transform classes for BlockParser.

    :copyright: Copyright 2017 by Takeshi KOMIYA
    :license: BSD, see LICENSE for details.
"""

import re
import typing
from docutils import nodes
from docutils.transforms import Transform
from pycmark import addnodes
from pycmark.readers import TextReader
from pycmark.inlineparser import InlineParser, backtrack_onerror
from pycmark.inlineparser.link_processors import LinkDestinationParser, LinkTitleParser
from pycmark.utils import ESCAPED_CHARS, normalize_link_label, transplant_nodes
from typing import List, cast

if typing.TYPE_CHECKING:
    from typing import Any  # NOQA


class BlanklineFilter(Transform):
    default_priority = 500

    def apply(self):
        for node in self.document.traverse(addnodes.blankline):
            node.parent.remove(node)


class TightListsDetector(Transform):
    default_priority = BlanklineFilter.default_priority - 1  # must be eariler than BlanklineFilter

    def apply(self, **kwargs):
        # type: (Any) -> None
        self.detect(self.document)

    def detect(self, document):
        # type: (nodes.Element) -> None
        def is_list_node(node):
            # type: (nodes.Node) -> bool
            return isinstance(node, (nodes.bullet_list, nodes.enumerated_list))

        def has_loose_element(node):
            # type: (nodes.Element) -> bool
            return any(isinstance(subnode, addnodes.blankline) for subnode in node)

        for node in document.traverse(is_list_node):  # type: nodes.Element
            children = cast(List[nodes.list_item], node)
            if any(has_loose_element(item) for item in children):
                node['tight'] = False
            else:
                node['tight'] = True

            # detect loose lists in list_items
            for list_item in children:
                self.detect(list_item)


class TightListsCompactor(Transform):
    default_priority = 999

    def apply(self):
        def is_tight_list(node):
            # type: (nodes.Node) -> bool
            return (isinstance(node, (nodes.bullet_list, nodes.enumerated_list)) and
                    node['tight'] is True)

        for list_node in self.document.traverse(is_tight_list):
            for list_item in list_node:
                for para in list_item[:]:
                    pos = list_item.index(para)
                    if isinstance(para, nodes.paragraph):
                        for i, text in enumerate(para[:]):
                            para.remove(text)
                            list_item.insert(pos + i + 1, text)
                        list_item.remove(para)


class SectionTreeConstructor(Transform):
    default_priority = 500

    def apply(self):
        def is_container_node(node):
            return isinstance(node, (nodes.document, nodes.block_quote, nodes.list_item))

        for node in self.document.traverse(is_container_node):
            self.construct_section_tree(node)

    def construct_section_tree(self, container):
        current_depth = 0
        last_section = None
        for node in container[:]:
            if isinstance(node, nodes.section):
                if current_depth + 1 < node['depth']:
                    msg = ('Invalid deep section "%s" (<h%d>) appeared. Recognized a <h%d>.' %
                           (node.astext(), node['depth'], current_depth + 1))
                    self.document.reporter.warning(msg, source=node[0].source, line=node[0].line)
                    node['depth'] = current_depth + 1
                elif current_depth >= node['depth']:
                    # leave the section
                    for _ in range(current_depth - node['depth'] + 1):
                        if last_section is not None:
                            last_section = last_section.parent

                if last_section:
                    node.parent.remove(node)
                    last_section += node

                current_depth = node['depth']
                last_section = node
            else:
                if last_section:
                    node.parent.remove(node)
                    last_section += node


class LinkReferenceDefinitionDetector(Transform):
    default_priority = 100
    pattern = re.compile(r'\s*\[((?:[^\[\]\\]|' + ESCAPED_CHARS + r'|\\)+)\]:')

    def apply(self):
        for node in self.document.traverse(nodes.paragraph):
            reader = TextReader(node[0])
            self.parse_linkref_definition(node, reader)

    @backtrack_onerror
    def parse_linkref_definition(self, node, reader):
        targets = []
        while True:
            matched = reader.consume(self.pattern)
            if not matched:
                break
            else:
                label = normalize_link_label(matched.group(1))
                if label.strip() == '':
                    break
                destination = LinkDestinationParser().parse(node, reader)
                if destination == '':
                    break
                title = LinkTitleParser().parse(node, reader)
                eol = reader.consume(re.compile('\s*(\n|$)'))
                if eol is None:
                    break

                target = nodes.target('', names=[label], refuri=destination, title=title)
                if label not in self.document.nameids:
                    self.document.note_explicit_target(target)
                else:
                    self.document.reporter.warning('Duplicate explicit target name: "%s"' % label,
                                                   source=node.source, line=node.line)
                targets.append(target)

        if targets:
            # insert found targets before the paragraph
            pos = node.parent.index(node)
            for target in reversed(targets):
                node.parent.insert(pos, target)

            if reader.remain:
                node.pop(0)
                node.insert(0, nodes.Text(reader.remain))
            else:
                node.parent.remove(node)


class InlineTransform(Transform):
    default_priority = 200

    def apply(self):
        def is_text_container(node):
            return isinstance(node, nodes.TextElement) and not isinstance(node, nodes.FixedTextElement)

        parser = self.create_parser()
        for node in self.document.traverse(is_text_container):
            parser.parse(node)

    def create_parser(self):
        parser = InlineParser()
        for processor in self.document.settings.inline_processors:
            parser.add_processor(processor(parser))

        return parser


class SparseTextConverter(Transform):
    default_priority = 900

    def apply(self):
        for node in self.document.traverse(addnodes.SparseText):
            pos = node.parent.index(node)
            node.parent.remove(node)
            node.parent.insert(pos, nodes.Text(str(node)))


class EmphasisConverter(Transform):
    default_priority = 900

    def apply(self):
        for node in self.document.traverse(nodes.TextElement):
            while True:
                markers = list(n for n in node.children if isinstance(n, addnodes.emphasis))
                closers = list(d for d in markers if d['can_close'])
                if len(closers) == 0:
                    break
                closer = closers[0]
                opener = self.find_opener(markers, closer)
                if opener is None:
                    closer['can_close'] = False
                    continue

                if opener['curr_length'] >= 2 and closer['curr_length'] >= 2:
                    length = 2
                    emph_node = nodes.strong()
                else:
                    length = 1
                    emph_node = nodes.emphasis()

                transplant_nodes(node, emph_node, start=opener, end=closer)
                self.deactivate_markers(emph_node)

                opener_pos = node.index(opener)
                node.insert(opener_pos + 1, emph_node)
                opener.shrink(length)
                closer.shrink(length)

            self.deactivate_markers(node)

    def find_opener(self, markers, closer):
        pos = markers.index(closer)
        for opener in reversed(markers[:pos]):
            if opener['can_open'] is False:
                continue
            elif opener['marker'][0] != closer['marker'][0]:
                continue
            else:
                odd_match = ((closer['can_open'] or opener['can_close']) and
                             (opener['orig_length'] + closer['orig_length']) % 3 == 0)
                if not odd_match:
                    return opener

        return None

    def deactivate_markers(self, node):
        markers = list(n for n in node.children if isinstance(n, addnodes.emphasis))
        for delim in markers:
            marker = str(delim)
            delim.replace_self(nodes.Text(marker, marker))


class BracketConverter(Transform):
    default_priority = 900

    def apply(self):
        for node in self.document.traverse(addnodes.bracket):
            node.replace_self(nodes.Text(node['marker']))


class TextNodeConnector(Transform):
    default_priority = 950  # must be executed after SparseTextConverter

    def apply(self):
        for node in self.document.traverse(nodes.TextElement):
            pos = 0
            while len(node) > pos + 1:
                if isinstance(node[pos], nodes.Text) and isinstance(node[pos + 1], nodes.Text):
                    text = node[pos] + node[pos + 1]
                    node.remove(node[pos + 1])
                    node.remove(node[pos])
                    node.insert(pos, nodes.Text(text, text))
                else:
                    pos += 1
