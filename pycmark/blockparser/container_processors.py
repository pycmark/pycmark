"""
    pycmark.blockparser.container_processors
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Container processor classes for BlockParser.

    :copyright: Copyright 2017-2019 by Takeshi KOMIYA
    :license: Apache License 2.0, see LICENSE for details.
"""

import re
from typing import List, cast

from docutils import nodes
from docutils.nodes import Element

from pycmark import addnodes
from pycmark.blockparser import BlockProcessor, PatternBlockProcessor
from pycmark.readers import BlockQuoteReader, LineReader, ListItemReader


# 5.1 Block quotes
class BlockQuoteProcessor(PatternBlockProcessor):
    paragraph_interruptable = True
    pattern = re.compile('^ {0,3}> ?')

    def run(self, reader: LineReader, document: Element) -> bool:
        quote = nodes.block_quote()
        quote.source, quote.line = reader.get_source_and_line(incr=1)
        document += quote
        self.parser.parse(BlockQuoteReader(reader), quote)
        return True


class ListProcessor(BlockProcessor):
    first_item_pattern = re.compile('^$')
    next_item_pattern = re.compile('^$')
    markers = ''

    def get_item_reader(self, reader: LineReader) -> ListItemReader:
        return ListItemReader(reader, self.markers, self)

    def match(self, reader: LineReader, in_list: bool = False, **kwargs) -> bool:
        if in_list:
            return bool(self.next_item_pattern.match(reader.next_line))
        else:
            return bool(self.first_item_pattern.match(reader.next_line))

    def run(self, reader: LineReader, document: Element) -> bool:
        item_reader = self.get_item_reader(reader)
        list_node = self.create_list_node(item_reader.marker)
        document += list_node

        while True:
            list_item = nodes.list_item()
            list_node += list_item

            item_reader = self.get_item_reader(reader)
            self.consume_blanklines(item_reader, list_item)
            if len(list_item) >= 2:
                # the list item starts with two or more blank lines...
                if not self.is_next_list_item(reader, item_reader.marker):
                    # non list item after blank lines breaks the list
                    break
            else:
                self.parser.parse(item_reader, list_item)
                if not self.is_next_list_item(reader, item_reader.marker):
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

    def is_next_list_item(self, reader: LineReader, marker: str) -> bool:
        """Checks the next line is a next list item or not."""
        try:
            matched = self.next_item_pattern.match(reader.next_line)
            if not matched:
                return False
            elif not self.is_same_marker_type(marker, matched.group(1).strip()):
                return False
            else:
                return True
        except IOError:
            return False

    def consume_blanklines(self, reader: LineReader, list_item: nodes.list_item) -> None:
        """Skip over blank lines at beginning of the list item."""
        try:
            while reader.next_line.strip() == '':
                reader.step()
                list_item += addnodes.blankline()
        except IOError:
            pass

    def create_list_node(self, marker: str) -> Element:
        raise NotImplementedError

    def is_same_marker_type(self, marker: str, candidate: str) -> bool:
        raise NotImplementedError


# 5.2 List items; bullet lists
class BulletListProcessor(ListProcessor):
    paragraph_interruptable = False
    first_item_pattern = re.compile(r'^( {0,3}[-+*])([ \t]+.*|$)')
    next_item_pattern = re.compile(r'^( *[-+*])([ \t]+.*|$)')
    markers = r'[-+*]'

    def create_list_node(self, marker: str) -> Element:
        return nodes.bullet_list(bullet=marker)

    def is_next_list_item(self, reader: LineReader, marker: str) -> bool:
        try:
            pattern = re.compile(r'^(\s*\%s){2,}\s*$' % marker)
            if pattern.match(reader.next_line):
                # themantic break detected
                return False
            else:
                return super().is_next_list_item(reader, marker)
        except IOError:
            return False

    def is_same_marker_type(self, marker: str, candidate: str) -> bool:
        return marker == candidate


class NonEmptyBulletListProcessor(BulletListProcessor):
    # The non-empty bullet list can interrupt paragraphs
    paragraph_interruptable = True
    first_item_pattern = re.compile(r'^( {0,3}[-+*])([ \t]+)(?=\S)(.*)')
    markers = r'[-+*]'


# 5.2 List items; ordered lists
class OrderedListProcessor(ListProcessor):
    paragraph_interruptable = False
    first_item_pattern = re.compile(r'^( {0,3}\d{1,9}[.)])([ \t]+.*|$)')
    next_item_pattern = re.compile(r'^( *\d{1,9}[.)])([ \t]+.*|$)')
    markers = r'\d{1,9}[.)]'

    def create_list_node(self, marker: str) -> Element:
        return nodes.enumerated_list(start=int(marker[:-1]), enumtype="arabic", suffix=marker[-1])

    def is_same_marker_type(self, marker: str, candidate: str) -> bool:
        return marker[-1] == candidate[-1]


class OneBasedOrderedListProcessor(OrderedListProcessor):
    # The ordered list starts with 1 can interrupt paragraphs
    paragraph_interruptable = True
    first_item_pattern = re.compile(r'^( {0,3}1[.)])([ \t]+)(?=\S)(.*)')
