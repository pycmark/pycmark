# -*- coding: utf-8 -*-
"""
    test_blockparser_container
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2017 by Takeshi KOMIYA
    :license: BSD, see LICENSE for details.
"""

from docutils import nodes
from utils import publish, assert_node


def test_block_quotes():
    # Example 191
    text = ("> # Foo\n"
            "> bar\n"
            "> baz\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.block_quote, ([nodes.section, nodes.title, "Foo"],
                                                             [nodes.paragraph, "bar\nbaz\n"])])

    # Example 192
    text = ("># Foo\n"
            ">bar\n"
            "> baz\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.block_quote, ([nodes.section, nodes.title, "Foo"],
                                                             [nodes.paragraph, "bar\nbaz\n"])])

    # Example 193
    text = ("   > # Foo\n"
            "   > bar\n"
            " > baz\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.block_quote, ([nodes.section, nodes.title, "Foo"],
                                                             [nodes.paragraph, "bar\nbaz\n"])])

    # Example 195
    text = ("> # Foo\n"
            "> bar\n"
            "baz\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.block_quote, ([nodes.section, nodes.title, "Foo"],
                                                             [nodes.paragraph, "bar\nbaz\n"])])

    # Example 196
    text = ("> bar\n"
            "baz\n"
            "> foo\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.block_quote, nodes.paragraph, "bar\nbaz\nfoo\n"])

    # Example 197
    text = ("> foo\n"
            "---\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.block_quote, nodes.paragraph, "foo\n"],
                                          nodes.transition)])

    # TODO: Add test for combination with bullet list (Example 198)

    # Example 199
    text = (">     foo\n"
            "    bar\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.block_quote, nodes.literal_block, "foo\n"],
                                          [nodes.literal_block, "bar\n"])])

    # Example 200
    text = ("> ```\n"
            "foo\n"
            "```\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.block_quote, nodes.literal_block],
                                          [nodes.paragraph, "foo\n"],
                                          [nodes.literal_block])])

    # Example 201
    text = ("> foo\n"
            "    - bar\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.block_quote, nodes.paragraph, "foo\n- bar\n"])

    # Example 203
    text = (">\n"
            ">\n"
            ">\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.block_quote, ()])

    # Example 204
    text = ("> foo\n"
            "\n"
            "> bar\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.block_quote, nodes.paragraph, "foo\n"],
                                          [nodes.block_quote, nodes.paragraph, "bar\n"])])

    # Example 205
    text = ("foo\n"
            "> bar\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.paragraph, "foo\n"],
                                          [nodes.block_quote, nodes.paragraph, "bar\n"])])

    # Example 212
    text = ("> bar\n"
            ">\n"
            "baz\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.block_quote, nodes.paragraph, "bar\n"],
                                          [nodes.paragraph, "baz\n"])])

    # Example 213
    text = ("> > > foo\n"
            "bar\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.block_quote, nodes.block_quote,
                         nodes.block_quote, nodes.paragraph, "foo\nbar\n"])

    # Example 214
    text = (">>> foo\n"
            "> bar\n"
            ">>baz\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.block_quote, nodes.block_quote,
                         nodes.block_quote, nodes.paragraph, "foo\nbar\nbaz\n"])

    # Example 215
    text = (">     code\n"
            "\n"
            ">    not code\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.block_quote, nodes.literal_block, "code\n"],
                                          [nodes.block_quote, nodes.paragraph, "not code\n"])])
