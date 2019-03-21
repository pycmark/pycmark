"""
    test_blockparser_std
    ~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2017-2019 by Takeshi KOMIYA
    :license: Apache License 2.0, see LICENSE for details.
"""

from docutils import nodes
from utils import publish, assert_node


def test_empty_text():
    result = publish("")
    assert_node(result, [nodes.document, ()])


def test_example_1():
    result = publish("\tfoo\tbaz\t\tbim")
    assert_node(result, [nodes.document, nodes.literal_block, "foo\tbaz\t\tbim"])


def test_example_2():
    result = publish("  \tfoo\tbaz\t\tbim")
    assert_node(result, [nodes.document, nodes.literal_block, "foo\tbaz\t\tbim"])


def test_example_4():
    text = ("  - foo\n"
            "\n"
            "\tbar\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.bullet_list, nodes.list_item, ([nodes.paragraph, "foo"],
                                                                              [nodes.paragraph, "bar"])])


def test_example_5():
    text = ("- foo\n"
            "\n"
            "\t\tbar\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.bullet_list, nodes.list_item, ([nodes.paragraph, "foo"],
                                                                              [nodes.literal_block, "  bar\n"])])


def test_example_6():
    result = publish(">\t\tfoo\n")
    assert_node(result, [nodes.document, nodes.block_quote, nodes.literal_block, "  foo\n"])


def test_example_7():
    result = publish("-\t\tfoo\n")
    assert_node(result, [nodes.document, nodes.bullet_list, nodes.list_item, nodes.literal_block, "  foo\n"])


def test_example_9():
    text = (" - foo\n"
            "   - bar\n"
            "\t - baz\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.bullet_list, nodes.list_item, ("foo",
                                                                              nodes.bullet_list)])
    assert_node(result[0][0][1], [nodes.bullet_list, nodes.list_item, ("bar",
                                                                       nodes.bullet_list)])
    assert_node(result[0][0][1][0][1], [nodes.bullet_list, nodes.list_item, "baz"])


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
    assert_node(result, [nodes.document, nodes.paragraph, "--\n**\n__"])


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
    assert_node(result, [nodes.document, ([nodes.paragraph, "_ _ _ _ a"],
                                          [nodes.paragraph, "a------"],
                                          [nodes.paragraph, "---a---"])])


def test_example_28():
    text = ("Foo\n"
            "***\n"
            "bar\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.paragraph, "Foo"],
                                          nodes.transition,
                                          [nodes.paragraph, "bar"])])


def test_example_29():
    text = ("Foo\n"
            "---\n"
            "bar\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.section, ([nodes.title, "Foo"],
                                                         [nodes.paragraph, "bar"])])


def test_example_30():
    text = ("* Foo\n"
            "* * *\n"
            "* Bar\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.bullet_list, nodes.list_item, "Foo"],
                                          nodes.transition,
                                          [nodes.bullet_list, nodes.list_item, "Bar"])])


def test_example_31():
    text = ("- Foo\n"
            "- * * *\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.bullet_list, ([nodes.list_item, "Foo"],
                                                             [nodes.list_item, nodes.transition])])


def test_example_32():
    text = ("# foo\n"
            "## foo\n"
            "### foo\n"
            "#### foo\n"
            "##### foo\n"
            "###### foo\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.section, ([nodes.title, "foo"],
                                                         [nodes.section, ([nodes.title, "foo"],
                                                                          [nodes.section, ([nodes.title, "foo"],
                                                                                           nodes.section)])])])
    assert_node(result[0][1][1][1], [nodes.section, ([nodes.title, "foo"],
                                                     [nodes.section, ([nodes.title, "foo"],
                                                                      [nodes.section, nodes.title, "foo"])])])
    assert_node(result[0], nodes.section, depth=1)
    assert_node(result[0][1], nodes.section, depth=2)
    assert_node(result[0][1][1], nodes.section, depth=3)
    assert_node(result[0][1][1][1], nodes.section, depth=4)
    assert_node(result[0][1][1][1][1], nodes.section, depth=5)
    assert_node(result[0][1][1][1][1][1], nodes.section, depth=6)


def test_example_33():
    result = publish("####### foo")
    assert_node(result, [nodes.document, nodes.paragraph, "####### foo"])


def test_example_34():
    text = ("#5 bolt\n"
            "\n"
            "#hashtag\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.paragraph, "#5 bolt"],
                                          [nodes.paragraph, "#hashtag"])])


def test_example_36():
    result = publish(r"# foo *bar* \*baz\*")
    assert_node(result, [nodes.document, nodes.section, nodes.title, ("foo ",
                                                                      [nodes.emphasis, "bar"],
                                                                      " *baz*")])


def test_example_37():
    result = publish("#                  foo                     ")
    assert_node(result, [nodes.document, nodes.section, nodes.title, "foo"])


