# -*- coding: utf-8 -*-
"""
    pycmark.readers
    ~~~~~~~~~~~~~~~

    CommonMark reader classes.

    :copyright: Copyright 2017 by Takeshi KOMIYA
    :license: BSD, see LICENSE for details.
"""

import re
from typing import List, Match, Pattern, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from pycmark.inlineparser.list_processors import ListProcessor


class LineReader:
    """A line based reader for text."""

    def __init__(self, lines: List[str], source: str = None, lineno: int = 0) -> None:
        self.lines = lines
        self.source = source
        self.lineno = lineno  # lineno is 1 origin

    def __getitem__(self, key: int) -> str:
        """Returns arbitrary line or lines."""
        return self.lines[key]

    def __iter__(self) -> "LineReader":
        """Returns itself as a iterator."""
        return self

    def __next__(self) -> str:
        """Returns a next line from buffer. same as :meth:`readline()`."""
        try:
            return self.readline()
        except IOError:
            raise StopIteration

    def get_source_and_line(self, lineno: int = None) -> Tuple[str, int]:
        """Returns source filename and current line number."""
        if lineno is not None:
            return self.source, lineno
        else:
            return self.source, self.lineno

    def fetch(self, relative: int = 0, **kwargs) -> str:
        """Returns an arbitrary line without moving the current line."""
        try:
            return self.lines[self.lineno + relative - 1]
        except IndexError:
            raise IOError

    def readline(self, **kwargs) -> str:
        """Reads a next line from buffer and steps the current line to next."""
        try:
            line = self.fetch(1, **kwargs)
            self.step()
            return line
        except IndexError:
            raise IOError

    def eof(self, **kwargs) -> bool:
        """Returns it reaches the EOF (end of file) or not."""
        return len(self.lines) == self.lineno

    @property
    def current_line(self) -> str:
        """Returns the current line."""
        return self.fetch(0)

    @property
    def next_line(self) -> str:
        """Returns the next line."""
        return self.fetch(1)

    def step(self, n: int = 1) -> None:
        """Steps the current line to next."""
        self.lineno += n


class LineReaderDecorator(LineReader):
    """A base class of LineReader decorators."""

    def __init__(self, reader: LineReader) -> None:
        self.reader = reader

    def __getitem__(self, key: int) -> str:
        return self.reader[key]

    @property
    def lineno(self) -> int:  # type: ignore
        return self.reader.lineno

    def get_source_and_line(self, lineno: int = None) -> Tuple[str, int]:
        return self.reader.get_source_and_line(lineno)

    def fetch(self, relative: int = 0, **kwargs) -> str:
        raise NotImplementedError

    def eof(self, **kwargs) -> bool:
        if self.reader.eof(**kwargs):
            return True
        else:
            try:
                self.fetch(1, **kwargs)
                return False
            except IOError:
                return True

    def step(self, n: int = 1) -> None:
        self.reader.step(n)


class BlockQuoteReader(LineReaderDecorator):
    """A reader for block quotes."""
    pattern = re.compile('^ {0,3}> ?')

    def fetch(self, relative: int = 0, **kwargs) -> str:
        """Returns a line without quote markers."""
        line = self.reader.fetch(relative, lazy=kwargs.get('lazy'))
        if self.pattern.match(line):
            return self.pattern.sub('', line)
        elif kwargs.get('lazy') and line.strip():
            return line
        else:
            raise IOError


class LazyLineReader(LineReaderDecorator):
    """A reader supports laziness paragraphs."""

    def fetch(self, relative: int = 0, **kwargs) -> str:
        return self.reader.fetch(relative, lazy=True)

    def eof(self, **kwargs) -> bool:
        return self.reader.eof(lazy=True)


class ListItemReader(LineReaderDecorator):
    """A reader for list items."""

    def __init__(self, reader: LineReader, indent: int, processor: "ListProcessor") -> None:
        self.indent = indent
        self.pattern = re.compile('^ {%d}' % indent)
        self.begining_lineno = reader.lineno + 1
        self.processor = processor
        super().__init__(reader)

    def fetch(self, relative: int = 0, **kwargs) -> str:
        if kwargs.get('lazy'):
            reader: LineReader = LazyLineReader(self.reader)
        else:
            reader = self.reader

        line = self.reader.fetch(relative, **kwargs)
        if self.lineno + relative == self.begining_lineno:
            # remove a list marker and indents when the beginning line
            return line[self.indent:]
        elif self.pattern.match(line):
            return self.pattern.sub('', line)
        elif self.processor.match(reader, in_list=True):
            # next list item found
            raise IOError
        elif line.strip() == '':
            return '\n'
        elif kwargs.get('lazy') and line.strip():
            return line
        else:
            raise IOError


class TextReader:
    """A character based reader."""

    def __init__(self, text: str, position: int = 0) -> None:
        self.subject = text
        self.position = position

    def __getitem__(self, key: int) -> str:
        return self.subject[key]

    @property
    def remain(self) -> str:
        return self.subject[self.position:]

    def step(self, n: int = 1) -> None:
        self.position += n

    def consume(self, pattern: Pattern) -> Match:
        matched = pattern.match(self.remain)
        if matched:
            self.step(len(matched.group(0)))

        return matched
