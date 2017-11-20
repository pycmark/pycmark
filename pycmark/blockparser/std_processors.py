# -*- coding: utf-8 -*-
"""
    pycmark.blockparser.std_processors
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Standard processor classes for BlockParser.

    :copyright: Copyright 2017 by Takeshi KOMIYA
    :license: BSD, see LICENSE for details.
"""

import re
from docutils import nodes
from pycmark.blockparser import PatternBlockProcessor


# 4.1 Thematic breaks
class ThematicBreakProcessor(PatternBlockProcessor):
    pattern = re.compile('^ {0,3}((\*\s*){3,}|(-\s*){3,}|(_\s*){3,})\s*$')

    def run(self, document, reader):
        reader.readline()
        document += nodes.transition()
        return True


# 4.2 ATX headings
class ATXHeadingProcessor(PatternBlockProcessor):
    pattern = re.compile('^ {0,3}(#{1,6})\s(.*)$')
    trailing_hashes = re.compile('\s+#+\s*$')

    def run(self, document, reader):
        marker, title = self.pattern.match(reader.readline()).groups()
        title = self.trailing_hashes.sub('', title.strip())
        title_node = nodes.title(title, title)
        title_node.source, title_node.line = reader.get_source_and_line()
        document += nodes.section('', title_node, depth=len(marker))
        return True
