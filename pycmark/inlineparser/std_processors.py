# -*- coding: utf-8 -*-
"""
    pycmark.inlineparser.std_processors
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Standard processor classes for InlineParser.

    :copyright: Copyright 2017 by Takeshi KOMIYA
    :license: BSD, see LICENSE for details.
"""

import re
import unicodedata
from docutils import nodes
from docutils.nodes import Text
from pycmark import addnodes
from pycmark.inlineparser import PatternInlineProcessor, UnmatchedTokenError, backtrack_onerror
from pycmark.utils import entitytrans
from pycmark.utils import OPENTAG, CLOSETAG, escaped_chars_pattern


def is_punctuation(char):
    return 'P' in unicodedata.category(char)


# 6.1 Backslash escapes
class BackslashEscapeProcessor(PatternInlineProcessor):
    pattern = escaped_chars_pattern

    def run(self, document, reader):
        document += addnodes.SparseText(reader.subject, reader.position + 1, reader.position + 2)
        reader.step(2)
        return True


# 6.2 Entity and numeric character references
class EntityReferenceProcessor(PatternInlineProcessor):
    pattern = re.compile(r'&(?:\w{1,32}|#\d+|#X[0-9A-Fa-f]+);')

    def run(self, document, reader):
        text = reader.consume(self.pattern).group(0)
        document += Text(entitytrans._unescape(text))
        return True


# 6.3 Code spans
class CodeSpanProcessor(PatternInlineProcessor):
    pattern = re.compile(r'`+')

    @backtrack_onerror
    def run(self, document, reader):
        marker = reader.consume(self.pattern).group(0)

        pattern = re.compile(marker + r"([^`]|$)")
        text = addnodes.SparseText(reader.remain, 0, 0)
        while reader.remain:
            if pattern.match(reader.remain):
                code = re.sub(r'\s+', ' ', str(text), re.S).strip()
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


# 6.4 Emphasis and strong emphasis
class EmphasisProcessor(PatternInlineProcessor):
    pattern = re.compile(r'(\*+|_+)')
    whitespaces = re.compile(r'\s|0xa0')

    def run(self, document, reader):
        if reader.position == 0:
            before_is_whitespace = True
            before_is_punctuation = False
        else:
            before = reader[reader.position - 1]
            before_is_whitespace = self.whitespaces.match(before)
            before_is_punctuation = is_punctuation(before)

        marker = reader.consume(self.pattern).group(0)

        if reader.remain:
            after = reader.remain[0]
            after_is_whitespace = self.whitespaces.match(after)
            after_is_punctuation = is_punctuation(after)
        else:
            after_is_whitespace = True
            after_is_punctuation = False

        left_flanking = (not after_is_whitespace and
                         (not after_is_punctuation or
                          before_is_whitespace or
                          before_is_punctuation))
        right_flanking = (not before_is_whitespace and
                          (not before_is_punctuation or
                           after_is_whitespace or
                           after_is_punctuation))

        if marker[0] == '_':
            can_open = (left_flanking and
                        (not right_flanking or before_is_punctuation))
            can_close = (right_flanking and
                         (not left_flanking or after_is_punctuation))
        else:
            can_open = left_flanking
            can_close = right_flanking

        document += addnodes.emphasis(marker=marker, can_open=can_open, can_close=can_close,
                                      orig_length=len(marker), curr_length=len(marker))
        return True


# 6.7 Autolinks
class URIAutolinkProcessor(PatternInlineProcessor):
    pattern = re.compile(r'<([a-z][a-z0-9+.-]{1,31}:[^<>\x00-\x20]*)>', re.I)

    def run(self, document, reader):
        uri = reader.consume(self.pattern).group(1)
        document += nodes.reference(uri, uri, refuri=uri)
        return True


class EmailAutolinkProcessor(PatternInlineProcessor):
    pattern = re.compile(r'<([a-zA-Z0-9.!#$%&\'*+/=?^_`{|}~-]+@[a-zA-Z0-9]'
                         r'(?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?'
                         r'(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*)>')

    def run(self, document, reader):
        uri = reader.consume(self.pattern).group(1)
        document += nodes.reference(uri, uri, refuri='mailto:' + uri)
        return True


# 6.8 Raw HTML
class RawHTMLProcessor(PatternInlineProcessor):
    HTML_COMMENT = r'<!---->|<!--(?:-?[^>-])(?:-?[^-])*-->'
    PROCESSING_INSTRUCTION = r"<\?.*?\?>"
    DECLARATION = r"<![A-Z]+" + r"\s+[^>]*>"
    CDATA = r'<!\[CDATA\[[\s\S]*?\]\]>'
    HTMLTAG = ("(?:" + OPENTAG + "|" + CLOSETAG + "|" + HTML_COMMENT + "|" +
               PROCESSING_INSTRUCTION + "|" + DECLARATION + "|" + CDATA + ")")
    pattern = re.compile(HTMLTAG)

    def run(self, document, reader):
        html = reader.consume(self.pattern).group(0)
        document += nodes.raw(html, html, format='html')
        return True
