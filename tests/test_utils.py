# -*- coding: utf-8 -*-
"""
    test_utils
    ~~~~~~~~~~

    :copyright: Copyright 2017 by Takeshi KOMIYA
    :license: BSD, see LICENSE for details.
"""

from pycmark.utils import expand_leading_tabs


def test_expand_leading_tabs():
    # normal case
    text = "\tLorem ipsum\tdolor sit amet"
    assert expand_leading_tabs(text) == "    Lorem ipsum\tdolor sit amet"

    text = "  \tLorem ipsum\tdolor sit amet"
    assert expand_leading_tabs(text) == "    Lorem ipsum\tdolor sit amet"

    text = "\t  Lorem ipsum\tdolor sit amet"
    assert expand_leading_tabs(text) == "      Lorem ipsum\tdolor sit amet"

    text = "  \t  Lorem ipsum\tdolor sit amet"
    assert expand_leading_tabs(text) == "      Lorem ipsum\tdolor sit amet"

    # no tabs
    text = "Lorem ipsum\tdolor sit amet"
    assert expand_leading_tabs(text) == text

    # large tabstop
    text = "\tLorem ipsum\tdolor sit amet"
    assert expand_leading_tabs(text, 8) == "        Lorem ipsum\tdolor sit amet"
