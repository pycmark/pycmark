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
    # Example 13
    text = ("***\n"
            "---\n"
            "___\n")
    result = publish(text)
    assert_node(result, [nodes.document, (nodes.transition,
                                          nodes.transition,
                                          nodes.transition)])

    # Example 14
    result = publish("+++")
    assert_node(result, [nodes.document, nodes.paragraph, "+++"])

    # Example 16
    text = ("--\n"
            "**\n"
            "__\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.paragraph, text])

    # Example 17
    text = (" ***\n"
            "  ***\n"
            "   ***\n")
    result = publish(text)
    assert_node(result, [nodes.document, (nodes.transition,
                                          nodes.transition,
                                          nodes.transition)])

    # Example 18
    result = publish("    ***")
    assert_node(result, [nodes.document, nodes.literal_block, "***"])

    # Example 20
    result = publish("_____________________________________")
    assert_node(result, [nodes.document, nodes.transition])

    # Example 21
    result = publish(" - - -")
    assert_node(result, [nodes.document, nodes.transition])

    # Example 22
    result = publish(" **  * ** * ** * **")
    assert_node(result, [nodes.document, nodes.transition])

    # Example 24
    result = publish("- - - -    ")
    assert_node(result, [nodes.document, nodes.transition])

    # Example 25
    text = ("_ _ _ _ a\n"
            "\n"
            "a------\n"
            "\n"
            "---a---\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.paragraph, "_ _ _ _ a\n"],
                                          [nodes.paragraph, "a------\n"],
                                          [nodes.paragraph, "---a---\n"])])

    # Example 28
    text = ("Foo\n"
            "***\n"
            "bar\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.paragraph, "Foo\n"],
                                          nodes.transition,
                                          [nodes.paragraph, "bar\n"])])

    # TODO: add test for combination with other notations (Example 29, 30, 31)


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

    # Example 33
    result = publish("####### foo")
    assert_node(result, [nodes.document, nodes.paragraph, "####### foo"])

    # Example 34
    text = ("#5 bolt\n"
            "\n"
            "#hashtag\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.paragraph, "#5 bolt\n"],
                                          [nodes.paragraph, "#hashtag\n"])])

    # TODO: add test for inlines in title (Example 36)

    # Example 37
    result = publish("#                  foo                     ")
    assert_node(result, [nodes.document, nodes.section, nodes.title, "foo"])

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

    # Example 48
    text = ("Foo bar\n"
            "# baz\n"
            "Bar foo\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.paragraph, "Foo bar\n"],
                                          [nodes.section, nodes.title, "baz"],
                                          [nodes.paragraph, "Bar foo\n"])])

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

    # Example 82
    text = ("Foo\n"
            "    bar\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.paragraph, "Foo\nbar\n"])

    # Example 83
    text = ("    foo\n"
            "bar\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.literal_block, "foo\n"],
                                          [nodes.paragraph, "bar\n"])])

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

    # Example 90
    text = ("``\n"
            "foo\n"
            "``\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.paragraph, text])

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

    # Example 97
    text = ("> ```\n"
            "> aaa\n"
            "\n"
            "bbb\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.block_quote, nodes.literal_block, "aaa\n"],
                                          [nodes.paragraph, "bbb\n"])])

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

    # Example 109
    text = ("foo\n"
            "```\n"
            "bar\n"
            "```\n"
            "baz\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.paragraph, "foo\n"],
                                          [nodes.literal_block, "bar\n"],
                                          [nodes.paragraph, "baz\n"])])

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
