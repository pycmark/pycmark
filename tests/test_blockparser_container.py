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


def test_list_items():
    # Example 217
    text = ("1.  A paragraph\n"
            "    with two lines.\n"
            "\n"
            "        indented code\n"
            "\n"
            "    > A block quote.\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.enumerated_list, nodes.list_item])
    assert_node(result[0][0], [nodes.list_item, ([nodes.paragraph, "A paragraph\nwith two lines.\n"],
                                                 [nodes.literal_block, "indented code\n"],
                                                 [nodes.block_quote, nodes.paragraph, "A block quote.\n"])])

    # Example 218
    text = ("- one\n"
            "\n"
            " two\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.bullet_list, nodes.list_item, nodes.paragraph, "one\n"],
                                          [nodes.paragraph, "two\n"])])

    # Example 219
    text = ("- one\n"
            "\n"
            "  two\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.bullet_list, nodes.list_item, ([nodes.paragraph, "one\n"],
                                                                              [nodes.paragraph, "two\n"])])

    # Example 220
    text = (" -    one\n"
            "\n"
            "     two\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.bullet_list, nodes.list_item, nodes.paragraph, "one\n"],
                                          [nodes.literal_block, " two\n"])])

    # Example 221
    text = (" -    one\n"
            "\n"
            "      two\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.bullet_list, nodes.list_item, ([nodes.paragraph, "one\n"],
                                                                              [nodes.paragraph, "two\n"])])

    # Example 222
    text = ("   > > 1.  one\n"
            ">>\n"
            ">>     two\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.block_quote, nodes.block_quote,
                         nodes.enumerated_list, nodes.list_item, ([nodes.paragraph, "one\n"],
                                                                  [nodes.paragraph, "two\n"])])

    # Example 223
    text = (">>- one\n"
            ">>\n"
            "  >  > two\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.block_quote, nodes.block_quote,
                         ([nodes.bullet_list, nodes.list_item, nodes.paragraph, "one\n"],
                          [nodes.paragraph, "two\n"])])

    # Example 224
    text = ("-one\n"
            "\n"
            "2.two\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.paragraph, "-one\n"],
                                          [nodes.paragraph, "2.two\n"])])

    # Example 225
    text = ("- foo\n"
            "\n"
            "\n"
            "  bar\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.bullet_list, nodes.list_item, ([nodes.paragraph, "foo\n"],
                                                                              [nodes.paragraph, "bar\n"])])

    # Example 226
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
                         ([nodes.paragraph, "foo\n"],
                          [nodes.literal_block, "bar\n"],
                          [nodes.paragraph, "baz\n"],
                          [nodes.block_quote, nodes.paragraph, "bam\n"])])

    # Example 228
    result = publish("123456789. ok")
    assert_node(result, [nodes.document, nodes.enumerated_list, nodes.list_item, nodes.paragraph, "ok"])
    assert_node(result[0], nodes.enumerated_list, start=123456789)

    # Example 229
    text = ("1234567890. not ok\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.paragraph, text])

    # Example 230
    result = publish("0. ok")
    assert_node(result, [nodes.document, nodes.enumerated_list, nodes.list_item, nodes.paragraph, "ok"])
    assert_node(result[0], nodes.enumerated_list, start=0)

    # Example 231
    result = publish("003. ok")
    assert_node(result, [nodes.document, nodes.enumerated_list, nodes.list_item, nodes.paragraph, "ok"])
    assert_node(result[0], nodes.enumerated_list, start=3)

    # Example 232
    text = ("-1. not ok")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.paragraph, text])

    # Example 233
    text = ("- foo\n"
            "\n"
            "      bar\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.bullet_list, nodes.list_item, ([nodes.paragraph, "foo\n"],
                                                                              [nodes.literal_block, "bar\n"])])

    # Example 234
    text = ("  10.  foo\n"
            "\n"
            "           bar\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.enumerated_list, nodes.list_item, ([nodes.paragraph, "foo\n"],
                                                                                  [nodes.literal_block, "bar\n"])])

    # Example 236
    text = ("1.     indented code\n"
            "\n"
            "   paragraph\n"
            "\n"
            "       more code\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.enumerated_list, nodes.list_item,
                         ([nodes.literal_block, "indented code\n"],
                          [nodes.paragraph, "paragraph\n"],
                          [nodes.literal_block, "more code\n"])])

    # Example 239
    text = ("-    foo\n"
            "\n"
            "  bar\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.bullet_list, nodes.list_item, nodes.paragraph, "foo\n"],
                                          [nodes.paragraph, "bar\n"])])

    # Example 241
    text = ("-\n"
            "  foo\n"
            "-\n"
            "  ```\n"
            "  bar\n"
            "  ```\n"
            "-\n"
            "      baz\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.bullet_list, ([nodes.list_item, nodes.paragraph, "foo\n"],
                                                             [nodes.list_item, nodes.literal_block, "bar\n"],
                                                             [nodes.list_item, nodes.literal_block, "baz\n"])])

    # Example 242
    text = ("-   \n"
            "  foo\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.bullet_list, nodes.list_item, nodes.paragraph, "foo\n"])

    # Example 243
    text = ("- foo\n"
            "-   \n"
            "- bar\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.bullet_list, ([nodes.list_item, nodes.paragraph, "foo\n"],
                                                             nodes.list_item,
                                                             [nodes.list_item, nodes.paragraph, "bar\n"])])

    # Example 244
    text = ("1. foo\n"
            "2.\n"
            "3. bar\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.enumerated_list, ([nodes.list_item, nodes.paragraph, "foo\n"],
                                                                 nodes.list_item,
                                                                 [nodes.list_item, nodes.paragraph, "bar\n"])])

    # Example 247
    result = publish("*")
    assert_node(result, [nodes.document, nodes.bullet_list, nodes.list_item])

    # Example 248
    text = ("foo\n"
            "*\n"
            "\n"
            "foo\n"
            "1.\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.paragraph, "foo\n*\n"],
                                          [nodes.paragraph, "foo\n1.\n"])])

    # Example 251
    text = ("   1.  A paragraph\n"
            "       with two lines.\n"
            "\n"
            "           indented code\n"
            "\n"
            "       > A block quote.\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.enumerated_list, nodes.list_item,
                         ([nodes.paragraph, "A paragraph\nwith two lines.\n"],
                          [nodes.literal_block, "indented code\n"],
                          [nodes.block_quote, nodes.paragraph, "A block quote.\n"])])

    # Example 253
    text = ("  1.  A paragraph\n"
            "with two lines.\n"
            "\n"
            "          indented code\n"
            "\n"
            "      > A block quote.\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.enumerated_list, nodes.list_item,
                         ([nodes.paragraph, "A paragraph\nwith two lines.\n"],
                          [nodes.literal_block, "indented code\n"],
                          [nodes.block_quote, nodes.paragraph, "A block quote.\n"])])

    # Example 254
    text = ("  1.  A paragraph\n"
            "    with two lines.\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.enumerated_list, nodes.list_item,
                         nodes.paragraph, "A paragraph\nwith two lines.\n"])

    # Example 255
    text = ("> 1. > Blockquote\n"
            "continued here.\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.block_quote, nodes.enumerated_list, nodes.list_item,
                         nodes.block_quote, nodes.paragraph, "Blockquote\ncontinued here.\n"])

    # Example 257
    text = ("- foo\n"
            "  - bar\n"
            "    - baz\n"
            "      - boo\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.bullet_list, nodes.list_item, ([nodes.paragraph, "foo\n"],
                                                                              [nodes.bullet_list, nodes.list_item])])
    assert_node(result[0][0][1][0], [nodes.list_item, ([nodes.paragraph, "bar\n"],
                                                       [nodes.bullet_list, nodes.list_item])])
    assert_node(result[0][0][1][0][1][0], [nodes.list_item, ([nodes.paragraph, "baz\n"],
                                                             [nodes.bullet_list, nodes.list_item])])
    assert_node(result[0][0][1][0][1][0][1][0], [nodes.list_item, nodes.paragraph, "boo\n"])

    # Example 258
    text = ("- foo\n"
            " - bar\n"
            "  - baz\n"
            "   - boo\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.bullet_list, ([nodes.list_item, nodes.paragraph, "foo\n"],
                                                             [nodes.list_item, nodes.paragraph, "bar\n"],
                                                             [nodes.list_item, nodes.paragraph, "baz\n"],
                                                             [nodes.list_item, nodes.paragraph, "boo\n"])])

    # Example 261
    result = publish("- - foo")
    assert_node(result, [nodes.document, nodes.bullet_list, nodes.list_item,
                         nodes.bullet_list, nodes.list_item, nodes.paragraph, "foo"])

    # Example 262
    result = publish("1. - 2. foo")
    assert_node(result, [nodes.document, nodes.enumerated_list, nodes.list_item,
                         nodes.bullet_list, nodes.list_item, nodes.enumerated_list, nodes.list_item,
                         nodes.paragraph, "foo"])

    # TODO: Add test for combination with heading (Example 263)


