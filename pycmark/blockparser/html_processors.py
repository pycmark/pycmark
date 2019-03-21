"""
    pycmark.blockparser.html_processors
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    HTML processor classes for BlockParser.

    :copyright: Copyright 2017-2019 by Takeshi KOMIYA
    :license: Apache License 2.0, see LICENSE for details.
"""

import re

from docutils import nodes
from docutils.nodes import Element

from pycmark.blockparser import PatternBlockProcessor
from pycmark.readers import LineReader
from pycmark.utils import OPENTAG, CLOSETAG

STANDARD_HTML_TAGS = (
    'address', 'article', 'aside', 'base', 'basefont', 'blockquote', 'body',
    'caption', 'center', 'col', 'colgroup', 'dd', 'details', 'dialog', 'dir',
    'div', 'dl', 'dt', 'fieldset', 'figcaption', 'figure', 'footer', 'form',
    'frame', 'frameset', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'head', 'header',
    'hr', 'html', 'iframe', 'legend', 'li', 'link', 'main', 'menu', 'menuitem',
    'meta', 'nav', 'noframes', 'ol', 'optgroup', 'option', 'p', 'param',
    'section', 'source', 'summary', 'table', 'tbody', 'td', 'tfoot', 'th',
    'thead', 'title', 'tr', 'track', 'ul'
)


class BaseHTMLBlockProcessor(PatternBlockProcessor):
    paragraph_interruptable = True
    closing_pattern = re.compile(r'^$')

    def run(self, reader: LineReader, document: Element) -> bool:
        location = reader.get_source_and_line(incr=1)
        content = ''
        for line in reader:
            content += line
            if self.closing_pattern.search(line):
                break

        content = re.sub('\n+$', '\n', content)  # strip multiple CRs on tail
        document += nodes.raw(content, content, format='html')
        location.set_source_info(document[-1])
        return True


# 4.6 HTML blocks; <script>, <pre>, <script>
class ScriptHTMLBlockProcessor(BaseHTMLBlockProcessor):
    priority = 400
    pattern = re.compile(r'^ {0,3}<(script|pre|style)( |>|$)', re.I)
    closing_pattern = re.compile(r'</(script|pre|style)>', re.I)


# 4.6 HTML blocks; <!-- ... -->
class CommentHTMLBlockProcessor(BaseHTMLBlockProcessor):
    pattern = re.compile(r'^ {0,3}<\!--')
    closing_pattern = re.compile(r'-->')


# 4.6 HTML blocks; <? ... ?>
class ProcessingInstructionHTMLBlockProcessor(BaseHTMLBlockProcessor):
    pattern = re.compile(r'^ {0,3}<\?', re.I)
    closing_pattern = re.compile(r'\?>', re.I)


# 4.6 HTML blocks; declarations
class DeclarationHTMLBlockProcessor(BaseHTMLBlockProcessor):
    pattern = re.compile(r'^ {0,3}<\![A-Z]+')
    closing_pattern = re.compile(r'>')


# 4.6 HTML blocks; CDATA
class CdataHTMLBlockProcessor(BaseHTMLBlockProcessor):
    pattern = re.compile(r'^ {0,3}<\!\[CDATA\[')
    closing_pattern = re.compile(r']]>')


# 4.6 HTML blocks; Standard tags
class StandardTagsHTMLBlockProcessor(BaseHTMLBlockProcessor):
    pattern = re.compile(r'^ {0,3}</?(%s)( |>|/>|$)' % '|'.join(STANDARD_HTML_TAGS), re.I)
    closing_pattern = re.compile(r'^\s*$')


# 4.6 HTML blocks; complete tags
class CompleteTagsHTMLBlockProcessor(BaseHTMLBlockProcessor):
    paragraph_interruptable = False
    pattern = re.compile(r'^ {0,3}(?:' + OPENTAG + '|' + CLOSETAG + r')\s*$')
    closing_pattern = re.compile(r'^\s*$')
