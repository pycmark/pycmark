# -*- coding: utf-8 -*-
"""
    test_inlineparser_std
    ~~~~~~~~~~~~~~~~~~~~~

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


def test_example_314():
    result = publish("`foo`")
    assert_node(result, [nodes.document, nodes.paragraph, nodes.literal, "foo"])


def test_example_315():
    result = publish("`` foo ` bar  ``")
    assert_node(result, [nodes.document, nodes.paragraph, nodes.literal, "foo ` bar"])


def test_example_316():
    result = publish("` `` `")
    assert_node(result, [nodes.document, nodes.paragraph, nodes.literal, "``"])


def test_example_318():
    text = ("`foo   bar\n"
            "  baz`\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.paragraph, nodes.literal, "foo bar baz"])


def test_example_321():
    result = publish("`foo\`bar`")
    assert_node(result, [nodes.document, nodes.paragraph, ([nodes.literal, "foo\\"],
                                                           "bar`")])


def test_example_322():
    result = publish("*foo`*`")
    assert_node(result, [nodes.document, nodes.paragraph, ("*foo",
                                                           [nodes.literal, "*"])])


def test_example_323():
    result = publish("[not a `link](/foo`)")
    assert_node(result, [nodes.document, nodes.paragraph, ("[not a ",
                                                           [nodes.literal, "link](/foo"],
                                                           ")")])


def test_example_324():
    result = publish("""`<a href="`">`""")
    assert_node(result, [nodes.document, nodes.paragraph, ([nodes.literal, "<a href=\""],
                                                           "\">`")])

# TODO: add test for Example 325

# TODO: add test for Example 327


def test_example_328():
    result = publish("```foo``")
    assert_node(result, [nodes.document, nodes.paragraph, "```foo``"])


def test_example_329():
    result = publish("`foo")
    assert_node(result, [nodes.document, nodes.paragraph, "`foo"])


def test_example_330():
    result = publish("`foo``bar``")
    assert_node(result, [nodes.document, nodes.paragraph, ("`foo",
                                                           [nodes.literal, "bar"])])