def test_example_38():
    text = (" ### foo\n"
            "  ## foo\n"
            "   # foo\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.section, ([nodes.title, "foo"],
                                                           [nodes.section, nodes.title, "foo"])],
                                          [nodes.section, nodes.title, "foo"])])
    assert_node(result[0], nodes.section, depth=1)
    assert_node(result[0][1], nodes.section, depth=2)
    assert_node(result[1], nodes.section, depth=1)


def test_example_41():
    text = ("## foo ##\n"
            "  ###   bar    ###\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.section, ([nodes.title, "foo"],
                                                           [nodes.section, nodes.title, "bar"])])])


def test_example_42():
    text = ("# foo ##################################\n"
            "##### foo ##\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.section, ([nodes.title, "foo"],
                                                           [nodes.section, nodes.title, "foo"])])])


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
    assert_node(result, [nodes.document, ([nodes.section, ([nodes.title, "foo ###"],
                                                           [nodes.section, nodes.title, "foo ###"])],
                                          [nodes.section, nodes.title, "foo #"])])


def test_example_48():
    text = ("Foo bar\n"
            "# baz\n"
            "Bar foo\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.paragraph, "Foo bar"],
                                          [nodes.section, ([nodes.title, "baz"],
                                                           [nodes.paragraph, "Bar foo"])])])


def test_example_49():
    text = ("## \n"
            "#\n"
            "### ###\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.section, nodes.title],
                                          [nodes.section, (nodes.title,
                                                           [nodes.section, nodes.title])])])


def test_example_50():
    text = ("Foo *bar*\n"
            "=========\n"
            "\n"
            "Foo *bar*\n"
            "---------\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.section, ([nodes.title, ("Foo ",
                                                                        [nodes.emphasis, "bar"])],
                                                         [nodes.section, nodes.title, ("Foo ",
                                                                                       [nodes.emphasis, "bar"])])])
    assert_node(result[0], depth=1)
    assert_node(result[0][1], depth=2)


def test_example_51():
    text = ("Foo *bar\n"
            "baz*\n"
            "====\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.section, nodes.title, ("Foo ",
                                                                      [nodes.emphasis, "bar\nbaz"])])
    assert_node(result[0], depth=1)


def test_example_52():
    text = ("Foo\n"
            "-------------------------\n"
            "\n"
            "Foo\n"
            "=\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.section, nodes.title, "Foo"],
                                          [nodes.section, nodes.title, "Foo"])])
    assert_node(result[0], depth=1)
    assert_node(result[1], depth=1)


def test_example_53():
    text = ("   Foo\n"
            "---\n"
            "\n"
            "  Foo\n"
            "-----\n"
            "\n"
            "  Foo\n"
            "  ===\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.section, ([nodes.title, "Foo"],
                                                           [nodes.section, nodes.title, "Foo"])],
                                          [nodes.section, nodes.title, "Foo"])])


def test_example_54():
    text = ("    Foo\n"
            "    ---\n"
            "\n"
            "    Foo\n"
            "---\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.literal_block, "Foo\n---\n\nFoo\n"],
                                          nodes.transition)])


def test_example_55():
    text = ("Foo\n"
            "   ----      \n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.section, nodes.title, "Foo"])


def test_example_56():
    text = ("Foo\n"
            "    ---\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.paragraph, "Foo\n---"])


def test_example_58():
    text = ("Foo  \n"
            "-----\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.section, nodes.title, "Foo"])


def test_example_59():
    text = ("Foo\\\n"
            "----\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.section, nodes.title, "Foo\\"])


def test_example_60():
    text = ("""`Foo\n"""
            """----\n"""
            """`\n"""
            """\n"""
            """<a title="a lot\n"""
            """---\n"""
            """of dashes"/>\n""")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.section, ([nodes.title, "`Foo"],
                                                           [nodes.paragraph, "`"],
                                                           [nodes.section, ([nodes.title, """<a title="a lot"""],
                                                                            [nodes.paragraph, """of dashes"/>"""])])])])


def test_example_61():
    text = ("> Foo\n"
            "---\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.block_quote, nodes.paragraph, "Foo"],
                                          nodes.transition)])


def test_example_62():
    text = ("> foo\n"
            "bar\n"
            "===\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.block_quote, nodes.paragraph, "foo\nbar\n==="])


def test_example_63():
    text = ("- Foo\n"
            "---\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.bullet_list, nodes.list_item, "Foo"],
                                          nodes.transition)])


def test_example_65():
    text = ("---\n"
            "Foo\n"
            "---\n"
            "Bar\n"
            "---\n"
            "Baz\n")
    result = publish(text)
    assert_node(result, [nodes.document, (nodes.transition,
                                          [nodes.section, ([nodes.title, "Foo"],
                                                           [nodes.section, ([nodes.title, "Bar"],
                                                                            [nodes.paragraph, "Baz"])])])])


