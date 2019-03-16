"""
    pycmark.blockparser.std_processors
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Standard processor classes for BlockParser.

    :copyright: Copyright 2017-2019 by Takeshi KOMIYA
    :license: BSD, see LICENSE for details.
"""

import re

from docutils import nodes
from docutils.nodes import Element, Node

from pycmark import addnodes
from pycmark.blockparser import BlockProcessor, PatternBlockProcessor
from pycmark.readers import (
    FencedCodeBlockReader, IndentedCodeBlockReader, LazyLineReader, LineReader
)
from pycmark.utils import entitytrans, unescape


# 4.1 Thematic breaks
class ThematicBreakProcessor(PatternBlockProcessor):
    paragraph_interruptable = True
    pattern = re.compile(r'^ {0,3}((\*\s*){3,}|(-\s*){3,}|(_\s*){3,})\s*$')

    def run(self, document: Element, reader: LineReader) -> bool:
        reader.readline()
        document += nodes.transition()
        return True


# 4.2 ATX headings
class ATXHeadingProcessor(PatternBlockProcessor):
    paragraph_interruptable = True
    pattern = re.compile(r'^ {0,3}(#{1,6})(\s.*)$')
    trailing_hashes = re.compile(r'\s+#+\s*$')

    def run(self, document: Element, reader: LineReader) -> bool:
        marker, title = self.pattern.match(reader.readline()).groups()
        title = self.trailing_hashes.sub('', title).strip()
        title_node = nodes.title(title, title)
        title_node.source, title_node.line = reader.get_source_and_line()
        document += nodes.section('', title_node, depth=len(marker))
        self.note_implicit_target(document, document[-1])
        return True

    def note_implicit_target(self, document: Element, node: Node) -> None:
        while document.parent:
            document = document.parent

        document.note_implicit_target(node)  # type: ignore


# 4.4 Indented code blocks
class IndentedCodeBlockProcessor(PatternBlockProcessor):
    paragraph_interruptable = False
    pattern = re.compile(r'^    (.*\n?)$')
    followings = re.compile(r'^(    (.*\n?)|\s*)$')

    def run(self, document: Element, reader: LineReader) -> bool:
        source, lineno = reader.get_source_and_line()

        code = ''.join(IndentedCodeBlockReader(reader))
        code = re.sub('^\n+', '', code)  # strip blank lines
        code = re.sub('\n+$', '\n', code)  # strip blank lines
        document += nodes.literal_block(code, code, classes=['code'])
        document[-1].source = source
        document[-1].line = lineno + 1  # lineno points previous line
        return True


# 4.5 Fenced code blocks
class BacktickFencedCodeBlockProcessor(PatternBlockProcessor):
    paragraph_interruptable = True
    pattern = re.compile(r'^( {0,3})(`{3,})([^`]*)$')

    def run(self, document: Element, reader: LineReader) -> bool:
        source, lineno = reader.get_source_and_line()

        indent, marker, info = self.pattern.match(reader.readline()).groups()
        code = ''.join(FencedCodeBlockReader(reader, len(indent), marker))

        literal_block = nodes.literal_block(code, code, classes=['code'])
        literal_block.source = source
        literal_block.line = lineno + 1  # lineno points previous line
        if info.strip():
            language = unescape(entitytrans._unescape(info.split()[0].strip()))
            literal_block['language'] = language
            literal_block['classes'].append('language-%s' % language.split()[0])
        document += literal_block

        return True


class TildeFencedCodeBlockProcessor(BacktickFencedCodeBlockProcessor):
    paragraph_interruptable = True
    pattern = re.compile(r'^( {0,3})(~{3,})(.*)$')


# 4.3 Setext headings
# 4.7 Link reference definitions
# 4.8 Paragraphs
class ParagraphProcessor(BlockProcessor):
    setext_heading_underline = re.compile(r'^ {0,3}(=+|-+)\s*$')

    def match(self, reader: LineReader, **kwargs) -> bool:
        return True

    def run(self, document: Element, reader: LineReader) -> bool:
        source, lineno = reader.get_source_and_line()
        node = self.read(reader, setext_heading_allowed=True)
        if isinstance(node, nodes.section):
            node[0].source = source
            node[0].line = lineno + 1  # lineno points previous line
            self.note_implicit_target(document, node)
        else:
            text = self.read(LazyLineReader(reader), node.rawsource).rawsource.strip()
            node = nodes.paragraph(text, text)
            node.source = source
            node.line = lineno + 1  # lineno points previous line

        document += node
        return True

    def read(self, reader: LineReader, text: str = '', setext_heading_allowed: bool = False) -> Element:
        def get_depth(line: str) -> int:
            if line.strip()[0] == '=':
                return 1
            else:
                return 2

        while not reader.eof():
            try:
                if text and setext_heading_allowed and self.setext_heading_underline.match(reader.next_line):
                    line = reader.readline()
                    section = nodes.section(depth=get_depth(line))
                    section += nodes.title(text.strip(), text.strip())
                    return section
                elif self.parser.is_interrupted(reader):
                    break

                line = reader.readline()
                text += line.lstrip()
            except IOError:
                break

        return nodes.paragraph(text, text)

    def note_implicit_target(self, document: Element, node: Node) -> None:
        while document.parent:
            document = document.parent

        document.note_implicit_target(node)  # type: ignore


# 4.9 Blank lines
class BlankLineProcessor(PatternBlockProcessor):
    paragraph_interruptable = True
    pattern = re.compile(r'^\s*$')

    def run(self, document: Element, reader: LineReader) -> bool:
        reader.readline()  # skip the line
        document += addnodes.blankline()
        return True
