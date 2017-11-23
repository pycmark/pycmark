# -*- coding: utf-8 -*-
"""
    pycmark.blockparser.container_processors
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Container processor classes for BlockParser.

    :copyright: Copyright 2017 by Takeshi KOMIYA
    :license: BSD, see LICENSE for details.
"""

import re
import typing
from docutils import nodes
from pycmark import addnodes
from pycmark.blockparser import BlockProcessor, PatternBlockProcessor
from pycmark.readers import BlockQuoteReader, ListItemReader

if typing.TYPE_CHECKING:
    from typing import Any  # NOQA
    from pycmark.readers import LineReader  # NOQA


# 5.1 Block quotes
class BlockQuoteProcessor(PatternBlockProcessor):
    paragraph_interruptable = True
    pattern = re.compile('^ {0,3}> ?')

    def run(self, document, reader):
        quote = nodes.block_quote()
        quote.source, quote.line = reader.get_source_and_line()
        quote.line += 1
        self.parser.parse(BlockQuoteReader(reader), quote)
        document += quote
        return True


class ListProcessor(BlockProcessor):
    first_item_pattern = re.compile('^$')
    next_item_pattern = re.compile('^$')

    def match(self, reader, in_list=False, **kwargs):
        # type: (LineReader, bool, Any) -> bool
        if in_list:
            return bool(self.next_item_pattern.match(reader.next_line))
        else:
            return bool(self.first_item_pattern.match(reader.next_line))

    def run(self, document, reader):
        # type: (nodes.Node, LineReader) -> bool
        marker = self.first_item_pattern.match(reader.next_line).group(2)
        list_node = self.create_list_node(marker)
        while True:
            list_item = nodes.list_item()
            indent = self.get_indent_depth(reader)
            self.parser.parse(ListItemReader(reader, indent, self), list_item)
            list_node += list_item

            if not self.is_next_list_item(reader, marker):
                break

        # blank lines at tail of last list_item should be recognized as a part of outside of list
        for node in reversed(list_node[-1]):
            if isinstance(node, addnodes.blankline):
                list_node[-1].remove(node)
                document += node
            else:
                break
        document += list_node
        return True

    def get_indent_depth(self, reader):
        # type: (LineReader) -> int
        indent, marker, following, content = self.next_item_pattern.match(reader.next_line).groups()
        if 1 <= len(following) <= 4 and content.strip():
            # the case a list_item having small indents
            return len(indent) + len(marker) + len(following)
        else:
            # the case a list_item having much indents (>= 4) or nothing (the line is marker only)
            return len(indent) + len(marker) + 1

    def is_next_list_item(self, reader, marker):
        # type: (LineReader, str) -> bool
        """Checks the next line is a next list item or not."""
        try:
            matched = self.next_item_pattern.match(reader.next_line)
            if not matched:
                return False
            elif not self.is_same_marker_type(marker, matched.group(2)):
                return False
            else:
                return True
        except IOError:
            return False

    def create_list_node(self, marker):
        # type: (str) -> nodes.Node
        raise NotImplementedError

    def is_same_marker_type(self, marker, candidate):
        # type: (str, str) -> bool
        raise NotImplementedError


# 5.2 List items; bullet lists
class BulletListProcessor(ListProcessor):
    paragraph_interruptable = False
    first_item_pattern = re.compile('^( {0,3})([-+*])( +|$)(.*)')
    next_item_pattern = re.compile('^( *)([-+*])( +|$)(.*)')

    def create_list_node(self, marker):
        # type: (str) -> nodes.Node
        return nodes.bullet_list(bullet=marker)

    def is_same_marker_type(self, marker, candidate):
        # type: (str, str) -> bool
        return marker == candidate


class NonEmptyBulletListProcessor(ListProcessor):
    # The non-empty bullet list can interrupt paragraphs
    paragraph_interruptable = True
    first_item_pattern = re.compile('^( {0,3})([-+*])( +)(?=\S)(.*)')


# 5.2 List items; ordered lists
class OrderedListProcessor(ListProcessor):
    paragraph_interruptable = False
    first_item_pattern = re.compile('^( {0,3})(\d{1,9}[.)])( +|$)(.*)')
    next_item_pattern = re.compile('^( *)(\d{1,9}[.)])( +|$)(.*)')

    def create_list_node(self, marker):
        # type: (str) -> nodes.Node
        return nodes.enumerated_list(start=int(marker[:-1]), enumtype="arabic", suffix=marker[-1])

    def is_same_marker_type(self, marker, candidate):
        # type: (str, str) -> bool
        return marker[-1] == candidate[-1]


class OneBasedOrderedListProcessor(OrderedListProcessor):
    # The ordered list starts with 1 can interrupt paragraphs
    paragraph_interruptable = True
    first_item_pattern = re.compile('^( {0,3})(1[.)])( +)(?=\S)(.*)')
