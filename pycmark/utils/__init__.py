# -*- coding: utf-8 -*-
"""
    pycmark.utils
    ~~~~~~~~~~~~~

    Utility libraries

    :copyright: Copyright 2017 by Takeshi KOMIYA
    :license: BSD, see LICENSE for details.
"""

import re

# common regexp
ESCAPED_CHARS = r'\\[!"#$%&\'()*+,./:;<=>?@[\\\]^_`{|}~-]'
escaped_chars_pattern = re.compile(ESCAPED_CHARS)

# HTML regexp
TAGNAME = '[a-zA-Z][a-zA-Z0-9-]*'
ATTRIBUTE_NAME = '[a-zA-Z_:][a-zA-Z0-9_.:-]*'
UNQUOTED_VALUE = "[^ \"'=<>`]+"
SINGLE_QUOTED_VALUE = "'[^']*'"
DOUBLE_QUOTED_VALUE = '"[^"]*"'
ATTRIBUTE_VALUE = ("(?:" + UNQUOTED_VALUE + "|" + SINGLE_QUOTED_VALUE + "|" +
                   DOUBLE_QUOTED_VALUE + ")")
ATTRIBUTE_VALUE_SPEC = "(?:\\s*=\\s*" + ATTRIBUTE_VALUE + ")"
ATTRIBUTE = "(?:\\s+" + ATTRIBUTE_NAME + ATTRIBUTE_VALUE_SPEC + "?)"
OPENTAG = "<" + TAGNAME + ATTRIBUTE + "*\\s*/?>"
CLOSETAG = "</" + TAGNAME + "\\s*>"


def unescape(text):
    return escaped_chars_pattern.sub(lambda m: m.group(0)[1], text)


def normalize_link_label(label):
    label = unescape(label)
    label = re.sub('\s+', '', label)
    return label.strip().casefold()


def transplant_nodes(parent, new_parent, start, end):
    start_pos = parent.index(start)
    end_pos = parent.index(end)
    for _ in range(start_pos + 1, end_pos):
        # Note: do not use Element.remove() here.
        # It removes wrong node if the target is Text.
        subnode = parent.pop(start_pos + 1)
        new_parent += subnode

    return new_parent
