"""
    test_blockparser_container
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2017-2019 by Takeshi KOMIYA
    :license: Apache License 2.0, see LICENSE for details.
"""

from docutils import nodes
from utils import publish, assert_node


def test_example_191():
    text = ("> # Foo\n"
            "> bar\n"
            "> baz\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.block_quote, ([nodes.section, ([nodes.title, "Foo"],
                                                                              [nodes.paragraph, "bar\nbaz"])])])


def test_example_192():
    text = ("># Foo\n"
            ">bar\n"
            "> baz\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.block_quote, ([nodes.section, ([nodes.title, "Foo"],
                                                                              [nodes.paragraph, "bar\nbaz"])])])


def test_example_193():
    text = ("   > # Foo\n"
            "   > bar\n"
            " > baz\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.block_quote, ([nodes.section, ([nodes.title, "Foo"],
                                                                              [nodes.paragraph, "bar\nbaz"])])])


def test_example_195():
    text = ("> # Foo\n"
            "> bar\n"
            "baz\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.block_quote, ([nodes.section, ([nodes.title, "Foo"],
                                                                              [nodes.paragraph, "bar\nbaz"])])])


def test_example_196():
    text = ("> bar\n"
            "baz\n"
            "> foo\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.block_quote, nodes.paragraph, "bar\nbaz\nfoo"])


def test_example_197():
    text = ("> foo\n"
            "---\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.block_quote, nodes.paragraph, "foo"],
                                          nodes.transition)])


def test_example_198():
    text = ("> - foo\n"
            "- bar\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.block_quote, nodes.bullet_list, nodes.list_item, "foo"],
                                          [nodes.bullet_list, nodes.list_item, "bar"])])


def test_example_199():
    text = (">     foo\n"
            "    bar\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.block_quote, nodes.literal_block, "foo\n"],
                                          [nodes.literal_block, "bar\n"])])


def test_example_200():
    text = ("> ```\n"
            "foo\n"
            "```\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.block_quote, nodes.literal_block],
                                          [nodes.paragraph, "foo"],
                                          [nodes.literal_block])])


def test_example_201():
    text = ("> foo\n"
            "    - bar\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.block_quote, nodes.paragraph, "foo\n- bar"])


def test_example_203():
    text = (">\n"
            ">\n"
            ">\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.block_quote, ()])


def test_example_204():
    text = ("> foo\n"
            "\n"
            "> bar\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.block_quote, nodes.paragraph, "foo"],
                                          [nodes.block_quote, nodes.paragraph, "bar"])])


def test_example_205():
    text = ("foo\n"
            "> bar\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.paragraph, "foo"],
                                          [nodes.block_quote, nodes.paragraph, "bar"])])


def test_example_212():
    text = ("> bar\n"
            ">\n"
            "baz\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.block_quote, nodes.paragraph, "bar"],
                                          [nodes.paragraph, "baz"])])


def test_example_213():
    text = ("> > > foo\n"
            "bar\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.block_quote, nodes.block_quote,
                         nodes.block_quote, nodes.paragraph, "foo\nbar"])


def test_example_214():
    text = (">>> foo\n"
            "> bar\n"
            ">>baz\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.block_quote, nodes.block_quote,
                         nodes.block_quote, nodes.paragraph, "foo\nbar\nbaz"])


def test_example_215():
    text = (">     code\n"
            "\n"
            ">    not code\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.block_quote, nodes.literal_block, "code\n"],
                                          [nodes.block_quote, nodes.paragraph, "not code"])])


def test_example_217():
    text = ("1.  A paragraph\n"
            "    with two lines.\n"
            "\n"
            "        indented code\n"
            "\n"
            "    > A block quote.\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.enumerated_list, nodes.list_item])
    assert_node(result[0][0], [nodes.list_item, ([nodes.paragraph, "A paragraph\nwith two lines."],
                                                 [nodes.literal_block, "indented code\n"],
                                                 [nodes.block_quote, nodes.paragraph, "A block quote."])])


def test_example_218():
    text = ("- one\n"
            "\n"
            " two\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.bullet_list, nodes.list_item, "one"],
                                          [nodes.paragraph, "two"])])


def test_example_219():
    text = ("- one\n"
            "\n"
            "  two\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.bullet_list, nodes.list_item, ([nodes.paragraph, "one"],
                                                                              [nodes.paragraph, "two"])])


