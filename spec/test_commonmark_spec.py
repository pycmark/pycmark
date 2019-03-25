"""
    test_commonmmark_spec
    ~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2019 by Takeshi KOMIYA
    :license: Apache License 2.0, see LICENSE for details.
"""

from md2html import convert


def test_commonmark_spec(commonmark_spec):
    example_id, source, expected = commonmark_spec
    assert convert(source) == expected