def test_list():
    # Example 264
    text = ("- foo\n"
            "- bar\n"
            "+ baz\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.bullet_list, ([nodes.list_item, nodes.paragraph, "foo\n"],
                                                               [nodes.list_item, nodes.paragraph, "bar\n"])],
                                          [nodes.bullet_list, nodes.list_item, nodes.paragraph, "baz\n"])])

    # Example 263
    text = ("1. foo\n"
            "2. bar\n"
            "3) baz\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.enumerated_list, ([nodes.list_item, nodes.paragraph, "foo\n"],
                                                                   [nodes.list_item, nodes.paragraph, "bar\n"])],
                                          [nodes.enumerated_list, nodes.list_item, nodes.paragraph, "baz\n"])])

    # Example 266
    text = ("Foo\n"
            "- bar\n"
            "- baz\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.paragraph, "Foo\n"],
                                          [nodes.bullet_list, ([nodes.list_item, nodes.paragraph, "bar\n"],
                                                               [nodes.list_item, nodes.paragraph, "baz\n"])])])

    # Example 267
    text = ("The number of windows in my house is\n"
            "14.  The number of doors is 6.\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.paragraph, text])

    # Example 267
    text = ("The number of windows in my house is\n"
            "1.  The number of doors is 6.\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.paragraph, "The number of windows in my house is\n"],
                                          [nodes.enumerated_list, nodes.list_item, nodes.paragraph,
                                           "The number of doors is 6.\n"])])

    # Example 269
    text = ("- foo\n"
            "\n"
            "- bar\n"
            "\n"
            "\n"
            "- baz\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.bullet_list, ([nodes.list_item, nodes.paragraph, "foo\n"],
                                                             [nodes.list_item, nodes.paragraph, "bar\n"],
                                                             [nodes.list_item, nodes.paragraph, "baz\n"])])

    # Example 270
    text = ("- foo\n"
            "  - bar\n"
            "    - baz\n"
            "\n"
            "\n"
            "      bim\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.bullet_list, nodes.list_item,
                         ([nodes.paragraph, "foo\n"],
                          [nodes.bullet_list, nodes.list_item,
                           ([nodes.paragraph, "bar\n"],
                            [nodes.bullet_list, nodes.list_item, ([nodes.paragraph, "baz\n"],
                                                                  [nodes.paragraph, "bim\n"])])])])

    # Example 271
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
    assert_node(result, [nodes.document, nodes.bullet_list, ([nodes.list_item, nodes.paragraph, "a\n"],
                                                             [nodes.list_item, nodes.paragraph, "b\n"],
                                                             [nodes.list_item, nodes.paragraph, "c\n"],
                                                             [nodes.list_item, nodes.paragraph, "d\n"],
                                                             [nodes.list_item, nodes.paragraph, "e\n"],
                                                             [nodes.list_item, nodes.paragraph, "f\n"],
                                                             [nodes.list_item, nodes.paragraph, "g\n"],
                                                             [nodes.list_item, nodes.paragraph, "h\n"],
                                                             [nodes.list_item, nodes.paragraph, "i\n"])])

    # Example 272
    text = ("1. a\n"
            "\n"
            "  2. b\n"
            "\n"
            "    3. c\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.enumerated_list, ([nodes.list_item, nodes.paragraph, "a\n"],
                                                                 [nodes.list_item, nodes.paragraph, "b\n"],
                                                                 [nodes.list_item, nodes.paragraph, "c\n"])])