def test_example_66():
    text = ("\n"
            "====\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.paragraph, "===="])


def test_example_67():
    text = ("---\n"
            "---\n")
    result = publish(text)
    assert_node(result, [nodes.document, (nodes.transition,
                                          nodes.transition)])


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
    assert_node(result, [nodes.document, nodes.paragraph, "Foo\nbar"])


def test_example_83():
    text = ("    foo\n"
            "bar\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.literal_block, "foo\n"],
                                          [nodes.paragraph, "bar"])])


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
    assert_node(result, [nodes.document, nodes.paragraph, nodes.literal, "foo"])


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
                                          [nodes.paragraph, "bbb"])])


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


def test_example_107():
    text = ("``` ```\n"
            "aaa\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.paragraph, (nodes.literal,
                                                           "\naaa")])


def test_example_109():
    text = ("foo\n"
            "```\n"
            "bar\n"
            "```\n"
            "baz\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.paragraph, "foo"],
                                          [nodes.literal_block, "bar\n"],
                                          [nodes.paragraph, "baz"])])


def test_example_111():
    text = ("```ruby\n"
            "def foo(x)\n"
            "  return 3\n"
            "end\n"
            "```\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.literal_block, "def foo(x)\n  return 3\nend\n"])
    assert_node(result[0], nodes.literal_block, classes=["code", "language-ruby"])


def test_example_114():
    text = ("``` aa ```\n"
            "foo\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.paragraph, ([nodes.literal, "aa"],
                                                           "\nfoo")])


