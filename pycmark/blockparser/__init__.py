# -*- coding: utf-8 -*-
"""
    pycmark.blockparser
    ~~~~~~~~~~~~~~~~~~~

    A parser for block elements.

    :copyright: Copyright 2017 by Takeshi KOMIYA
    :license: BSD, see LICENSE for details.
"""

import re


class BlockParser(object):
    """A parser for block elements."""
    def __init__(self):
        self.processors = []

    def add_processor(self, processor):
        # type: (BlockProcessor) -> None
        """Add a block processor to parser."""
        self.processors.append(processor)

    def parse(self, reader, document):
        """Parses a text and build document."""
        while not reader.eof():
            for processor in self.processors:
                if processor.match(reader):
                    if processor.run(document, reader):
                        break
            else:
                raise RuntimeError('Failed to parse')


class BlockProcessor(object):
    def __init__(self, parser):
        self.parser = parser

    def match(self, reader, **kwargs):
        return False

    def run(self, document, reader):
        return False


class PatternBlockProcessor(BlockProcessor):
    pattern = re.compile('^$')

    def match(self, reader, **kwargs):
        return bool(self.pattern.match(reader.next_line))
