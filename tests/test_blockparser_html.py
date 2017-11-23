# -*- coding: utf-8 -*-
"""
    test_blockparser_html
    ~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2017 by Takeshi KOMIYA
    :license: BSD, see LICENSE for details.
"""

from docutils import nodes
from utils import publish, assert_node


# TODO: add test for breaking by a blank line (Example 116)


def test_example_117():
    text = ("<table>\n"
            "  <tr>\n"
            "    <td>\n"
            "           hi\n"
            "    </td>\n"
            "  </tr>\n"
            "</table>\n"
            "\n"
            "okay.\n")
    result = publish(text)
    assert_node(result, [nodes.document, (nodes.raw,
                                          [nodes.paragraph, "okay."])])
    assert result[0][0] == ("<table>\n"
                            "  <tr>\n"
                            "    <td>\n"
                            "           hi\n"
                            "    </td>\n"
                            "  </tr>\n"
                            "</table>\n")


def test_example_118():
    text = (" <div>\n"
            "  *hello*\n"
            "         <foo><a>\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.raw, text])
    assert_node(result[0], nodes.raw, format='html')


def test_example_119():
    text = ("</div>\n"
            "*foo*\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.raw, text])


def test_example_121():
    text = ("""<div id="foo"\n"""
            """  class="bar">\n"""
            """</div>\n""")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.raw, text])


def test_example_124():
    text = ("""<div id="foo"\n"""
            """*hi*\n""")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.raw, text])


def test_example_129():
    text = ("""<div></div>\n"""
            """``` c\n"""
            """int x = 33;\n"""
            """```\n""")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.raw, text])


def test_example_131():
    text = ("""<Warning>\n"""
            """*bar*\n"""
            """</Warning>\n""")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.raw, text])

# TODO: add test for standard tags and inline notation (Example 136)


def test_example_137():
    text = ("""<pre language="haskell"><code>\n"""
            """import Text.HTML.TagSoup\n"""
            """\n"""
            """main :: IO ()\n"""
            """main = print $ parseTags tags\n"""
            """</code></pre>\n"""
            """okay\n""")
    result = publish(text)
    assert_node(result, [nodes.document, (nodes.raw,
                                          [nodes.paragraph, "okay"])])


def test_example_139():
    text = ("""<style\n"""
            """  type="text/css">\n"""
            """h1 {color:red;}\n"""
            """\n"""
            """p {color:blue;}\n"""
            """</style>\n"""
            """okay\n""")
    result = publish(text)
    assert_node(result, [nodes.document, (nodes.raw,
                                          [nodes.paragraph, "okay"])])


def test_example_138():
    text = ("""<script type="text/javascript">\n"""
            """// JavaScript example\n"""
            """\n"""
            """document.getElementById("demo").innerHTML = "Hello JavaScript!";\n"""
            """</script>\n"""
            """okay\n""")
    result = publish(text)
    assert_node(result, [nodes.document, (nodes.raw,
                                          [nodes.paragraph, "okay"])])


def test_example_141():
    text = ("""> <div>\n"""
            """> foo\n"""
            """\n"""
            """bar\n""")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.block_quote, nodes.raw, "<div>\nfoo\n"],
                                          [nodes.paragraph, "bar"])])

# TODO: add test for bullet_list containing HTML tags (Example 142)

# TODO: add test for HTML tags containing paragraph (Example 143)


def test_example_145():
    text = ("""<script>\n"""
            """foo\n"""
            """</script>1. *bar*\n""")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.raw, text])


def test_example_146():
    text = ("""<!-- Foo\n"""
            """\n"""
            """bar\n"""
            """   baz -->\n"""
            """okay\n""")
    result = publish(text)
    assert_node(result, [nodes.document, (nodes.raw,
                                          [nodes.paragraph, "okay"])])


def test_example_147():
    text = ("""<?php\n"""
            """\n"""
            """  echo '>';\n"""
            """\n"""
            """?>\n"""
            """okay\n""")
    result = publish(text)
    assert_node(result, [nodes.document, (nodes.raw,
                                          [nodes.paragraph, "okay"])])


def test_example_148():
    text = "<!DOCTYPE html>"
    result = publish(text)
    assert_node(result, [nodes.document, nodes.raw, text])


def test_example_149():
    text = ("""<![CDATA[\n"""
            """function matchwo(a,b)\n"""
            """{\n"""
            """  if (a < b && a < 0) then {\n"""
            """    return 1;\n"""
            """\n"""
            """  } else {\n"""
            """\n"""
            """    return 0;\n"""
            """  }\n"""
            """}\n"""
            """]]>\n"""
            """okay\n""")
    result = publish(text)
    assert_node(result, [nodes.document, (nodes.raw,
                                          [nodes.paragraph, "okay"])])


def test_example_150():
    text = ("""  <!-- foo -->\n"""
            """\n"""
            """    <!-- foo -->\n""")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.raw, "  <!-- foo -->\n"],
                                          [nodes.literal_block, "<!-- foo -->\n"])])


def test_example_152():
    text = ("""Foo\n"""
            """<div>\n"""
            """bar\n"""
            """</div>\n""")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.paragraph, "Foo"],
                                          nodes.raw)])


def test_example_153():
    text = ("""<div>\n"""
            """bar\n"""
            """</div>\n"""
            """*foo*\n""")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.raw, text])


def test_example_154():
    text = ("""Foo\n"""
            """<a href="bar">\n"""
            """baz\n""")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.paragraph, text.strip()])


def test_example_157():
    text = ("<table>\n"
            "\n"
            "<tr>\n"
            "\n"
            "<td>\n"
            "Hi\n"
            "</td>\n"
            "\n"
            "</tr>\n"
            "\n"
            "</table>\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.raw, "<table>\n"],
                                          [nodes.raw, "<tr>\n"],
                                          [nodes.raw, "<td>\nHi\n</td>\n"],
                                          [nodes.raw, "</tr>\n"],
                                          [nodes.raw, "</table>\n"])])
