"""
    pycmark.inlineparser.link_processors
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Link processor classes for InlineParser.

    :copyright: Copyright 2017-2019 by Takeshi KOMIYA
    :license: Apache License 2.0, see LICENSE for details.
"""

import re
from typing import Tuple

from docutils import nodes
from docutils.nodes import Element, Text
from docutils.nodes import fully_normalize_name

from pycmark import addnodes
from pycmark.inlineparser import PatternInlineProcessor, backtrack_onerror
from pycmark.readers import TextReader
from pycmark.utils import entitytrans, normalize_uri
from pycmark.utils import ESCAPED_CHARS, escaped_chars_pattern, get_root_document, unescape, transplant_nodes

LABEL_NOT_MATCHED = object()


# 6.5 Links
# 6.6 Images
class LinkOpenerProcessor(PatternInlineProcessor):
    pattern = re.compile(r'\!?\[')

    def run(self, reader: TextReader, document: Element) -> bool:
        marker = reader.consume(self.pattern).group(0)
        document += addnodes.bracket(marker=marker, can_open=True, active=True, position=reader.position)
        return True


class LinkCloserProcessor(PatternInlineProcessor):
    pattern = re.compile(r'\]')

    def run(self, reader: TextReader, document: Element) -> bool:
        reader.step(1)
        document += addnodes.bracket(marker="]", can_open=False, position=reader.position - 1)
        self.process_link_or_image(reader, document)
        return True

    @backtrack_onerror
    def process_link_or_image(self, reader: TextReader, document: Element) -> bool:
        brackets = list(n for n in document.children if isinstance(n, addnodes.bracket))
        openers = list(d for d in brackets if d['can_open'])
        if len(openers) == 0:
            return True

        opener = openers.pop()
        closer = brackets.pop()

        if not opener['active']:
            opener.replace_self(Text(opener['marker']))
            closer.replace_self(Text(closer['marker']))
            return True

        try:
            if reader.remain.startswith('('):
                # link destination + link title (optional)
                #     [...](<.+> ".+")
                #     [...](.+ ".+")
                destination, title = self.parse_link_destination(reader, document)
            elif reader.remain.startswith('['):
                # link label
                #     [...][.+]
                #     [...][]
                destination, title = self.parse_link_label(reader, document, opener=opener, closer=closer)
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
                opener.replace_self(Text(opener['marker']))
                closer.replace_self(Text(closer['marker']))
                raise
        elif destination == LABEL_NOT_MATCHED:
            opener.replace_self(Text(opener['marker']))
            closer.replace_self(Text(closer['marker']))
            raise

        node: Element = None
        if opener['marker'] == '![':
            from pycmark.transforms import EmphasisConverter  # lazy loading
            para = transplant_nodes(document, nodes.paragraph(), start=opener, end=closer)
            EmphasisConverter(para).apply()
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
    def parse_link_destination(self, reader: TextReader, document: Element) -> Tuple[str, str]:
        reader.step()
        destination = LinkDestinationParser().parse(reader, document)
        title = LinkTitleParser().parse(reader, document)
        assert reader.consume(re.compile(r'\s*\)'))

        return destination, title

    @backtrack_onerror
    def parse_link_label(self, reader: TextReader, document: Element, opener: Element = None, closer: Element = None) -> Tuple[object, str]:  # NOQA
        reader.step()
        refname = LinkLabelParser().parse(reader, document)
        if refname == '':
            # collapsed reference link
            #     [...][]
            refname = reader[opener['position']:closer['position']]

        target = self.lookup_target(document, refname)
        if target:
            destination = target.get('refuri')
            title = target.get('title')
            return destination, title
        else:
            return LABEL_NOT_MATCHED, None

    def lookup_target(self, node: Element, refname: str) -> nodes.Element:
        document = get_root_document(node)

        refname = fully_normalize_name(refname)
        node_id = document.nameids.get(refname)
        if node_id is None:
            return None

        return document.ids.get(node_id)


class LinkDestinationParser:
    pattern = re.compile(r'\s*<((?:[^ <>\n\\]|' + ESCAPED_CHARS + r'|\\)*)>', re.S)

    def parse(self, reader: TextReader, document: Element) -> str:
        matched = reader.consume(self.pattern)
        if matched:
            return self.normalize_link_destination(matched.group(1))
        else:
            return self.parseBareLinkDestination(reader, document)

    def normalize_link_destination(self, s: str) -> str:
        s = entitytrans._unescape(s)
        s = unescape(s)
        s = normalize_uri(s)
        return s

    def parseBareLinkDestination(self, reader: TextReader, document: Element) -> str:
        assert reader.consume(re.compile(r'[ \n]*'))

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
        return self.normalize_link_destination(reader[start:end])


class LinkTitleParser:
    pattern = re.compile(r'\s*("(' + ESCAPED_CHARS + r'|[^"])*"|' +
                         r"'(" + ESCAPED_CHARS + r"|[^'])*'|" +
                         r"\((" + ESCAPED_CHARS + r"|[^)])*\))")

    def parse(self, reader: TextReader, document: Element) -> str:
        matched = reader.consume(self.pattern)
        if matched:
            return unescape(entitytrans._unescape(matched.group(1)[1:-1]))
        else:
            return None


class LinkLabelParser:
    pattern = re.compile(r'(?:[^\[\]\\]|' + ESCAPED_CHARS + r'|\\){0,1000}\]')

    def parse(self, reader: TextReader, document: Element) -> str:
        matched = reader.consume(self.pattern)
        if matched:
            return matched.group(0)[:-1]
        else:
            return None
