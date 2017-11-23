# -*- coding: utf-8 -*-
"""
    test_inlineparser
    ~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2017 by Takeshi KOMIYA
    :license: BSD, see LICENSE for details.
"""

from docutils import nodes
from utils import publish, assert_node


def test_example_289():
    text = r"""\!\"\#\$\%\&\'\(\)\*\+\,\-\.\/\:\;\<\=\>\?\@\[\\\]\^\_\`\{\|\}\~"""
    result = publish(text)
    assert_node(result, [nodes.document, nodes.paragraph, "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"])


def test_example_290():
    text = r"\→\A\a\ \3\φ\«"
    result = publish(text)
    assert_node(result, [nodes.document, nodes.paragraph, r"\→\A\a\ \3\φ\«"])


def test_example_291():
    text = ("""\\*not emphasized*\n"""
            """\\<br/> not a tag\n"""
            """\\[not a link](/foo)\n"""
            """\\`not code`\n"""
            """1\\. not a list\n"""
            """\\* not a list\n"""
            """\\# not a heading\n"""
            """\\[foo]: /url "not a reference"\n""")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.paragraph, ("*not emphasized*\n"
                                                           "<br/> not a tag\n"
                                                           "[not a link](/foo)\n"
                                                           "`not code`\n"
                                                           "1. not a list\n"
                                                           "* not a list\n"
                                                           "# not a heading\n"
                                                           "[foo]: /url \"not a reference\"")])
