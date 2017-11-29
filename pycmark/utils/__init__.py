# -*- coding: utf-8 -*-
"""
    pycmark.utils
    ~~~~~~~~~~~~~

    Utility libraries

    :copyright: Copyright 2017 by Takeshi KOMIYA
    :license: BSD, see LICENSE for details.
"""

import re

ESCAPED_CHARS = r'\\[!"#$%&\'()*+,./:;<=>?@[\\\]^_`{|}~-]'
escaped_chars_pattern = re.compile(ESCAPED_CHARS)


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
