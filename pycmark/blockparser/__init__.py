"""
    pycmark.blockparser
    ~~~~~~~~~~~~~~~~~~~

    A parser for block elements.

    :copyright: Copyright 2017-2019 by Takeshi KOMIYA
    :license: Apache License 2.0, see LICENSE for details.
"""

import re
from typing import Any, List, Tuple

from docutils.nodes import Element

from pycmark.readers import LineReader


class BlockParser:
    """A parser for block elements."""
    def __init__(self) -> None:
        self.processors: List[Tuple[int, "BlockProcessor"]] = []

    def add_processor(self, processor: "BlockProcessor") -> None:
        """Add a block processor to parser."""
        self.processors.append((processor.priority, processor))
        self.processors.sort()

    def parse(self, reader: LineReader, document: Element) -> None:
        """Parses a text and build document."""
        while not reader.eof():
            for _, processor in self.processors:
                if processor.match(reader):
                    if processor.run(reader, document):
                        break
            else:
                raise RuntimeError('Failed to parse')

    def is_interrupted(self, reader: LineReader) -> bool:
        try:
            for _, processor in self.processors:
                if processor.paragraph_interruptable and processor.match(reader):
                    return True
        except IOError:
            pass

        return False


class BlockProcessor:
    #: priority of the processor (1-999)
    priority = 500

    #: This processor can interrupt a paragraph
    paragraph_interruptable = False

    def __init__(self, parser: BlockParser) -> None:
        self.parser = parser

    def match(self, reader: LineReader, **kwargs) -> bool:
        return False

    def run(self, reader: LineReader, document: Element) -> bool:
        return False

    def __lt__(self, other: Any) -> bool:
        return self.__class__.__name__ < other.__class__.__name__


class PatternBlockProcessor(BlockProcessor):
    pattern = re.compile('^$')

    def match(self, reader: LineReader, **kwargs) -> bool:
        return bool(self.pattern.match(reader.next_line))
