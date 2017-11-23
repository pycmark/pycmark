# -*- coding: utf-8 -*-
"""
    pycmark.inlineparser.std_processors
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Standard processor classes for InlineParser.

    :copyright: Copyright 2017 by Takeshi KOMIYA
    :license: BSD, see LICENSE for details.
"""

import re
from docutils import nodes
from pycmark import addnodes
from pycmark.inlineparser import (
    PatternInlineProcessor, UnmatchedTokenError, backtrack_onerror
)


# 6.1 Backslash escapes
class BackslashEscapeProcessor(PatternInlineProcessor):
    pattern = re.compile('\\\\[!"#$%&\'()*+,./:;<=>?@[\\\\\\]^_`{|}~-]')

    def run(self, document, reader):
        document += addnodes.SparseText(reader.subject, reader.position + 1, reader.position + 2)
        reader.step(2)
        return True


# 6.3 Code spans
class CodeSpanProcessor(PatternInlineProcessor):
    pattern = re.compile('(`+)')

    @backtrack_onerror
    def run(self, document, reader):
        marker = self.pattern.match(reader.remain).group(1)
        reader.step(len(marker))

        pattern = re.compile(marker + "([^`]|$)")
        text = addnodes.SparseText(reader.remain, 0, 0)
        while reader.remain:
            if pattern.match(reader.remain):
                code = re.sub('\s+', ' ', str(text), re.S).strip()
                document += nodes.literal(code, code)
                reader.step(len(marker))
                return True
            elif reader.remain[0] == '`':
                while reader.remain and reader.remain[0] == '`':
                    text.spread(end=1)
                    reader.step()
            else:
                text.spread(end=1)
                reader.step()
        else:
            raise UnmatchedTokenError(marker)
