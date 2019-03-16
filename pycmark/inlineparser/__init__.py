"""
    pycmark.inlineparser
    ~~~~~~~~~~~~~~~~~~~~

    A parser for inline elements.

    :copyright: Copyright 2017-2019 by Takeshi KOMIYA
    :license: BSD, see LICENSE for details.
"""

import re
from functools import wraps
from typing import Callable, List, cast

from docutils.nodes import Element, Text, TextElement

from pycmark.addnodes import SparseText
from pycmark.readers import TextReader


class InlineParser:
    """A parser for inline elements."""

    def __init__(self) -> None:
        self.processors: List["InlineProcessor"] = []

    def add_processor(self, processor: "InlineProcessor") -> None:
        """Add a inline processor to parser."""
        self.processors.append(processor)

    def parse(self, document: TextElement) -> TextElement:
        """Parses a text and build TextElement."""
        if len(document) == 0:
            return document

        reader = TextReader(cast(Text, document.pop()))
        while reader.remain:
            for processor in self.processors:
                if processor.match(reader):
                    if processor.run(document, reader) is True:
                        break
            else:
                if len(document) > 0 and isinstance(document[-1], SparseText):
                    tail = document[-1]
                    tail.spread(end=1)
                else:
                    tail = SparseText(reader.subject, reader.position, reader.position + 1)
                    document += tail

                if reader.remain[0] == '\\':  # escaped
                    tail.spread(end=1)
                    reader.step(2)
                else:
                    reader.step(1)

        return document


class InlineProcessor:
    def __init__(self, parser: InlineParser) -> None:
        self.parser = parser

    def match(self, reader: TextReader) -> bool:
        return False

    def run(self, document: TextElement, reader: TextReader) -> bool:
        return False


class PatternInlineProcessor(InlineProcessor):
    pattern = re.compile('^$')

    def match(self, reader: TextReader, **kwargs) -> bool:
        return bool(self.pattern.match(reader.remain))


class UnmatchedTokenError(Exception):
    pass


class ParseError(Exception):
    pass


def backtrack_onerror(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(self, document: Element, reader: TextReader, **kwargs) -> bool:
        new_reader = TextReader(reader.subject, reader.position)
        try:
            ret = func(self, document, new_reader, **kwargs)
            if ret:
                reader.position = new_reader.position
            return ret
        except UnmatchedTokenError as exc:
            text = exc.args[0]
            document += Text(text)
            reader.step(len(text))
            return True
        except Exception:
            return False

    return wrapper
