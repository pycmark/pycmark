# -*- coding: utf-8 -*-
"""
    pycmark.addnodes
    ~~~~~~~~~~~~~~~~

    Additiona docutils nodes for pycmark.

    :copyright: Copyright 2017 by Takeshi KOMIYA
    :license: BSD, see LICENSE for details.
"""

from docutils import nodes
from docutils.nodes import Element, Invisible


class blankline(Element, Invisible):
    """A node represents a blank line."""
    pass


class emphasis(Element):
    """A node reprents a marker for emphasis and strong."""

    def __str__(self):
        length = self['curr_length']
        return self['marker'][:length]

    def astext(self):
        return str(self)

    def shrink(self, n):
        if self['curr_length'] == n:
            self.parent.remove(self)
        else:
            self['curr_length'] -= n


class bracket(Element):
    """A node reprenents a square bracket (both opening and closing)."""

    def __str__(self):
        return self['marker']

    def astext(self):
        return str(self)


class SparseText(Element):
    """A node represents a text."""

    def __init__(self, text, start, end):
        nodes.Element.__init__(self)
        self['text'] = text
        self.start = start
        self.end = end

    def __str__(self):
        return self['text'][self.start:self.end]

    def astext(self):
        return str(self)

    def spread(self, end=1, start=0):
        self.start -= start
        self.end += end
