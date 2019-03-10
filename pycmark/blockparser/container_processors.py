# -*- coding: utf-8 -*-
"""
    pycmark.blockparser.container_processors
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Container processor classes for BlockParser.

    :copyright: Copyright 2017 by Takeshi KOMIYA
    :license: BSD, see LICENSE for details.
"""

import re
from docutils import nodes
from docutils.nodes import Element
from pycmark import addnodes
from pycmark.blockparser import BlockProcessor, PatternBlockProcessor
from pycmark.readers import BlockQuoteReader, LineReader, ListItemReader
from typing import List, cast


# 5.1 Block quotes
class BlockQuoteProcessor(PatternBlockProcessor):
    paragraph_interruptable = True
    pattern = re.compile('^ {0,3}> ?')

    def run(self, document, reader):
        quote = nodes.block_quote()
        quote.source, quote.line = reader.get_source_and_line()
        quote.line += 1
        document += quote
        self.parser.parse(BlockQuoteReader(reader), quote)
        return True


class ListProcessor(BlockProcessor):
    first_item_pattern = re.compile('^$')
    next_item_pattern = re.compile('^$')

    def match(self, reader: LineReader, in_list: bool = False, **kwargs) -> bool:
        if in_list:
            return bool(self.next_item_pattern.match(reader.next_line))
        else:
            return bool(self.first_item_pattern.match(reader.next_line))

    def run(self, document: Element, reader: LineReader) -> bool:
        marker = self.first_item_pattern.match(reader.next_line).group(2)
        list_node = self.create_list_node(marker)
        document += list_node
        while True:
            list_item = nodes.list_item()
            list_node += list_item
            indent = self.get_indent_depth(reader)
            self.parser.parse(ListItemReader(reader, indent, self), list_item)

            if not self.is_next_list_item(reader, marker):
                break

        # blank lines at tail of last list_item should be recognized as a part of outside of list
        last_item = cast(List[Element], list_node[-1])
        for node in reversed(last_item):
            if isinstance(node, addnodes.blankline):
                last_item.remove(node)
                document += node
            else:
                break
        return True

    def get_indent_depth(self, reader: LineReader) -> int:
        indent, marker, following, content = self.next_item_pattern.match(reader.next_line).groups()
        if 1 <= len(following) <= 4 and content.strip():
            # the case a list_item having small indents
            return len(indent) + len(marker) + len(following)
        else:
            # the case a list_item having much indents (>= 4) or nothing (the line is marker only)
            return len(indent) + len(marker) + 1

    def is_next_list_item(self, reader: LineReader, marker: str) -> bool:
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

    def create_list_node(self, marker: str) -> Element:
        raise NotImplementedError

    def is_same_marker_type(self, marker: str, candidate: str) -> bool:
        raise NotImplementedError


# 5.2 List items; bullet lists
class BulletListProcessor(ListProcessor):
    paragraph_interruptable = False
    first_item_pattern = re.compile('^( {0,3})([-+*])( +|$)(.*)')
    next_item_pattern = re.compile('^( *)([-+*])( +|$)(.*)')

    def create_list_node(self, marker: str) -> Element:
        return nodes.bullet_list(bullet=marker)

    def is_next_list_item(self, reader: LineReader, marker: str) -> bool:
        try:
            pattern = re.compile(r'^(\s*\%s){2,}\s*$' % marker)
            if pattern.match(reader.next_line):
                # themantic break detected
                return False
            else:
                return super(BulletListProcessor, self).is_next_list_item(reader, marker)
        except IOError:
            return False

    def is_same_marker_type(self, marker: str, candidate: str) -> bool:
        return marker == candidate


class NonEmptyBulletListProcessor(ListProcessor):
    # The non-empty bullet list can interrupt paragraphs
    paragraph_interruptable = True
    first_item_pattern = re.compile(r'^( {0,3})([-+*])( +)(?=\S)(.*)')


# 5.2 List items; ordered lists
class OrderedListProcessor(ListProcessor):
    paragraph_interruptable = False
    first_item_pattern = re.compile(r'^( {0,3})(\d{1,9}[.)])( +|$)(.*)')
    next_item_pattern = re.compile(r'^( *)(\d{1,9}[.)])( +|$)(.*)')

    def create_list_node(self, marker: str) -> Element:
        return nodes.enumerated_list(start=int(marker[:-1]), enumtype="arabic", suffix=marker[-1])

    def is_same_marker_type(self, marker: str, candidate: str) -> bool:
        return marker[-1] == candidate[-1]


class OneBasedOrderedListProcessor(OrderedListProcessor):
    # The ordered list starts with 1 can interrupt paragraphs
    paragraph_interruptable = True
    first_item_pattern = re.compile(r'^( {0,3})(1[.)])( +)(?=\S)(.*)')
