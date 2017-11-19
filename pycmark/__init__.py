# -*- coding: utf-8 -*-
"""
    pycmark
    ~~~~~~~

    CommonMark parser for docutils.

    :copyright: Copyright 2017 by Takeshi KOMIYA
    :license: BSD, see LICENSE for details.
"""

from docutils.parsers import Parser
from pycmark.readers import LineReader
from pycmark.blockparser import BlockParser
from pycmark.blockparser.std_processors import (
    ThematicBreakProcessor
)


class CommonMarkParser(Parser):
    """CommonMark parser for docutils."""

    supported = ('markdown', 'commonmark', 'md')

    def get_block_processors(self):
        """Returns block processors. Overrided by subclasses."""
        return [
            ThematicBreakProcessor,
        ]

    def create_parser(self):
        """Creates a block parser and returns it.

        Internally, ``get_block_processors()`` is called to create a parser.
        So you can change the processors by subclassing.
        """
        parser = BlockParser()
        for processor in self.get_block_processors():
            parser.add_processor(processor(parser))
        return parser

    def parse(self, inputtext, document):
        """Parses a text and build document."""
        reader = LineReader(inputtext.splitlines(True))
        parser = self.create_parser()
        parser.parse(reader, document)
