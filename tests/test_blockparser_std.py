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


def test_atx_headings():
    # Example 32
    text = ("# foo\n"
            "## foo\n"
            "### foo\n"
            "#### foo\n"
            "##### foo\n"
            "###### foo\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.section, nodes.title, "foo"],
                                          [nodes.section, nodes.title, "foo"],
                                          [nodes.section, nodes.title, "foo"],
                                          [nodes.section, nodes.title, "foo"],
                                          [nodes.section, nodes.title, "foo"],
                                          [nodes.section, nodes.title, "foo"])])
    assert_node(result[0], nodes.section, depth=1)
    assert_node(result[1], nodes.section, depth=2)
    assert_node(result[2], nodes.section, depth=3)
    assert_node(result[3], nodes.section, depth=4)
    assert_node(result[4], nodes.section, depth=5)
    assert_node(result[5], nodes.section, depth=6)

    # TODO: add test for 7th leveled headings (Example 33)

    # TODO: add test for no spaces after # (Example 34)

    # TODO: add test for inlines in title (Example 36)

    # Example 38
    text = (" ### foo\n"
            "  ## foo\n"
            "   # foo\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.section, nodes.title, "foo"],
                                          [nodes.section, nodes.title, "foo"],
                                          [nodes.section, nodes.title, "foo"])])
    assert_node(result[0], nodes.section, depth=3)
    assert_node(result[1], nodes.section, depth=2)
    assert_node(result[2], nodes.section, depth=1)

    # Example 41
    text = ("## foo ##\n"
            "  ###   bar    ###\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.section, nodes.title, "foo"],
                                          [nodes.section, nodes.title, "bar"])])

    # Example 42
    text = ("# foo ##################################\n"
            "##### foo ##\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.section, nodes.title, "foo"],
                                          [nodes.section, nodes.title, "foo"])])

    # Example 43
    result = publish("### foo ###     ")
    assert_node(result, [nodes.document, nodes.section, nodes.title, "foo"])

    # Example 44
    result = publish("### foo ### b")
    assert_node(result, [nodes.document, nodes.section, nodes.title, "foo ### b"])

    # Example 45
    result = publish("# foo#")
    assert_node(result, [nodes.document, nodes.section, nodes.title, "foo#"])
    # Example 46
    text = ("### foo \\###\n"
            "## foo #\\##\n"
            "# foo \\#\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.section, nodes.title, "foo \\###"],
                                          [nodes.section, nodes.title, "foo #\\##"],
                                          [nodes.section, nodes.title, "foo \\#"])])

    # Example 49
    text = ("## \n"
            "#\n"
            "### ###\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.section, nodes.title],
                                          [nodes.section, nodes.title],
                                          [nodes.section, nodes.title])])


def test_indented_blocks():
    # Example 76
    text = ("    a simple\n"
            "      indented code block\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.literal_block, "a simple\n  indented code block\n"])

    # Example 79
    text = ("    <a/>\n"
            "    *hi*\n"
            "\n"
            "    - one\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.literal_block, "<a/>\n*hi*\n\n- one\n"])

    # Example 81
    text = ("    chunk1\n"
            "      \n"
            "      chunk2\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.literal_block, "chunk1\n  \n  chunk2\n"])

    # TODO: add test for combination with paragraph (Example 82 and 83)

    # Example 86
    text = ("\n"
            "    \n"
            "    foo\n"
            "    \n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.literal_block, "foo\n"])


def test_fenced_code_blocks():
    # Example 88
    text = ("```\n"
            "<\n"
            " >\n"
            "```\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.literal_block, "<\n >\n"])

    # Example 89
    text = ("~~~\n"
            "<\n"
            " >\n"
            "~~~\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.literal_block, "<\n >\n"])

    # TODO: add test for lesser backtics (Example 90)

    # Example 91
    text = ("```\n"
            "aaa\n"
            "~~~\n"
            "```\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.literal_block, "aaa\n~~~\n"])

    # Example 92
    text = ("~~~\n"
            "aaa\n"
            "```\n"
            "~~~\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.literal_block, "aaa\n```\n"])

    # Example 93
    text = ("````\n"
            "aaa\n"
            "```\n"
            "``````\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.literal_block, "aaa\n```\n"])

    # Example 95
    result = publish("```")
    assert_node(result, [nodes.document, nodes.literal_block])

    # Example 96
    text = ("`````\n"
            "\n"
            "```\n"
            "aaa\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.literal_block, "\n```\naaa\n"])

    # TODO: add test for combination with block_quotes (Example 97)

    # Example 100
    text = (" ```\n"
            " aaa\n"
            "aaa\n"
            "```\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.literal_block, "aaa\naaa\n"])

    # Example 102
    text = ("   ```\n"
            "   aaa\n"
            "    aaa\n"
            "  aaa\n"
            "   ```\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.literal_block, "aaa\n aaa\naaa\n"])

    # Example 103
    text = ("    ```\n"
            "    aaa\n"
            "    ```\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.literal_block, "```\naaa\n```\n"])

    # Example 106
    text = ("```\n"
            "aaa\n"
            "    ```\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.literal_block, "aaa\n    ```\n"])

    # TODO: add test for inline code spans (Example 107)

    # Example 111
    text = ("```ruby\n"
            "def foo(x)\n"
            "  return 3\n"
            "end\n"
            "```\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.literal_block, "def foo(x)\n  return 3\nend\n"])
    assert_node(result[0], nodes.literal_block, classes=["language-ruby"])

    # TODO: add test for inline code spans (Example 114)

    # Example 115
    text = ("```\n"
            "``` aaa\n"
            "```\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.literal_block, "``` aaa\n"])