def test_example_220():
    text = (" -    one\n"
            "\n"
            "     two\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.bullet_list, nodes.list_item, "one"],
                                          [nodes.literal_block, " two\n"])])


def test_example_221():
    text = (" -    one\n"
            "\n"
            "      two\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.bullet_list, nodes.list_item, ([nodes.paragraph, "one"],
                                                                              [nodes.paragraph, "two"])])


def test_example_222():
    text = ("   > > 1.  one\n"
            ">>\n"
            ">>     two\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.block_quote, nodes.block_quote,
                         nodes.enumerated_list, nodes.list_item, ([nodes.paragraph, "one"],
                                                                  [nodes.paragraph, "two"])])


def test_example_223():
    text = (">>- one\n"
            ">>\n"
            "  >  > two\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.block_quote, nodes.block_quote,
                         ([nodes.bullet_list, nodes.list_item, "one"],
                          [nodes.paragraph, "two"])])


def test_example_224():
    text = ("-one\n"
            "\n"
            "2.two\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.paragraph, "-one"],
                                          [nodes.paragraph, "2.two"])])


def test_example_225():
    text = ("- foo\n"
            "\n"
            "\n"
            "  bar\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.bullet_list, nodes.list_item, ([nodes.paragraph, "foo"],
                                                                              [nodes.paragraph, "bar"])])


def test_example_226():
    text = ("1.  foo\n"
            "\n"
            "    ```\n"
            "    bar\n"
            "    ```\n"
            "\n"
            "    baz\n"
            "\n"
            "    > bam\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.enumerated_list, nodes.list_item,
                         ([nodes.paragraph, "foo"],
                          [nodes.literal_block, "bar\n"],
                          [nodes.paragraph, "baz"],
                          [nodes.block_quote, nodes.paragraph, "bam"])])


def test_example_228():
    result = publish("123456789. ok")
    assert_node(result, [nodes.document, nodes.enumerated_list, nodes.list_item, "ok"])
    assert_node(result[0], nodes.enumerated_list, start=123456789)


def test_example_229():
    text = ("1234567890. not ok\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.paragraph, text.strip()])


def test_example_230():
    result = publish("0. ok")
    assert_node(result, [nodes.document, nodes.enumerated_list, nodes.list_item, "ok"])
    assert_node(result[0], nodes.enumerated_list, start=0)


def test_example_231():
    result = publish("003. ok")
    assert_node(result, [nodes.document, nodes.enumerated_list, nodes.list_item, "ok"])
    assert_node(result[0], nodes.enumerated_list, start=3)


def test_example_232():
    text = ("-1. not ok")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.paragraph, text])


def test_example_233():
    text = ("- foo\n"
            "\n"
            "      bar\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.bullet_list, nodes.list_item, ([nodes.paragraph, "foo"],
                                                                              [nodes.literal_block, "bar\n"])])


def test_example_234():
    text = ("  10.  foo\n"
            "\n"
            "           bar\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.enumerated_list, nodes.list_item, ([nodes.paragraph, "foo"],
                                                                                  [nodes.literal_block, "bar\n"])])


def test_example_236():
    text = ("1.     indented code\n"
            "\n"
            "   paragraph\n"
            "\n"
            "       more code\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.enumerated_list, nodes.list_item,
                         ([nodes.literal_block, "indented code\n"],
                          [nodes.paragraph, "paragraph"],
                          [nodes.literal_block, "more code\n"])])


def test_example_239():
    text = ("-    foo\n"
            "\n"
            "  bar\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.bullet_list, nodes.list_item, "foo"],
                                          [nodes.paragraph, "bar"])])


def test_example_241():
    text = ("-\n"
            "  foo\n"
            "-\n"
            "  ```\n"
            "  bar\n"
            "  ```\n"
            "-\n"
            "      baz\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.bullet_list, ([nodes.list_item, "foo"],
                                                             [nodes.list_item, nodes.literal_block, "bar\n"],
                                                             [nodes.list_item, nodes.literal_block, "baz\n"])])


def test_example_242():
    text = ("-   \n"
            "  foo\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.bullet_list, nodes.list_item, "foo"])


def test_example_243():
    text = ("-   \n"
            "\n"
            "  foo\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.bullet_list, nodes.list_item],
                                          [nodes.paragraph, "foo"])])


