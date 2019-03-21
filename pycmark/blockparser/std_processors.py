"""
    pycmark.blockparser.std_processors
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Standard processor classes for BlockParser.

    :copyright: Copyright 2017-2019 by Takeshi KOMIYA
    :license: Apache License 2.0, see LICENSE for details.
"""

import re

from docutils import nodes
from docutils.nodes import Element

from pycmark import addnodes
from pycmark.blockparser import BlockProcessor, PatternBlockProcessor
from pycmark.readers import (
    FencedCodeBlockReader, IndentedCodeBlockReader, LazyLineReader, LineReader
)
from pycmark.utils import entitytrans, get_root_document, unescape


# 4.1 Thematic breaks
class ThematicBreakProcessor(PatternBlockProcessor):
    priority = 200
    paragraph_interruptable = True
    pattern = re.compile(r'^ {0,3}((\*\s*){3,}|(-\s*){3,}|(_\s*){3,})\s*$')

    def run(self, reader: LineReader, document: Element) -> bool:
        reader.readline()
        document += nodes.transition()
        return True


# 4.2 ATX headings
class ATXHeadingProcessor(PatternBlockProcessor):
    paragraph_interruptable = True
    pattern = re.compile(r'^ {0,3}(#{1,6})(\s.*)$')
    trailing_hashes = re.compile(r'\s+#+\s*$')

    def run(self, reader: LineReader, document: Element) -> bool:
        marker, title = self.pattern.match(reader.readline()).groups()
        title = self.trailing_hashes.sub('', title).strip()
        title_node = nodes.title(title, title)
        title_node.source, title_node.line = reader.get_source_and_line()
        section = nodes.section('', title_node, depth=len(marker))
        get_root_document(document).note_implicit_target(section)

        document += section
        return True


# 4.3 Setext headings
class SetextHeadingProcessor(BlockProcessor):
    priority = 750
    pattern = re.compile(r'^ {0,3}(=+|-+)\s*$')
    section_level = {'=': 1, '-': 2}

    def match(self, reader: LineReader, **kwargs) -> bool:
        return True

    def run(self, reader: LineReader, document: Element) -> bool:
        location = reader.get_source_and_line(incr=1)

        lines = []
        underline = None
        try:
            for line in reader:
                lines.append(line.lstrip())
                if self.pattern.match(reader.next_line):
                    underline = reader.readline()
                    break
                elif self.parser.is_interrupted(reader):
                    break
        except IOError:
            pass

        if underline is None:
            # underline of heading not found. backtracking.
            reader.step(-len(lines))
            return False
        else:
            text = ''.join(lines).strip()
            depth = self.section_level[underline.strip()[0]]
            section = nodes.section(depth=depth)
            section += nodes.title(text, text)
            location.set_source_info(section[0])
            get_root_document(document).note_implicit_target(section)

            document += section
            return True


# 4.4 Indented code blocks
class IndentedCodeBlockProcessor(PatternBlockProcessor):
    paragraph_interruptable = False
    pattern = re.compile(r'^    (.*\n?)$')
    followings = re.compile(r'^(    (.*\n?)|\s*)$')

    def run(self, reader: LineReader, document: Element) -> bool:
        location = reader.get_source_and_line(incr=1)

        code = ''.join(IndentedCodeBlockReader(reader))
        code = re.sub('^\n+', '', code)  # strip blank lines
        code = re.sub('\n+$', '\n', code)  # strip blank lines
        document += nodes.literal_block(code, code, classes=['code'])
        location.set_source_info(document[-1])
        return True


# 4.5 Fenced code blocks
class BacktickFencedCodeBlockProcessor(PatternBlockProcessor):
    paragraph_interruptable = True
    pattern = re.compile(r'^( {0,3})(`{3,})([^`]*)$')

    def run(self, reader: LineReader, document: Element) -> bool:
        location = reader.get_source_and_line(incr=1)

        indent, marker, info = self.pattern.match(reader.readline()).groups()
        code = ''.join(FencedCodeBlockReader(reader, len(indent), marker))

        literal_block = nodes.literal_block(code, code, classes=['code'])
        location.set_source_info(literal_block)
        if info.strip():
            language = unescape(entitytrans._unescape(info.split()[0].strip()))
            literal_block['language'] = language
            literal_block['classes'].append('language-%s' % language.split()[0])
        document += literal_block

        return True


class TildeFencedCodeBlockProcessor(BacktickFencedCodeBlockProcessor):
    paragraph_interruptable = True
    pattern = re.compile(r'^( {0,3})(~{3,})(.*)$')


# 4.7 Link reference definitions
# 4.8 Paragraphs
class ParagraphProcessor(BlockProcessor):
    priority = 800

    def match(self, reader: LineReader, **kwargs) -> bool:
        return True

    def run(self, reader: LineReader, document: Element) -> bool:
        location = reader.get_source_and_line(incr=1)
        reader = LazyLineReader(reader)

        text = ''
        for line in reader:
            text += line.lstrip()
            if self.parser.is_interrupted(reader):
                break

        node = nodes.paragraph(text.strip(), text.strip())
        location.set_source_info(node)
        document += node

        return True


# 4.9 Blank lines
class BlankLineProcessor(PatternBlockProcessor):
    paragraph_interruptable = True
    pattern = re.compile(r'^\s*$')

    def run(self, reader: LineReader, document: Element) -> bool:
        reader.readline()  # skip the line
        document += addnodes.blankline()
        return True
