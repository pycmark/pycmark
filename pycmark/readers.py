# -*- coding: utf-8 -*-
"""
    pycmark.readers
    ~~~~~~~~~~~~~~~

    CommonMark reader classes.

    :copyright: Copyright 2017 by Takeshi KOMIYA
    :license: BSD, see LICENSE for details.
"""

import re
import typing

if typing.TYPE_CHECKING:
    from typing import Any, List, Tuple, Union  # NOQA
    from pycmark.blockparser.list_processors import ListProcessor  # NOQA


class LineReader(object):
    """A line based reader for text."""

    def __init__(self, lines, source=None, lineno=0):
        # type: (List[str], str, int) -> None
        self.lines = lines
        self.source = source
        self.lineno = lineno  # lineno is 1 origin

    def __getitem__(self, key):
        # type: (Union[int, slice]) -> str
        """Returns arbitrary line or lines."""
        return self.lines[key]

    def __iter__(self):
        # type: () -> LineReader
        """Returns itself as a iterator."""
        return self

    def __next__(self):
        # type: () -> str
        """Returns a next line from buffer. same as :meth:`readline()`."""
        try:
            return self.readline()
        except IOError:
            raise StopIteration

    def get_source_and_line(self, lineno=None):
        # type: (int) -> Tuple[str, int]
        """Returns source filename and current line number."""
        if lineno is not None:
            return self.source, lineno
        else:
            return self.source, self.lineno

    def fetch(self, relative=0, **kwargs):
        # type: (int, Any) -> str
        """Returns an arbitrary line without moving the current line."""
        try:
            return self.lines[self.lineno + relative - 1]
        except IndexError:
            raise IOError

    def readline(self, **kwargs):
        # type: (Any) -> str
        """Reads a next line from buffer and steps the current line to next."""
        try:
            line = self.fetch(1, **kwargs)
            self.step()
            return line
        except IndexError:
            raise IOError

    def eof(self, **kwargs):
        # type: (Any) -> bool
        """Returns it reaches the EOF (end of file) or not."""
        return len(self.lines) == self.lineno

    @property
    def current_line(self):
        # type: () -> str
        """Returns the current line."""
        return self.fetch(0)

    @property
    def next_line(self):
        # type: () -> str
        """Returns the next line."""
        return self.fetch(1)

    def step(self, n=1):
        # type: (int) -> None
        """Steps the current line to next."""
        self.lineno += n


class LineReaderDecorator(LineReader):
    """A base class of LineReader decorators."""

    def __init__(self, reader):
        # type: (LineReader) -> None
        self.reader = reader

    def __getitem__(self, key):
        # type: (Union[int, slice]) -> str
        return self.reader[key]

    @property
    def lineno(self):  # type: ignore
        # type: () -> int
        return self.reader.lineno

    def get_source_and_line(self, lineno=None):
        # type: (int) -> Tuple[str, int]
        return self.reader.get_source_and_line(lineno)

    def fetch(self, relative=0, **kwargs):
        # type: (int, Any) -> str
        raise NotImplementedError

    def eof(self, **kwargs):
        # type: (Any) -> bool
        if self.reader.eof(**kwargs):
            return True
        else:
            try:
                self.fetch(1, **kwargs)
                return False
            except IOError:
                return True

    def step(self, n=1):
        # type: (int) -> None
        self.reader.step(n)


class BlockQuoteReader(LineReaderDecorator):
    """A reader for block quotes."""
    pattern = re.compile('^ {0,3}> ?')

    def fetch(self, relative=0, **kwargs):
        # type: (int, Any) -> str
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

    def fetch(self, relative=0):
        return self.reader.fetch(relative, lazy=True)

    def eof(self, **kwargs):
        # type: (Any) -> bool
        return self.reader.eof(lazy=True)


class ListItemReader(LineReaderDecorator):
    """A reader for list items."""

    def __init__(self, reader, indent, processor):
        # type: (LineReader, int, ListProcessor) -> None
        self.indent = indent
        self.pattern = re.compile('^ {%d}' % indent)
        self.begining_lineno = reader.lineno + 1
        self.processor = processor
        super(ListItemReader, self).__init__(reader)

    def fetch(self, relative=0, **kwargs):
        # type: (int, Any) -> str
        if kwargs.get('lazy'):
            reader = LazyLineReader(self.reader)  # type: LineReader
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


class TextReader(object):
    """A character based reader."""

    def __init__(self, text, position=0):
        # type: (str, int) -> None
        self.subject = text
        self.position = position

    def __getitem__(self, key):
        # type: (int) -> str
        return self.subject[key]

    @property
    def remain(self):
        # type: () -> str
        return self.subject[self.position:]

    def step(self, n=1):
        # type: (int) -> None
        self.position += n