def test_example_245():
    text = ("- foo\n"
            "-   \n"
            "- bar\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.bullet_list, ([nodes.list_item, "foo"],
                                                             nodes.list_item,
                                                             [nodes.list_item, "bar"])])


def test_example_246():
    text = ("1. foo\n"
            "2.\n"
            "3. bar\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.enumerated_list, ([nodes.list_item, "foo"],
                                                                 nodes.list_item,
                                                                 [nodes.list_item, "bar"])])


def test_example_247():
    result = publish("*")
    assert_node(result, [nodes.document, nodes.bullet_list, nodes.list_item])


def test_example_248():
    text = ("foo\n"
            "*\n"
            "\n"
            "foo\n"
            "1.\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.paragraph, "foo\n*"],
                                          [nodes.paragraph, "foo\n1."])])


def test_example_251():
    text = ("   1.  A paragraph\n"
            "       with two lines.\n"
            "\n"
            "           indented code\n"
            "\n"
            "       > A block quote.\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.enumerated_list, nodes.list_item,
                         ([nodes.paragraph, "A paragraph\nwith two lines."],
                          [nodes.literal_block, "indented code\n"],
                          [nodes.block_quote, nodes.paragraph, "A block quote."])])


def test_example_253():
    text = ("  1.  A paragraph\n"
            "with two lines.\n"
            "\n"
            "          indented code\n"
            "\n"
            "      > A block quote.\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.enumerated_list, nodes.list_item,
                         ([nodes.paragraph, "A paragraph\nwith two lines."],
                          [nodes.literal_block, "indented code\n"],
                          [nodes.block_quote, nodes.paragraph, "A block quote."])])


def test_example_254():
    text = ("  1.  A paragraph\n"
            "    with two lines.\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.enumerated_list, nodes.list_item, "A paragraph\nwith two lines."])


def test_example_255():
    text = ("> 1. > Blockquote\n"
            "continued here.\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.block_quote, nodes.enumerated_list, nodes.list_item,
                         nodes.block_quote, nodes.paragraph, "Blockquote\ncontinued here."])


def test_example_257():
    text = ("- foo\n"
            "  - bar\n"
            "    - baz\n"
            "      - boo\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.bullet_list, nodes.list_item, ("foo",
                                                                              [nodes.bullet_list, nodes.list_item])])
    assert_node(result[0][0][1][0], [nodes.list_item, ("bar",
                                                       [nodes.bullet_list, nodes.list_item])])
    assert_node(result[0][0][1][0][1][0], [nodes.list_item, ("baz",
                                                             [nodes.bullet_list, nodes.list_item, "boo"])])


def test_example_258():
    text = ("- foo\n"
            " - bar\n"
            "  - baz\n"
            "   - boo\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.bullet_list, ([nodes.list_item, "foo"],
                                                             [nodes.list_item, "bar"],
                                                             [nodes.list_item, "baz"],
                                                             [nodes.list_item, "boo"])])


def test_example_261():
    result = publish("- - foo")
    assert_node(result, [nodes.document, nodes.bullet_list, nodes.list_item,
                         nodes.bullet_list, nodes.list_item, "foo"])


def test_example_262():
    result = publish("1. - 2. foo")
    assert_node(result, [nodes.document, nodes.enumerated_list, nodes.list_item,
                         nodes.bullet_list, nodes.list_item, nodes.enumerated_list, nodes.list_item, "foo"])


def test_example_263():
    text = ("- # Foo\n"
            "- Bar\n"
            "  ---\n"
            "  baz\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.bullet_list,
                         ([nodes.list_item, nodes.section, nodes.title, "Foo"],
                          [nodes.list_item, nodes.section, ([nodes.title, "Bar"],
                                                            [nodes.paragraph, "baz"])])])


def test_example_264():
    text = ("- foo\n"
            "- bar\n"
            "+ baz\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.bullet_list, ([nodes.list_item, "foo"],
                                                               [nodes.list_item, "bar"])],
                                          [nodes.bullet_list, nodes.list_item, "baz"])])


def test_example_265():
    text = ("1. foo\n"
            "2. bar\n"
            "3) baz\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.enumerated_list, ([nodes.list_item, "foo"],
                                                                   [nodes.list_item, "bar"])],
                                          [nodes.enumerated_list, nodes.list_item, "baz"])])


def test_example_266():
    text = ("Foo\n"
            "- bar\n"
            "- baz\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.paragraph, "Foo"],
                                          [nodes.bullet_list, ([nodes.list_item, "bar"],
                                                               [nodes.list_item, "baz"])])])


