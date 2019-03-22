"""
    pycmark.inlineparser
    ~~~~~~~~~~~~~~~~~~~~

    A parser for inline elements.

    :copyright: Copyright 2017-2019 by Takeshi KOMIYA
    :license: Apache License 2.0, see LICENSE for details.
"""

import re
from functools import wraps
from typing import Any, Callable, List, Tuple, cast

from docutils.nodes import Element, Text, TextElement

from pycmark.addnodes import SparseText
from pycmark.readers import TextReader


class InlineParser:
    """A parser for inline elements."""

    def __init__(self) -> None:
        self.processors: List[Tuple[int, "InlineProcessor"]] = []

    def add_processor(self, processor: "InlineProcessor") -> None:
        """Add a inline processor to parser."""
        self.processors.append((processor.priority, processor))
        self.processors.sort()

    def parse(self, document: TextElement) -> TextElement:
        """Parses a text and build TextElement."""
        if len(document) == 0:
            return document

        reader = TextReader(cast(Text, document.pop()))
        while reader.remain:
            for _, processor in self.processors:
                if processor.match(reader):
                    if processor.run(reader, document) is True:
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
    #: priority of the processor (1-999)
    priority = 500

    def __init__(self, parser: InlineParser) -> None:
        self.parser = parser

    def match(self, reader: TextReader) -> bool:
        return False

    def run(self, reader: TextReader, document: TextElement) -> bool:
        return False

    def __lt__(self, other: Any) -> bool:
        return self.__class__.__name__ < other.__class__.__name__


class PatternInlineProcessor(InlineProcessor):
    pattern = re.compile('^$')

    def match(self, reader: TextReader, **kwargs) -> bool:
        return bool(self.pattern.match(reader.remain))


class UnmatchedTokenError(Exception):
    pass


def backtrack_onerror(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(self, reader: TextReader, document: Element, **kwargs) -> bool:
        new_reader = TextReader(reader.subject, reader.position)
        try:
            ret = func(self, new_reader, document, **kwargs)
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
