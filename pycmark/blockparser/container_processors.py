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
from pycmark.blockparser import PatternBlockProcessor
from pycmark.readers import BlockQuoteReader


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
