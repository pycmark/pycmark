# -*- coding: utf-8 -*-
"""
    pycmark.addnodes
    ~~~~~~~~~~~~~~~~

    Additiona docutils nodes for pycmark.

    :copyright: Copyright 2017 by Takeshi KOMIYA
    :license: BSD, see LICENSE for details.
"""

from docutils import nodes


class blankline(nodes.Element, nodes.Invisible):
    """A node represents a blank line."""
    pass
