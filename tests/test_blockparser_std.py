# -*- coding: utf-8 -*-
"""
    test_blockparser_std
    ~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2017 by Takeshi KOMIYA
    :license: BSD, see LICENSE for details.
"""

from docutils import nodes
from utils import publish, assert_node


def test_empty_text():
    result = publish("")
    assert_node(result, [nodes.document, ()])


def test_thematic_breaks():
    result = publish("***")
    assert_node(result, [nodes.document, nodes.transition])

    result = publish("----")
    assert_node(result, [nodes.document, nodes.transition])

    result = publish("_____")
    assert_node(result, [nodes.document, nodes.transition])

    # TODO: add test for short thematic break


def test_indented_thematic_breaks():
    result = publish(" ***")
    assert_node(result, [nodes.document, nodes.transition])

    result = publish("  ---")
    assert_node(result, [nodes.document, nodes.transition])

    result = publish("   ___")
    assert_node(result, [nodes.document, nodes.transition])

    # TODO: add test for four indented thematic break


def test_spanned_thematic_breaks():
    result = publish("* * *")
    assert_node(result, [nodes.document, nodes.transition])

    result = publish("-  -  -")
    assert_node(result, [nodes.document, nodes.transition])

    result = publish("_   _   _")
    assert_node(result, [nodes.document, nodes.transition])
