# -*- coding: utf-8 -*-
"""
    pycmark.blockparser.std_processors
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Standard processor classes for BlockParser.

    :copyright: Copyright 2017 by Takeshi KOMIYA
    :license: BSD, see LICENSE for details.
"""

import re
from docutils import nodes
from pycmark import addnodes
from pycmark.blockparser import BlockProcessor, PatternBlockProcessor
from pycmark.readers import LazyLineReader
from pycmark.utils import entitytrans


# 4.1 Thematic breaks
class ThematicBreakProcessor(PatternBlockProcessor):
    paragraph_interruptable = True
    pattern = re.compile('^ {0,3}((\*\s*){3,}|(-\s*){3,}|(_\s*){3,})\s*$')

    def run(self, document, reader):
        reader.readline()
        document += nodes.transition()
        return True


# 4.2 ATX headings
class ATXHeadingProcessor(PatternBlockProcessor):
    paragraph_interruptable = True
    pattern = re.compile('^ {0,3}(#{1,6})\s(.*)$')
    trailing_hashes = re.compile('\s+#+\s*$')

    def run(self, document, reader):
        marker, title = self.pattern.match(reader.readline()).groups()
        title = self.trailing_hashes.sub('', title.strip())
        title_node = nodes.title(title, title)
        title_node.source, title_node.line = reader.get_source_and_line()
        document += nodes.section('', title_node, depth=len(marker))
        return True


# 4.4 Indented code blocks
class IndentedCodeBlockProcessor(PatternBlockProcessor):
    paragraph_interruptable = False
    pattern = re.compile('^(    | {0,3}\t)(.*\n?)$')
    followings = re.compile('^((?:    | {0,3}\t)(.*\n?)|\s*)$')

    def run(self, document, reader):
        source, lineno = reader.get_source_and_line()

        code = ''
        for line in reader:
            matched = self.followings.match(line)
            if matched:
                if matched.group(2):
                    code += matched.group(2)
                else:
                    code += "\n"
            else:
                reader.step(-1)
                break

        code = re.sub('^\n*(.*\n)\n*$', '\\1', code)  # strip blank lines
        document += nodes.literal_block(code, code)
        document[-1].source = source
        document[-1].line = lineno + 1  # lineno points previous line
        return True


# 4.5 Fenced code blocks
class FencedCodeBlockProcessor(PatternBlockProcessor):
    paragraph_interruptable = True
    pattern = re.compile('^( {0,3})(`{3,}|~{3,})([^`]*)$')

    def run(self, document, reader):
        def unindent(text, length):
            return re.sub('^ {0,%d}' % length, '', text)

        source, lineno = reader.get_source_and_line()

        code = ''
        indent, marker, language = self.pattern.match(reader.readline()).groups()
        closing_pattern = re.compile('^ {0,3}%s+\s*$' % marker)
        for line in reader:
            if closing_pattern.match(line):
                break
            else:
                code += unindent(line, len(indent))

        document += nodes.literal_block(code, code)
        document[-1].source = source
        document[-1].line = lineno + 1  # lineno points previous line
        if language and language.strip():
            language = entitytrans._unescape(language.strip())
            document[-1]['language'] = language
            document[-1]['classes'].append('language-%s' % language.split()[0])

        return True


# 4.3 Setext headings
# 4.8 Paragraphs
class ParagraphProcessor(BlockProcessor):
    setext_heading_underline = re.compile('^ {0,3}(=+|-+)\s*$')

    def match(self, reader, **kwargs):
        return True

    def run(self, document, reader):
        source, lineno = reader.get_source_and_line()
        node = self.read(reader, setext_heading_allowed=True)
        if isinstance(node, nodes.section):
            node[0].source = source
            node[0].line = lineno + 1  # lineno points previous line
        else:
            text = self.read(LazyLineReader(reader), node.rawsource).rawsource.strip()
            node = nodes.paragraph(text, text)
            node.source = source
            node.line = lineno + 1  # lineno points previous line

        document += node
        return True

    def read(self, reader, text='', setext_heading_allowed=False):
        def get_depth(line):
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


# 4.9 Blank lines
class BlankLineProcessor(PatternBlockProcessor):
    paragraph_interruptable = True
    pattern = re.compile('^\s*$')

    def run(self, document, reader):
        reader.readline()  # skip the line
        document += addnodes.blankline()
        return True
