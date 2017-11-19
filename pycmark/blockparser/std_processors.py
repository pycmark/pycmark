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
