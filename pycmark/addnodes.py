"""
    pycmark.addnodes
    ~~~~~~~~~~~~~~~~

    Additional docutils nodes for pycmark.

    :copyright: Copyright 2017-2019 by Takeshi KOMIYA
    :license: Apache License 2.0, see LICENSE for details.
"""

from docutils.nodes import Element, Invisible


class blankline(Element, Invisible):
    """A node represents a blank line."""
    pass


class linebreak(Element, Invisible):
    """A node represents a hard linebreak."""
    pass


class emphasis(Element):
    """A node reprents a marker for emphasis and strong."""

    def __str__(self) -> str:
        length = self['curr_length']
        return self['marker'][:length]

    def astext(self) -> str:
        return str(self)

    def shrink(self, n: int) -> None:
        if self['curr_length'] == n:
            self.parent.remove(self)
        else:
            self['curr_length'] -= n


class bracket(Element):
    """A node reprenents a square bracket (both opening and closing)."""

    def __str__(self) -> str:
        return self['marker']

    def astext(self) -> str:
        return str(self)


class SparseText(Element):
    """A node represents a text."""

    def __init__(self, text: str, start: int, end: int) -> None:
        super().__init__()
        self['text'] = text
        self.start = start
        self.end = end

    def __str__(self) -> str:
        return self['text'][self.start:self.end]

    def astext(self) -> str:
        return str(self)

    def spread(self, end: int = 1, start: int = 0) -> None:
        self.start -= start
        self.end += end
