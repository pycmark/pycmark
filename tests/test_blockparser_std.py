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


def test_example_13():
    text = ("***\n"
            "---\n"
            "___\n")
    result = publish(text)
    assert_node(result, [nodes.document, (nodes.transition,
                                          nodes.transition,
                                          nodes.transition)])


def test_example_14():
    result = publish("+++")
    assert_node(result, [nodes.document, nodes.paragraph, "+++"])


def test_example_16():
    text = ("--\n"
            "**\n"
            "__\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.paragraph, text])


def test_example_17():
    text = (" ***\n"
            "  ***\n"
            "   ***\n")
    result = publish(text)
    assert_node(result, [nodes.document, (nodes.transition,
                                          nodes.transition,
                                          nodes.transition)])


def test_example_18():
    result = publish("    ***")
    assert_node(result, [nodes.document, nodes.literal_block, "***"])


def test_example_20():
    result = publish("_____________________________________")
    assert_node(result, [nodes.document, nodes.transition])


def test_example_21():
    result = publish(" - - -")
    assert_node(result, [nodes.document, nodes.transition])


def test_example_22():
    result = publish(" **  * ** * ** * **")
    assert_node(result, [nodes.document, nodes.transition])


def test_example_24():
    result = publish("- - - -    ")
    assert_node(result, [nodes.document, nodes.transition])


def test_example_25():
    text = ("_ _ _ _ a\n"
            "\n"
            "a------\n"
            "\n"
            "---a---\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.paragraph, "_ _ _ _ a\n"],
                                          [nodes.paragraph, "a------\n"],
                                          [nodes.paragraph, "---a---\n"])])


def test_example_28():
    text = ("Foo\n"
            "***\n"
            "bar\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.paragraph, "Foo\n"],
                                          nodes.transition,
                                          [nodes.paragraph, "bar\n"])])

# TODO: add test for combination with other notations (Example 29, 30, 31)


def test_example_32():
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


def test_example_33():
    result = publish("####### foo")
    assert_node(result, [nodes.document, nodes.paragraph, "####### foo"])


def test_example_34():
    text = ("#5 bolt\n"
            "\n"
            "#hashtag\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.paragraph, "#5 bolt\n"],
                                          [nodes.paragraph, "#hashtag\n"])])

# TODO: add test for inlines in title (Example 36)


def test_example_37():
    result = publish("#                  foo                     ")
    assert_node(result, [nodes.document, nodes.section, nodes.title, "foo"])


def test_example_38():
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


def test_example_41():
    text = ("## foo ##\n"
            "  ###   bar    ###\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.section, nodes.title, "foo"],
                                          [nodes.section, nodes.title, "bar"])])


def test_example_42():
    text = ("# foo ##################################\n"
            "##### foo ##\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.section, nodes.title, "foo"],
                                          [nodes.section, nodes.title, "foo"])])


def test_example_43():
    result = publish("### foo ###     ")
    assert_node(result, [nodes.document, nodes.section, nodes.title, "foo"])


def test_example_44():
    result = publish("### foo ### b")
    assert_node(result, [nodes.document, nodes.section, nodes.title, "foo ### b"])


def test_example_45():
    result = publish("# foo#")
    assert_node(result, [nodes.document, nodes.section, nodes.title, "foo#"])


def test_example_46():
    text = ("### foo \\###\n"
            "## foo #\\##\n"
            "# foo \\#\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.section, nodes.title, "foo \\###"],
                                          [nodes.section, nodes.title, "foo #\\##"],
                                          [nodes.section, nodes.title, "foo \\#"])])


def test_example_48():
    text = ("Foo bar\n"
            "# baz\n"
            "Bar foo\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.paragraph, "Foo bar\n"],
                                          [nodes.section, nodes.title, "baz"],
                                          [nodes.paragraph, "Bar foo\n"])])


def test_example_49():
    text = ("## \n"
            "#\n"
            "### ###\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.section, nodes.title],
                                          [nodes.section, nodes.title],
                                          [nodes.section, nodes.title])])


def test_example_76():
    text = ("    a simple\n"
            "      indented code block\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.literal_block, "a simple\n  indented code block\n"])


def test_example_79():
    text = ("    <a/>\n"
            "    *hi*\n"
            "\n"
            "    - one\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.literal_block, "<a/>\n*hi*\n\n- one\n"])


def test_example_81():
    text = ("    chunk1\n"
            "      \n"
            "      chunk2\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.literal_block, "chunk1\n  \n  chunk2\n"])


def test_example_82():
    text = ("Foo\n"
            "    bar\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.paragraph, "Foo\nbar\n"])


def test_example_83():
    text = ("    foo\n"
            "bar\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.literal_block, "foo\n"],
                                          [nodes.paragraph, "bar\n"])])


def test_example_86():
    text = ("\n"
            "    \n"
            "    foo\n"
            "    \n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.literal_block, "foo\n"])


def test_example_88():
    text = ("```\n"
            "<\n"
            " >\n"
            "```\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.literal_block, "<\n >\n"])


def test_example_89():
    text = ("~~~\n"
            "<\n"
            " >\n"
            "~~~\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.literal_block, "<\n >\n"])


def test_example_90():
    text = ("``\n"
            "foo\n"
            "``\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.paragraph, text])


def test_example_91():
    text = ("```\n"
            "aaa\n"
            "~~~\n"
            "```\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.literal_block, "aaa\n~~~\n"])


def test_example_92():
    text = ("~~~\n"
            "aaa\n"
            "```\n"
            "~~~\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.literal_block, "aaa\n```\n"])


def test_example_93():
    text = ("````\n"
            "aaa\n"
            "```\n"
            "``````\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.literal_block, "aaa\n```\n"])


def test_example_95():
    result = publish("```")
    assert_node(result, [nodes.document, nodes.literal_block])


def test_example_96():
    text = ("`````\n"
            "\n"
            "```\n"
            "aaa\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.literal_block, "\n```\naaa\n"])


def test_example_97():
    text = ("> ```\n"
            "> aaa\n"
            "\n"
            "bbb\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.block_quote, nodes.literal_block, "aaa\n"],
                                          [nodes.paragraph, "bbb\n"])])


def test_example_100():
    text = (" ```\n"
            " aaa\n"
            "aaa\n"
            "```\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.literal_block, "aaa\naaa\n"])


def test_example_102():
    text = ("   ```\n"
            "   aaa\n"
            "    aaa\n"
            "  aaa\n"
            "   ```\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.literal_block, "aaa\n aaa\naaa\n"])


def test_example_103():
    text = ("    ```\n"
            "    aaa\n"
            "    ```\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.literal_block, "```\naaa\n```\n"])


def test_example_106():
    text = ("```\n"
            "aaa\n"
            "    ```\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.literal_block, "aaa\n    ```\n"])

# TODO: add test for inline code spans (Example 107)


def test_example_109():
    text = ("foo\n"
            "```\n"
            "bar\n"
            "```\n"
            "baz\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.paragraph, "foo\n"],
                                          [nodes.literal_block, "bar\n"],
                                          [nodes.paragraph, "baz\n"])])


def test_example_111():
    text = ("```ruby\n"
            "def foo(x)\n"
            "  return 3\n"
            "end\n"
            "```\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.literal_block, "def foo(x)\n  return 3\nend\n"])
    assert_node(result[0], nodes.literal_block, classes=["language-ruby"])

# TODO: add test for inline code spans (Example 114)


def test_example_115():
    text = ("```\n"
            "``` aaa\n"
            "```\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.literal_block, "``` aaa\n"])
