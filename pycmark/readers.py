# -*- coding: utf-8 -*-
"""
    pycmark.readers
    ~~~~~~~~~~~~~~~

    CommonMark reader classes.

    :copyright: Copyright 2017 by Takeshi KOMIYA
    :license: BSD, see LICENSE for details.
"""

import typing


if typing.TYPE_CHECKING:
    from typing import Any, List, Tuple, Union  # NOQA


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
