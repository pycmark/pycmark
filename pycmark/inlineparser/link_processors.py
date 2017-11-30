# -*- coding: utf-8 -*-
"""
    pycmark.inlineparser.link_processors
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Link processor classes for InlineParser.

    :copyright: Copyright 2017 by Takeshi KOMIYA
    :license: BSD, see LICENSE for details.
"""

import re
from docutils import nodes
from pycmark import addnodes
from pycmark.inlineparser import PatternInlineProcessor, backtrack_onerror
from pycmark.utils import entitytrans
from pycmark.utils import ESCAPED_CHARS, escaped_chars_pattern, unescape, normalize_link_label, transplant_nodes

LABEL_NOT_MATCHED = object()


# 6.5 Links
# 6.6 Images
class LinkOpenerProcessor(PatternInlineProcessor):
    pattern = re.compile('\!?\[')

    def run(self, document, reader):
        marker = reader.consume(self.pattern).group(0)
        document += addnodes.bracket(marker=marker, can_open=True, active=True, position=reader.position)
        return True


class LinkCloserProcessor(PatternInlineProcessor):
    pattern = re.compile('\]')

    def run(self, document, reader):
        reader.step(1)
        document += addnodes.bracket(marker="]", can_open=False, position=reader.position - 1)
        self.process_link_or_image(document, reader)
        return True

    @backtrack_onerror
    def process_link_or_image(self, document, reader):
        brackets = list(n for n in document.children if isinstance(n, addnodes.bracket))
        openers = list(d for d in brackets if d['can_open'])
        if len(openers) == 0:
            return

        opener = openers.pop()
        closer = brackets.pop()

        if not opener['active']:
            opener.replace_self(nodes.Text(opener['marker']))
            closer.replace_self(nodes.Text(closer['marker']))
            return

        try:
            if reader.remain.startswith('('):
                # link destination + link title (optional)
                #     [...](<.+> ".+")
                #     [...](.+ ".+")
                destination, title = self.parse_link_destination(document, reader)
            elif reader.remain.startswith('['):
                # link label
                #     [...][.+]
                #     [...][]
                destination, title = self.parse_link_label(document, reader, opener=opener, closer=closer)
            else:
                destination = None
                title = None
        except (TypeError, ValueError):
            destination = None
            title = None

        if destination is None:
            # shortcut reference link
            #    [...]
            refid = reader[opener['position']:closer['position']]
            target = self.lookup_target(document, refid)
            if target:
                destination = target.get('refuri')
                title = target.get('title')
            else:
                # deactivate brackets because no trailing link destination or link-label
                opener.replace_self(nodes.Text(opener['marker']))
                closer.replace_self(nodes.Text(closer['marker']))
                raise
        elif destination == LABEL_NOT_MATCHED:
            opener.replace_self(nodes.Text(opener['marker']))
            closer.replace_self(nodes.Text(closer['marker']))
            raise

        if opener['marker'] == '![':
            para = transplant_nodes(document, nodes.paragraph(), start=opener, end=closer)
            node = nodes.image('', uri=destination, alt=para.astext())
            if title:
                node['title'] = title
        else:
            node = nodes.reference('', refuri=destination)
            transplant_nodes(document, node, start=opener, end=closer)
            if title:
                node['reftitle'] = title

            # deactivate all left brackets before the link
            for n in openers:
                if n['marker'] == '[':
                    n['active'] = False

        document += node
        document.remove(opener)
        document.remove(closer)
        return True

    @backtrack_onerror
    def parse_link_destination(self, document, reader):
        reader.step()
        destination = LinkDestinationParser().parse(document, reader)
        title = LinkTitleParser().parse(document, reader)
        assert reader.consume(re.compile('\s*\)'))

        return destination, title

    @backtrack_onerror
    def parse_link_label(self, document, reader, opener=None, closer=None):
        reader.step()
        refid = LinkLabelParser().parse(document, reader)
        if refid == '':
            # collapsed reference link
            #     [...][]
            refid = reader[opener['position']:closer['position']]

        target = self.lookup_target(document, refid)
        if target:
            destination = target.get('refuri')
            title = target.get('title')
            return destination, title
        else:
            return LABEL_NOT_MATCHED, None

    def lookup_target(self, document, refid):
        while document.parent:
            document = document.parent

        node_id = document.nameids.get(normalize_link_label(refid))
        if node_id is None:
            return None

        return document.ids.get(node_id)


class LinkDestinationParser(object):
    pattern = re.compile(r'\s*<((?:[^ <>\n\\]|' + ESCAPED_CHARS + r'|\\)*)>', re.S)

    def parse(self, document, reader):
        matched = reader.consume(self.pattern)
        if matched:
            return unescape(entitytrans._unescape(matched.group(1)))
        else:
            return self.parseBareLinkDestination(document, reader)

    def parseBareLinkDestination(self, document, reader):
        assert reader.consume(re.compile('[ \n]*'))

        parens = 0
        start = reader.position
        while reader.remain:
            c = reader.remain[0]
            if c in (' ', '\n'):
                break
            elif c == '(':
                parens += 1
            elif c == ')':
                parens -= 1
                if parens < 0:
                    break
            elif escaped_chars_pattern.match(reader.remain):
                reader.step()  # one more step for escaping

            reader.step()

        end = reader.position
        return unescape(entitytrans._unescape(reader[start:end]))


class LinkTitleParser(object):
    pattern = re.compile('\s*("(' + ESCAPED_CHARS + '|[^"])*"|' +
                         "'(" + ESCAPED_CHARS + "|[^'])*'|" +
                         "\\((" + ESCAPED_CHARS + "|[^)])*\\))")

    def parse(self, document, reader):
        matched = reader.consume(self.pattern)
        if matched:
            return unescape(entitytrans._unescape(matched.group(1)[1:-1]))
        else:
            return None


class LinkLabelParser(object):
    pattern = re.compile(r'(?:[^\[\]\\]|' + ESCAPED_CHARS + r'|\\){0,1000}\]')

    def parse(self, document, reader):
        matched = reader.consume(self.pattern)
        if matched:
            return unescape(matched.group(0)[:-1])
        else:
            return None
