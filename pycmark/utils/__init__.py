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
