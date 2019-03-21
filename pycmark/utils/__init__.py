"""
    pycmark.utils
    ~~~~~~~~~~~~~

    Utility libraries

    :copyright: Copyright 2017-2019 by Takeshi KOMIYA
    :license: Apache License 2.0, see LICENSE for details.
"""

import re
from typing import List
from urllib.parse import quote, unquote

from docutils import nodes
from docutils.nodes import Element, Node

# common regexp
ESCAPED_CHARS = r'\\[!"#$%&\'()*+,./:;<=>?@[\\\]^_`{|}~-]'
escaped_chars_pattern = re.compile(ESCAPED_CHARS)

# HTML regexp
TAGNAME = r'[a-zA-Z][a-zA-Z0-9-]*'
ATTRIBUTE_NAME = r'[a-zA-Z_:][a-zA-Z0-9_.:-]*'
UNQUOTED_VALUE = r"[^\s\"'=<>`]+"
SINGLE_QUOTED_VALUE = r"'[^']*'"
DOUBLE_QUOTED_VALUE = r'"[^"]*"'
ATTRIBUTE_VALUE = ("(?:" + UNQUOTED_VALUE + "|" + SINGLE_QUOTED_VALUE + "|" +
                   DOUBLE_QUOTED_VALUE + ")")
ATTRIBUTE_VALUE_SPEC = r"(?:\s*=\s*" + ATTRIBUTE_VALUE + ")"
ATTRIBUTE = r"(?:\s+" + ATTRIBUTE_NAME + ATTRIBUTE_VALUE_SPEC + "?)"
OPENTAG = "<" + TAGNAME + ATTRIBUTE + r"*\s*/?>"
CLOSETAG = "</" + TAGNAME + r"\s*>"


def unescape(text: str) -> str:
    return escaped_chars_pattern.sub(lambda m: m.group(0)[1], text)


def normalize_uri(s: str) -> str:
    """Normalize URI."""
    # https://tools.ietf.org/html/rfc3986.html
    # https://tools.ietf.org/html/rfc5321.html
    safe = ''.join([
        ":?#",          # URI (rfc3986; 3)
        "/",            # Path (rfc3986; 3.3)
        "-._~",         # unreserved (rfc3986; 2.3)
        "!$&'()*+,;=",  # sub-delims (rfc3986; 2.2)
        "@",            # mail address (rfc5321; 4.1.2)
    ])
    return quote(unquote(s), safe=safe)


def expand_leading_tabs(text: str, markers: List[str] = [], tabstop: int = 4) -> str:
    leading_spaces_pattern = re.compile(r'^\s*%s\s*' % r'\s*'.join(markers))
    matched = leading_spaces_pattern.match(text)
    if matched and '\t' in matched.group(0):
        expanded = matched.group(0).expandtabs(tabstop)
        text = leading_spaces_pattern.sub(expanded, text)

    return text


def normalize_link_label(label: str) -> str:
    label = unescape(label)
    label = re.sub(r'\s+', '', label)
    return label.strip().casefold()


def get_root_document(node: Node) -> nodes.document:
    while node.parent:
        node = node.parent

    assert isinstance(node, nodes.document)
    return node


def transplant_nodes(parent: Element, new_parent: Element, start: Node, end: Node) -> Element:
    start_pos = parent.index(start)
    end_pos = parent.index(end)
    for _ in range(start_pos + 1, end_pos):
        # Note: do not use Element.remove() here.
        # It removes wrong node if the target is Text.
        subnode = parent.pop(start_pos + 1)
        new_parent += subnode

    return new_parent
