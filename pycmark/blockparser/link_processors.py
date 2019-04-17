"""
    pycmark.blockparser.link_processors
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Link processor classes for BlockParser.

    :copyright: Copyright 2017-2019 by Takeshi KOMIYA
    :license: Apache License 2.0, see LICENSE for details.
"""

import re
from typing import Tuple

from docutils import nodes
from docutils.nodes import Element
from docutils.nodes import fully_normalize_name

from pycmark.blockparser import PatternBlockProcessor
from pycmark.inlineparser.link_processors import LinkDestinationParser
from pycmark.readers import LineReader, MultiLineReader
from pycmark.utils import ESCAPED_CHARS, get_root_document, entitytrans, normalize_link_label, unescape


# 4.7 Link reference definitions
class LinkReferenceDefinitionProcessor(PatternBlockProcessor):
    priority = 750  # Before ParagraphProcessor
    LABEL_CHARACTER = r'(?:[^\[\]\\]|' + ESCAPED_CHARS + r'|\\)'
    pattern = re.compile(r'^ {0,3}\[(' + LABEL_CHARACTER + r'*)(?:\]:|$)')
    following_label_pattern = re.compile('^(' + LABEL_CHARACTER + r'*)(?:\]:|$)')
    whitespace_pattern = re.compile('([ \t]+|(?=\n|$))')
    eol_pattern = re.compile('\\s*(\n|$)')
    title_pattern = re.compile(r'\s*("(' + ESCAPED_CHARS + r'|[^"])*(?:"|$)|' +
                               r"'(" + ESCAPED_CHARS + r"|[^'])*(?:'|$)|" +
                               r"\((" + ESCAPED_CHARS + r"|[^)])*(?:\)|$))")

    def run(self, reader: LineReader, document: Element) -> bool:
        lineno = reader.lineno
        try:
            multiline_reader = MultiLineReader(reader)
            target = self.parse_linkref_definition(multiline_reader, document)
            if target:
                document += target
                return True
            else:
                reader.step(lineno - reader.lineno)  # rollback
                return False
        except IOError:
            reader.step(lineno - reader.lineno)  # rollback
            return False

    def parse_linkref_definition(self, reader: MultiLineReader, node: Element) -> nodes.target:
        reader.readline()

        name, label = self.parse_link_label(reader)
        if not label:
            return None

        self.skip_over_whitespace(reader)

        destination = self.parse_link_destination(reader, node)
        if destination is None:
            return None

        if self.ensure_whitespace(reader) is False:
            return None

        # parse link title
        position = reader.position
        title = self.parse_link_title(reader, node)
        if title is None or self.ensure_eol(reader) is False:
            # title not found or unknown text remains
            title = None
            reader.rewind(position)  # rollback cursor
            if self.ensure_eol(reader) is False:
                return None

        # build title node
        if title:
            target = nodes.target('', names=[name], refuri=destination, title=title)
        else:
            target = nodes.target('', names=[label], refuri=destination)

        document = get_root_document(node)
        if target['names'][0] not in document.nameids:
            document.note_explicit_target(target)
        else:
            document.reporter.warning('Duplicate explicit target name: "%s"' % target['names'][0],
                                      source=node.source, line=node.line)
        return target

    def parse_link_label(self, reader: MultiLineReader) -> Tuple[str, str]:
        matched = reader.consume(self.pattern)
        if not matched:
            return None, None

        label = matched.group(1)
        while not matched.group(0).endswith(']:'):
            # link label on multiple line
            reader.readline()
            matched = reader.consume(self.following_label_pattern)
            if not matched:
                return None, None
            elif matched.group(0) == '\n':  # empty line
                return None, None
            else:
                label += matched.group(1)

        name = fully_normalize_name(label)
        label = normalize_link_label(label)
        return name, label

    def skip_over_whitespace(self, reader: MultiLineReader) -> None:
        reader.consume(self.whitespace_pattern)

    def parse_link_destination(self, reader: MultiLineReader, node: Element) -> str:
        # try parsing link destination on following line
        if reader.eol():
            reader.readline()

        position = reader.position
        destination = LinkDestinationParser().parse(reader.text_reader, node)
        if position == reader.position:
            return None
        else:
            return destination

    def ensure_whitespace(self, reader: MultiLineReader) -> bool:
        return bool(reader.consume(self.whitespace_pattern))

    def parse_link_title(self, reader: MultiLineReader, node: Element) -> str:
        try:
            # try parsing link destination on following line
            if reader.eol():
                reader.readline()

            matched = reader.consume(self.title_pattern)
            if not matched:
                return None

            title = matched.group(1)
            quote = title[0]
            following_pattern = re.compile(r"^((" + ESCAPED_CHARS + r"|[^%s])*(?:\%s|$))" % (quote, quote))

            while not matched.group(1).endswith(quote):
                # link title on multiple line
                reader.readline()
                matched = reader.consume(following_pattern)
                if not matched:
                    return None
                elif matched.group(1) == '\n':  # empty line
                    return None
                else:
                    title += matched.group(1)

            return unescape(entitytrans._unescape(title[1:-1]))
        except IOError:
            return None

    def ensure_eol(self, reader: MultiLineReader) -> bool:
        return bool(reader.consume(self.eol_pattern))
