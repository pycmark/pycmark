# -*- coding: utf-8 -*-
"""
    pycmark.inlineparser.std_processors
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Standard processor classes for InlineParser.

    :copyright: Copyright 2017 by Takeshi KOMIYA
    :license: BSD, see LICENSE for details.
"""

import re
from pycmark import addnodes
from pycmark.inlineparser import PatternInlineProcessor


# 6.1 Backslash escapes
class BackslashEscapeProcessor(PatternInlineProcessor):
    pattern = re.compile('\\\\[!"#$%&\'()*+,./:;<=>?@[\\\\\\]^_`{|}~-]')

    def run(self, document, reader):
        document += addnodes.SparseText(reader.subject, reader.position + 1, reader.position + 2)
        reader.step(2)
        return True
