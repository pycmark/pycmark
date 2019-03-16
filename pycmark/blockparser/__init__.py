"""
    pycmark.blockparser
    ~~~~~~~~~~~~~~~~~~~

    A parser for block elements.

    :copyright: Copyright 2017-2019 by Takeshi KOMIYA
    :license: BSD, see LICENSE for details.
"""

import re
from typing import List

from docutils.nodes import Element

from pycmark.readers import LineReader


class BlockParser:
    """A parser for block elements."""
    def __init__(self) -> None:
        self.processors: List["BlockProcessor"] = []

    def add_processor(self, processor: "BlockProcessor") -> None:
        """Add a block processor to parser."""
        self.processors.append(processor)

    def parse(self, reader: LineReader, document: Element) -> None:
        """Parses a text and build document."""
        while not reader.eof():
            for processor in self.processors:
                if processor.match(reader):
                    if processor.run(document, reader):
                        break
            else:
                raise RuntimeError('Failed to parse')

    def is_interrupted(self, reader: LineReader) -> bool:
        for processor in self.processors:
            if processor.paragraph_interruptable and processor.match(reader):
                return True

        return False


class BlockProcessor:
    #: This processor can interrupt a paragraph
    paragraph_interruptable = False

    def __init__(self, parser: BlockParser) -> None:
        self.parser = parser

    def match(self, reader: LineReader, **kwargs) -> bool:
        return False

    def run(self, document: Element, reader: LineReader) -> bool:
        return False


class PatternBlockProcessor(BlockProcessor):
    pattern = re.compile('^$')

    def match(self, reader: LineReader, **kwargs) -> bool:
        return bool(self.pattern.match(reader.next_line))
