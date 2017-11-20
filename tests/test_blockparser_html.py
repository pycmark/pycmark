# -*- coding: utf-8 -*-
"""
    test_blockparser_html
    ~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2017 by Takeshi KOMIYA
    :license: BSD, see LICENSE for details.
"""

from docutils import nodes
from utils import publish, assert_node


def test_html_blocks():
    # TODO: add test for breaking by a blank line (Example 116 and 117)

    # Example 118
    text = (" <div>\n"
            "  *hello*\n"
            "         <foo><a>\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.raw, text])
    assert_node(result[0], nodes.raw, format='html')

    # TODO: add test for starting with closing tag (Example 119)

    # Example 121
    text = ("""<div id="foo"\n"""
            """  class="bar">\n"""
            """</div>\n""")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.raw, text])

    # Example 124
    text = ("""<div id="foo"\n"""
            """*hi*\n""")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.raw, text])

    # Example 129
    text = ("""<div></div>\n"""
            """``` c\n"""
            """int x = 33;\n"""
            """```\n""")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.raw, text])

    # Example 131
    text = ("""<Warning>\n"""
            """*bar*\n"""
            """</Warning>\n""")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.raw, text])

    # TODO: add test for standard tags and inline notation (Example 136)

    # Example 148
    text = "<!DOCTYPE html>"
    result = publish(text)
    assert_node(result, [nodes.document, nodes.raw, text])

    # Example 148
    text = ("""  <!-- foo -->\n"""
            """\n"""
            """    <!-- foo -->\n""")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.raw, "  <!-- foo -->\n"],
                                          [nodes.literal_block, "<!-- foo -->\n"])])

    # TODO: add test for HTML tags containing paragraph
    # (Example 137, 138, 139, 141, 142, 143, 145, 146, 147, 149, 152, 153, 154, 157)
