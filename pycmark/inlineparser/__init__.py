# -*- coding: utf-8 -*-
"""
    pycmark.inlineparser
    ~~~~~~~~~~~~~~~~~~~~

    A parser for inline elements.

    :copyright: Copyright 2017 by Takeshi KOMIYA
    :license: BSD, see LICENSE for details.
"""

import re
from docutils import nodes
from functools import wraps
from pycmark.addnodes import SparseText
from pycmark.readers import TextReader


class InlineParser(object):
    """A parser for inline elements."""

    def __init__(self):
        self.processors = []

    def add_processor(self, processor):
        # type: (InlineProcessor) -> None
        """Add a inline processor to parser."""
        self.processors.append(processor)

    def parse(self, document):
        """Parses a text and build TextElement."""
        if len(document) == 0:
            return

        reader = TextReader(document.pop())
        while reader.remain:
            for processor in self.processors:
                if processor.match(reader):
                    if processor.run(document, reader) is True:
                        break
            else:
                if len(document) == 0 or not isinstance(document[-1], SparseText):
                    document += SparseText(reader.subject, reader.position, reader.position + 1)
                else:
                    document[-1].spread(end=1)

                if reader.remain[0] == '\\':  # escaped
                    document[-1].spread(end=1)
                    reader.step(2)
                else:
                    reader.step(1)

        return document


class InlineProcessor(object):
    def __init__(self, parser):
        self.parser = parser

    def match(self, reader):
        return False

    def run(self, document, reader):
        return False


class PatternInlineProcessor(InlineProcessor):
    pattern = re.compile('^$')

    def match(self, reader, **kwargs):
        return bool(self.pattern.match(reader.remain))


class UnmatchedTokenError(Exception):
    pass


def backtrack_onerror(func):
    @wraps(func)
    def wrapper(self, document, reader):
        new_reader = TextReader(reader.subject, reader.position)
        try:
            ret = func(self, document, new_reader)
            if ret:
                reader.position = new_reader.position
            return ret
        except UnmatchedTokenError as exc:
            text = exc.args[0]
            document += nodes.Text(text)
            reader.step(len(text))
            return True
        except Exception:
            return False

    return wrapper