def test_example_114_2():
    text = ("~~~ aa ``` ~~~\n"
            "foo\n"
            "~~~\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.literal_block, "foo\n"])


def test_example_115():
    text = ("```\n"
            "``` aaa\n"
            "```\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.literal_block, "``` aaa\n"])


def test_example_159():
    text = ("""[foo]: /url "title"\n"""
            """\n"""
            """[foo]\n""")
    result = publish(text)
    assert_node(result, [nodes.document, (nodes.target,
                                          [nodes.paragraph, nodes.reference, "foo"])])
    assert_node(result[0], refuri="/url", title="title")
    assert_node(result[1][0], refuri="/url", reftitle="title")


def test_example_160():
    text = ("   [foo]: \n"
            "      /url  \n"
            "           'the title'  \n"
            "\n"
            "[foo]\n")
    result = publish(text)
    assert_node(result, [nodes.document, (nodes.target,
                                          [nodes.paragraph, nodes.reference, "foo"])])
    assert_node(result[0], refuri="/url", title="the title")
    assert_node(result[1][0], refuri="/url", reftitle="the title")


def test_example_161():
    text = ("[Foo*bar\\]]:my_(url) 'title (with parens)'\n"
            "\n"
            "[Foo*bar\\]]\n")
    result = publish(text)
    assert_node(result, [nodes.document, (nodes.target,
                                          [nodes.paragraph, nodes.reference, "Foo*bar]"])])
    assert_node(result[0], refuri="my_(url)", title="title (with parens)")
    assert_node(result[1][0], refuri="my_(url)", reftitle="title (with parens)")


def test_example_162():
    text = ("[Foo bar]:\n"
            "<my%20url>\n"
            "'title'\n"
            "\n"
            "[Foo bar]\n")
    result = publish(text)
    assert_node(result, [nodes.document, (nodes.target,
                                          [nodes.paragraph, nodes.reference, "Foo bar"])])
    assert_node(result[0], refuri="my%20url", title="title")
    assert_node(result[1][0], refuri="my%20url", reftitle="title")


def test_example_163():
    text = ("[foo]: /url '\n"
            "title\n"
            "line1\n"
            "line2\n"
            "'\n"
            "\n"
            "[foo]\n")
    result = publish(text)
    assert_node(result, [nodes.document, (nodes.target,
                                          [nodes.paragraph, nodes.reference, "foo"])])
    assert_node(result[0], refuri="/url", title="\ntitle\nline1\nline2\n")
    assert_node(result[1][0], refuri="/url", reftitle="\ntitle\nline1\nline2\n")


def test_example_164():
    text = ("[foo]: /url 'title\n"
            "\n"
            "with blank line'\n"
            "\n"
            "[foo]\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.paragraph, "[foo]: /url 'title"],
                                          [nodes.paragraph, "with blank line'"],
                                          [nodes.paragraph, "[foo]"])])


def test_example_165():
    text = ("[foo]:\n"
            "/url\n"
            "\n"
            "[foo]\n")
    result = publish(text)
    assert_node(result, [nodes.document, (nodes.target,
                                          [nodes.paragraph, nodes.reference, "foo"])])
    assert_node(result[0], refuri="/url")
    assert_node(result[1][0], refuri="/url")


def test_example_166():
    text = ("[foo]:\n"
            "\n"
            "[foo]\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.paragraph, "[foo]:"],
                                          [nodes.paragraph, "[foo]"])])


def test_example_167():
    text = ("""[foo]: /url\\bar\\*baz "foo\\"bar\\baz"\n"""
            """\n"""
            """[foo]\n""")
    result = publish(text)
    assert_node(result, [nodes.document, (nodes.target,
                                          [nodes.paragraph, nodes.reference, "foo"])])
    assert_node(result[0], refuri="/url%5Cbar*baz", title='foo"bar\\baz')
    assert_node(result[1][0], refuri="/url%5Cbar*baz", reftitle='foo"bar\\baz')


def test_example_168():
    text = ("[foo]\n"
            "\n"
            "[foo]: url\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.paragraph, nodes.reference, "foo"],
                                          nodes.target)])
    assert_node(result[1], refuri="url")
    assert_node(result[0][0], refuri="url")


def test_example_169():
    text = ("[foo]\n"
            "\n"
            "[foo]: first\n"
            "[foo]: second\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.paragraph, nodes.reference, "foo"],
                                          nodes.target,
                                          nodes.target)])
    assert_node(result[1], refuri="first")
    assert_node(result[2], refuri="second")
    assert_node(result[0][0], refuri="first")


def test_example_170():
    text = ("[FOO]: /url\n"
            "\n"
            "[Foo]\n")
    result = publish(text)
    assert_node(result, [nodes.document, (nodes.target,
                                          [nodes.paragraph, nodes.reference, "Foo"])])
    assert_node(result[0], refuri="/url")
    assert_node(result[1][0], refuri="/url")


def test_example_171():
    text = ("[ΑΓΩ]: /φου\n"
            "\n"
            "[αγω]\n")
    result = publish(text)
    assert_node(result, [nodes.document, (nodes.target,
                                          [nodes.paragraph, nodes.reference, "αγω"])])
    assert_node(result[0], refuri="/%CF%86%CE%BF%CF%85")
    assert_node(result[1][0], refuri="/%CF%86%CE%BF%CF%85")


def test_example_172():
    result = publish("[foo]: /url")
    assert_node(result, [nodes.document, nodes.target])


def test_example_173():
    text = ("[\n"
            "foo\n"
            "]: /url\n"
            "bar\n")
    result = publish(text)
    assert_node(result, [nodes.document, (nodes.target,
                                          [nodes.paragraph, "bar"])])


def test_example_174():
    result = publish('[foo]: /url "title" ok')
    assert_node(result, [nodes.document, nodes.paragraph, '[foo]: /url "title" ok'])


def test_example_175():
    text = ('[foo]: /url\n'
            '"title" ok\n')
    result = publish(text)
    assert_node(result, [nodes.document, (nodes.target,
                                          [nodes.paragraph, '"title" ok'])])


def test_example_176():
    text = ('    [foo]: /url "title"\n'
            '\n'
            '[foo]\n')
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.literal_block, '[foo]: /url "title"\n'],
                                          [nodes.paragraph, "[foo]"])])


def test_example_177():
    text = ("```\n"
            "[foo]: /url\n"
            "```\n"
            "\n"
            "[foo]\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.literal_block, "[foo]: /url\n"],
                                          [nodes.paragraph, "[foo]"])])


def test_example_178():
    text = ("Foo\n"
            "[bar]: /baz\n"
            "\n"
            "[bar]\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.paragraph, "Foo\n[bar]: /baz"],
                                          [nodes.paragraph, "[bar]"])])


def test_example_179():
    text = ("# [Foo]\n"
            "[foo]: /url\n"
            "> bar\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.section, ([nodes.title, nodes.reference, "Foo"],
                                                         nodes.target,
                                                         [nodes.block_quote, nodes.paragraph, "bar"])])


def test_example_180():
    text = ("""[foo]: /foo-url "foo"\n"""
            """[bar]: /bar-url\n"""
            """  "bar"\n"""
            """[baz]: /baz-url\n"""
            """\n"""
            """[foo],\n"""
            """[bar],\n"""
            """[baz]\n""")
    result = publish(text)
    assert_node(result, [nodes.document, (nodes.target,
                                          nodes.target,
                                          nodes.target,
                                          [nodes.paragraph, ([nodes.reference, "foo"],
                                                             ",\n",
                                                             [nodes.reference, "bar"],
                                                             ",\n",
                                                             [nodes.reference, "baz"])])])


def test_example_181():
    text = ("[foo]\n"
            "\n"
            "> [foo]: /url\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.paragraph, nodes.reference, "foo"],
                                          [nodes.block_quote, ()])])