def test_example_267():
    text = ("The number of windows in my house is\n"
            "14.  The number of doors is 6.\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.paragraph, text.strip()])


def test_example_268():
    text = ("The number of windows in my house is\n"
            "1.  The number of doors is 6.\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.paragraph, "The number of windows in my house is"],
                                          [nodes.enumerated_list, nodes.list_item, "The number of doors is 6."])])


def test_example_269():
    text = ("- foo\n"
            "\n"
            "- bar\n"
            "\n"
            "\n"
            "- baz\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.bullet_list, ([nodes.list_item, nodes.paragraph, "foo"],
                                                             [nodes.list_item, nodes.paragraph, "bar"],
                                                             [nodes.list_item, nodes.paragraph, "baz"])])


def test_example_270():
    text = ("- foo\n"
            "  - bar\n"
            "    - baz\n"
            "\n"
            "\n"
            "      bim\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.bullet_list, nodes.list_item,
                         ("foo",
                          [nodes.bullet_list, nodes.list_item,
                           ("bar",
                            [nodes.bullet_list, nodes.list_item, ([nodes.paragraph, "baz"],
                                                                  [nodes.paragraph, "bim"])])])])


def test_example_271():
    text = ("- a\n"
            " - b\n"
            "  - c\n"
            "   - d\n"
            "    - e\n"
            "   - f\n"
            "  - g\n"
            " - h\n"
            "- i\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.bullet_list, ([nodes.list_item, "a"],
                                                             [nodes.list_item, "b"],
                                                             [nodes.list_item, "c"],
                                                             [nodes.list_item, "d"],
                                                             [nodes.list_item, "e"],
                                                             [nodes.list_item, "f"],
                                                             [nodes.list_item, "g"],
                                                             [nodes.list_item, "h"],
                                                             [nodes.list_item, "i"])])


def test_example_274():
    text = ("1. a\n"
            "\n"
            "  2. b\n"
            "\n"
            "    3. c\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.enumerated_list, ([nodes.list_item, nodes.paragraph, "a"],
                                                                 [nodes.list_item, nodes.paragraph, "b"],
                                                                 [nodes.list_item, nodes.paragraph, "c"])])


def test_example_275():
    text = ("- a\n"
            "- b\n"
            "\n"
            "- c\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.bullet_list, ([nodes.list_item, nodes.paragraph, "a"],
                                                             [nodes.list_item, nodes.paragraph, "b"],
                                                             [nodes.list_item, nodes.paragraph, "c"])])


def test_example_276():
    text = ("* a\n"
            "*\n"
            "\n"
            "* c\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.bullet_list, ([nodes.list_item, nodes.paragraph, "a"],
                                                             [nodes.list_item],
                                                             [nodes.list_item, nodes.paragraph, "c"])])


def test_example_279():
    text = ("- a\n"
            "- ```\n"
            "  b\n"
            "\n"
            "\n"
            "  ```\n"
            "- c\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.bullet_list, ([nodes.list_item, "a"],
                                                             [nodes.list_item, nodes.literal_block, "b\n\n\n"],
                                                             [nodes.list_item, "c"])])


def test_example_280():
    text = ("- a\n"
            "  - b\n"
            "\n"
            "    c\n"
            "- d\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.bullet_list, ([nodes.list_item, ("a",
                                                                                [nodes.bullet_list, nodes.list_item])],
                                                             [nodes.list_item, "d"])])
    assert_node(result[0][0][1][0], [nodes.list_item, ([nodes.paragraph, "b"],
                                                       [nodes.paragraph, "c"])])


def test_example_282():
    text = ("- a\n"
            "  > b\n"
            "  ```\n"
            "  c\n"
            "  ```\n"
            "- d\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.bullet_list,
                         ([nodes.list_item, ("a",
                                             [nodes.block_quote, nodes.paragraph, "b"],
                                             [nodes.literal_block, "c\n"])],
                          [nodes.list_item, "d"])])


def test_example_286():
    text = ("* foo\n"
            "  * bar\n"
            "\n"
            "  baz\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.bullet_list, nodes.list_item,
                         ([nodes.paragraph, "foo"],
                          [nodes.bullet_list, nodes.list_item, "bar"],
                          [nodes.paragraph, "baz"])])
