"""
    test_utils
    ~~~~~~~~~~

    :copyright: Copyright 2017-2019 by Takeshi KOMIYA
    :license: Apache License 2.0, see LICENSE for details.
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

    # markers not found
    text = "  >\t-\tLorem ipsum\tdolor sit amet"
    assert expand_leading_tabs(text, ['-']) == "  >\t-\tLorem ipsum\tdolor sit amet"

    # large tabstop
    text = "\tLorem ipsum\tdolor sit amet"
    assert expand_leading_tabs(text, tabstop=8) == "        Lorem ipsum\tdolor sit amet"


def test_expand_leading_tabs_with_markers():
    text = "  >\tLorem ipsum\tdolor sit amet"
    assert expand_leading_tabs(text) == "  >\tLorem ipsum\tdolor sit amet"

    text = "  >\tLorem ipsum\tdolor sit amet"
    assert expand_leading_tabs(text, ['>']) == "  > Lorem ipsum\tdolor sit amet"

    text = "  >\t-\tLorem ipsum\tdolor sit amet"
    assert expand_leading_tabs(text, ['>', '-']) == "  > -   Lorem ipsum\tdolor sit amet"

    text = "  -\tLorem ipsum\tdolor sit amet"
    assert expand_leading_tabs(text, ['[-+*]']) == "  - Lorem ipsum\tdolor sit amet"

    text = " 1.\tLorem ipsum\tdolor sit amet"
    assert expand_leading_tabs(text, [r'\d+\.']) == " 1. Lorem ipsum\tdolor sit amet"
