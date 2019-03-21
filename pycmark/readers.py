"""
    pycmark.readers
    ~~~~~~~~~~~~~~~

    CommonMark reader classes.

    :copyright: Copyright 2017-2019 by Takeshi KOMIYA
    :license: Apache License 2.0, see LICENSE for details.
"""

import re
from typing import List, Match, NamedTuple, Pattern, TYPE_CHECKING, Union

from docutils.nodes import Node

from pycmark.utils import expand_leading_tabs

if TYPE_CHECKING:
    from pycmark.inlineparser.list_processors import ListProcessor


SourceInfoBase = NamedTuple('SourceInfo', [('source', str), ('lineno', int)])


class SourceInfo(SourceInfoBase):
    def set_source_info(self, node: Node) -> None:
        node.source = self.source
        node.line = self.lineno


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

    def get_source_and_line(self, incr: int = 0) -> SourceInfo:
        """Returns source filename and current line number."""
        return SourceInfo(self.source, self.lineno + incr)

    def fetch(self, relative: int = 0, **kwargs) -> str:
        """Returns an arbitrary line without moving the current line."""
        try:
            line = self.lines[self.lineno + relative - 1]
            return expand_leading_tabs(line, kwargs.get('markers', []))
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

    def get_source_and_line(self, incr: int = 0) -> SourceInfo:
        return self.reader.get_source_and_line(incr)

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
        kwargs.setdefault('markers', []).insert(0, '>')
        line = self.reader.fetch(relative, **kwargs)
        if self.pattern.match(line):
            return self.pattern.sub('', line)
        elif kwargs.get('lazy') and line.lstrip():
            return line
        else:
            raise IOError


class IndentedCodeBlockReader(LineReaderDecorator):
    """A reader for indented code blocks."""

    def fetch(self, relative: int = 0, **kwargs) -> str:
        """Returns a line without indents."""
        line = self.reader.fetch(relative, **kwargs)
        if line.startswith('    '):
            return line[4:]
        elif line.strip() == '':
            return '\n'
        else:
            raise IOError


class FencedCodeBlockReader(LineReaderDecorator):
    """A reader for fenced code blocks."""

    def __init__(self, reader: LineReader, indent: int, marker: str) -> None:
        super().__init__(reader)
        self.closing_pattern = re.compile(r'^ {0,3}%s+\s*$' % marker)
        self.indent_pattern = re.compile(r'^ {0,%d}' % indent)

    def fetch(self, relative: int = 0, **kwargs) -> str:
        """Returns a line without indents."""
        line = self.reader.fetch(relative, **kwargs)
        if self.closing_pattern.match(line):
            self.reader.step()
            raise IOError
        else:
            return self.indent_pattern.sub('', line)


class LazyLineReader(LineReaderDecorator):
    """A reader supports laziness paragraphs."""

    def fetch(self, relative: int = 0, **kwargs) -> str:
        kwargs['lazy'] = True
        return self.reader.fetch(relative, **kwargs)

    def eof(self, **kwargs) -> bool:
        kwargs['lazy'] = True
        return self.reader.eof(**kwargs)


class ListItemReader(LineReaderDecorator):
    """A reader for list items."""

    def __init__(self, reader: LineReader, markers: str, processor: "ListProcessor") -> None:
        self.markers = markers
        self.marker: str = None
        self.indent: int = None
        self.indent_pattern: Pattern = None
        self.beginning_lineno = reader.lineno + 1
        self.processor = processor
        super().__init__(reader)

        self.recognize_list_item()

    def recognize_list_item(self) -> None:
        first_line = self.reader.fetch(1, markers=[self.markers])
        matched = re.match(r'^(\s*(%s)\s*)(.*)' % self.markers, first_line)
        if matched is None:
            raise IOError
        else:
            self.marker = matched.group(2)

            prefix = matched.group(1)
            spaces_after_marker = len(prefix) - len(prefix.rstrip())
            remain = matched.group(3)
            if 1 <= spaces_after_marker <= 4 and len(remain) > 0:
                # the case a list_item having small indents
                indent = len(prefix)
            else:
                # the case a list_item having much indents (>= 4) or nothing (the line is marker only)
                indent = len(prefix.rstrip()) + 1

            self.set_indent(indent)

    def set_indent(self, indent: int) -> None:
        self.indent = indent
        self.indent_pattern = re.compile('^ {%d}' % indent)

    def fetch(self, relative: int = 0, **kwargs) -> str:
        if kwargs.get('lazy'):
            reader: LineReader = LazyLineReader(self.reader)
        else:
            reader = self.reader

        if self.is_beginning_line(relative):
            # skip over a list marker on the beginning line
            kwargs.setdefault('markers', []).insert(0, self.markers)

        line = self.reader.fetch(relative, **kwargs)
        if self.is_beginning_line(relative):
            # remove a list marker and indents when the beginning line
            return line[self.indent:]
        elif self.indent_pattern.match(line):
            return self.indent_pattern.sub('', line)
        elif line.strip() == '':
            return '\n'
        elif self.processor.match(reader, in_list=True):
            # next list item found
            raise IOError
        elif kwargs.get('lazy') and line.lstrip():
            return line
        else:
            raise IOError

    def is_beginning_line(self, relative: int) -> bool:
        return self.lineno + relative == self.beginning_lineno


class TextReader:
    """A character based reader."""

    def __init__(self, text: str, position: int = 0) -> None:
        self.subject = text
        self.position = position

    def __getitem__(self, key: Union[int, slice]) -> str:
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
