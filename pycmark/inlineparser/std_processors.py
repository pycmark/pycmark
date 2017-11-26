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
from pycmark import addnodes
from pycmark.inlineparser import (
    PatternInlineProcessor, UnmatchedTokenError, ParseError, backtrack_onerror
)
from pycmark.utils import entitytrans
from pycmark.utils import ESCAPED_CHARS, escaped_chars_pattern, unescape, transplant_nodes


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
    pattern = re.compile('&(?:\w{1,32}|#\d+|#X[0-9A-Fa-f]+);')

    def run(self, document, reader):
        text = reader.consume(self.pattern).group(0)
        document += nodes.Text(entitytrans._unescape(text))
        return True


# 6.3 Code spans
class CodeSpanProcessor(PatternInlineProcessor):
    pattern = re.compile('`+')

    @backtrack_onerror
    def run(self, document, reader):
        marker = reader.consume(self.pattern).group(0)

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


# 6.4 Emphasis and strong emphasis
class EmphasisProcessor(PatternInlineProcessor):
    pattern = re.compile('(\*+|_+)')
    whitespaces = re.compile('\s|0xa0')

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


# 6.5 Links
# 6.6 Images
class LinkOpenerProcessor(PatternInlineProcessor):
    pattern = re.compile('\!?\[')

    def run(self, document, reader):
        marker = reader.consume(self.pattern).group(0)
        document += addnodes.bracket(marker=marker, can_open=True)
        return True


class LinkCloserProcessor(PatternInlineProcessor):
    pattern = re.compile('\]')

    def run(self, document, reader):
        reader.step(1)
        document += addnodes.bracket(marker="]", can_open=False)
        self.process_link_or_image(document, reader)
        return True

    @backtrack_onerror
    def process_link_or_image(self, document, reader):
        brackets = list(n for n in document.children if isinstance(n, addnodes.bracket))
        openers = list(d for d in brackets if d['can_open'])
        if len(openers) == 0:
            return

        opener = openers.pop()
        closer = brackets.pop()

        if reader.remain.startswith('('):
            # link destination + link title (optional)
            #     [...](<.+> ".+")
            #     [...](.+ ".+")
            reader.step()
            destination = LinkDestinationParser().parse(document, reader)
            title = LinkTitleParser().parse(document, reader)
            assert reader.consume(re.compile('\s*\)'))
        elif reader.remain.startswith('['):
            # link label
            #     [...][.*]
            raise NotImplementedError
        else:
            # deactivate brackets because no trailing link destination or link-label
            opener.replace_self(nodes.Text(opener['marker']))
            closer.replace_self(nodes.Text(closer['marker']))
            raise

        if opener['marker'] == '![':
            para = transplant_nodes(document, nodes.paragraph(), start=opener, end=closer)
            node = nodes.image('', uri=destination, alt=para.astext())
            if title:
                node['title'] = title
        else:
            node = nodes.reference('', refuri=destination)
            transplant_nodes(document, node, start=opener, end=closer)
            if title:
                node['reftitle'] = title

            # deactivate all left brackets before the link
            for n in openers:
                if n['marker'] == '[':
                    n.replace_self(nodes.Text(n['marker']))

        document += node
        document.remove(opener)
        document.remove(closer)
        return True


class LinkDestinationParser(object):
    pattern = re.compile(r'\s*<((?:[^ <>\n\\]|' + ESCAPED_CHARS + r'|\\)*)>', re.S)

    def parse(self, document, reader):
        matched = reader.consume(self.pattern)
        if matched:
            return unescape(entitytrans._unescape(matched.group(1)))
        else:
            return self.parseBareLinkDestination(document, reader)

    def parseBareLinkDestination(self, document, reader):
        assert reader.consume(re.compile('[ \n]*'))

        parens = 0
        start = reader.position
        while reader.remain:
            c = reader.remain[0]
            if c in (' ', '\n'):
                break
            elif c == '(':
                parens += 1
            elif c == ')':
                parens -= 1
                if parens < 0:
                    break
            elif escaped_chars_pattern.match(reader.remain):
                reader.step()  # one more step for escaping

            reader.step()
        else:
            raise ParseError

        end = reader.position
        return unescape(entitytrans._unescape(reader[start:end]))


class LinkTitleParser(object):
    pattern = re.compile('\s*("(' + ESCAPED_CHARS + '|[^"])*"|' +
                         "'(" + ESCAPED_CHARS + "|[^'])*'|" +
                         "\\((" + ESCAPED_CHARS + "|[^)])*\\))")

    def parse(self, document, reader):
        matched = reader.consume(self.pattern)
        if matched:
            return unescape(entitytrans._unescape(matched.group(1)[1:-1]))
        else:
            return None


# 6.7 Autolinks
class URIAutolinkProcessor(PatternInlineProcessor):
    pattern = re.compile('<([a-z][a-z0-9+.-]{1,31}:[^<>\x00-\x20]*)>', re.I)

    def run(self, document, reader):
        uri = reader.consume(self.pattern).group(1)
        document += nodes.reference(uri, uri, refuri=uri)
        return True


class EmailAutolinkProcessor(PatternInlineProcessor):
    pattern = re.compile('<([a-zA-Z0-9.!#$%&\'*+/=?^_`{|}~-]+@[a-zA-Z0-9]'
                         '(?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?'
                         '(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*)>')

    def run(self, document, reader):
        uri = reader.consume(self.pattern).group(1)
        document += nodes.reference(uri, uri, refuri='mailto:' + uri)
        return True
