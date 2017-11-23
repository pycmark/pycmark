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


def test_example_331():
    result = publish("*foo bar*")
    assert_node(result, [nodes.document, nodes.paragraph, nodes.emphasis, "foo bar"])


def test_example_332():
    result = publish("a * foo bar*")
    assert_node(result, [nodes.document, nodes.paragraph, "a * foo bar*"])


def test_example_333():
    result = publish("""a*"foo"*""")
    assert_node(result, [nodes.document, nodes.paragraph, """a*"foo"*"""])


def test_example_334():
    result = publish("*\xa0a\xa0*")
    assert_node(result, [nodes.document, nodes.paragraph, "*\xa0a\xa0*"])


def test_example_335():
    result = publish("foo*bar*")
    assert_node(result, [nodes.document, nodes.paragraph, ("foo",
                                                           [nodes.emphasis, "bar"])])


def test_example_336():
    result = publish("5*6*78")
    assert_node(result, [nodes.document, nodes.paragraph, ("5",
                                                           [nodes.emphasis, "6"],
                                                           "78")])


def test_example_337():
    result = publish("_foo bar_")
    assert_node(result, [nodes.document, nodes.paragraph, nodes.emphasis, "foo bar"])


def test_example_340():
    result = publish("foo_bar_")
    assert_node(result, [nodes.document, nodes.paragraph, "foo_bar_"])


def test_example_344():
    result = publish("foo-_(bar)_")
    assert_node(result, [nodes.document, nodes.paragraph, ("foo-",
                                                           [nodes.emphasis, "(bar)"])])


def test_example_345():
    result = publish("_foo*")
    assert_node(result, [nodes.document, nodes.paragraph, "_foo*"])


def test_example_347():
    result = publish("*foo bar\n*")
    assert_node(result, [nodes.document, nodes.paragraph, "*foo bar\n*"])


def test_example_348():
    result = publish("*(*foo)")
    assert_node(result, [nodes.document, nodes.paragraph, "*(*foo)"])


def test_example_349():
    result = publish("*(*foo*)*")
    assert_node(result, [nodes.document, nodes.paragraph, nodes.emphasis, ("(",
                                                                           [nodes.emphasis, "foo"],
                                                                           ")")])


def test_example_353():
    result = publish("_(_foo_)_")
    assert_node(result, [nodes.document, nodes.paragraph, nodes.emphasis, ("(",
                                                                           [nodes.emphasis, "foo"],
                                                                           ")")])


def test_example_357():
    result = publish("_(bar)_.")
    assert_node(result, [nodes.document, nodes.paragraph, ([nodes.emphasis, "(bar)"],
                                                           ".")])


def test_example_358():
    result = publish("**foo bar**")
    assert_node(result, [nodes.document, nodes.paragraph, nodes.strong, "foo bar"])


def test_example_361():
    result = publish("foo**bar**")
    assert_node(result, [nodes.document, nodes.paragraph, ("foo",
                                                           [nodes.strong, "bar"])])


def test_example_362():
    result = publish("__foo bar__")
    assert_node(result, [nodes.document, nodes.paragraph, nodes.strong, "foo bar"])


def test_example_369():
    result = publish("__foo, __bar__, baz__")
    assert_node(result, [nodes.document, nodes.paragraph, nodes.strong, ("foo, ",
                                                                         [nodes.strong, "bar"],
                                                                         ", baz")])


def test_example_370():
    result = publish("foo-__(bar)__")
    assert_node(result, [nodes.document, nodes.paragraph, ("foo-",
                                                           [nodes.strong, "(bar)"])])


def test_example_373():
    result = publish("*(**foo**)*")
    assert_node(result, [nodes.document, nodes.paragraph, nodes.emphasis, ("(",
                                                                           [nodes.strong, "foo"],
                                                                           ")")])


def test_example_374():
    result = publish("**Gomphocarpus (*Gomphocarpus physocarpus*, syn.\n"
                     "*Asclepias physocarpa*)**")
    assert_node(result, [nodes.document, nodes.paragraph, nodes.strong, ("Gomphocarpus (",
                                                                         [nodes.emphasis, "Gomphocarpus physocarpus"],
                                                                         ", syn.\n",
                                                                         [nodes.emphasis, "Asclepias physocarpa"],
                                                                         ")")])

# TODO: add test for Example 384


def test_example_386():
    result = publish("_foo __bar__ baz_")
    assert_node(result, [nodes.document, nodes.paragraph, nodes.emphasis, ("foo ",
                                                                           [nodes.strong, "bar"],
                                                                           " baz")])


def test_example_388():
    result = publish("__foo_ bar_")
    assert_node(result, [nodes.document, nodes.paragraph, nodes.emphasis, ([nodes.emphasis, "foo"],
                                                                           " bar")])


def test_example_389():
    result = publish("*foo *bar**")
    assert_node(result, [nodes.document, nodes.paragraph, nodes.emphasis, ("foo ",
                                                                           [nodes.emphasis, "bar"])])


def test_example_392():
    result = publish("***foo** bar*")
    assert_node(result, [nodes.document, nodes.paragraph, nodes.emphasis, ([nodes.strong, "foo"],
                                                                           " bar")])


def test_example_393():
    result = publish("*foo **bar***")
    assert_node(result, [nodes.document, nodes.paragraph, nodes.emphasis, ("foo ",
                                                                           [nodes.strong, "bar"])])


def test_example_395():
    result = publish("*foo **bar *baz* bim** bop*")
    assert_node(result, [nodes.document, nodes.paragraph, nodes.emphasis, ("foo ",
                                                                           [nodes.strong, ("bar ",
                                                                                           [nodes.emphasis, "baz"],
                                                                                           " bim")],
                                                                           " bop")])

# TODO: add test for Example 396


def test_example_397():
    result = publish("** is not an empty emphasis")
    assert_node(result, [nodes.document, nodes.paragraph, "** is not an empty emphasis"])


def test_example_398():
    result = publish("**** is not an empty strong emphasis")
    assert_node(result, [nodes.document, nodes.paragraph, "**** is not an empty strong emphasis"])


def test_example_413():
    result = publish("foo ***")
    assert_node(result, [nodes.document, nodes.paragraph, "foo ***"])


def test_example_414():
    result = publish("foo *\**")
    assert_node(result, [nodes.document, nodes.paragraph, ("foo ",
                                                           [nodes.emphasis, "*"])])


def test_example_415():
    result = publish("foo *_*")
    assert_node(result, [nodes.document, nodes.paragraph, ("foo ",
                                                           [nodes.emphasis, "_"])])


def test_example_419():
    result = publish("**foo*")
    assert_node(result, [nodes.document, nodes.paragraph, ("*",
                                                           [nodes.emphasis, "foo"])])


def test_example_420():
    result = publish("*foo**")
    assert_node(result, [nodes.document, nodes.paragraph, ([nodes.emphasis, "foo"],
                                                           "*")])


def test_example_421():
    result = publish("***foo**")
    assert_node(result, [nodes.document, nodes.paragraph, ("*",
                                                           [nodes.strong, "foo"])])


def test_example_427():
    result = publish("foo _*_")
    assert_node(result, [nodes.document, nodes.paragraph, ("foo ",
                                                           [nodes.emphasis, "*"])])


def test_example_441():
    result = publish("****foo****")
    assert_node(result, [nodes.document, nodes.paragraph, nodes.strong, nodes.strong, "foo"])


def test_example_442():
    result = publish("____foo____")
    assert_node(result, [nodes.document, nodes.paragraph, nodes.strong, nodes.strong, "foo"])


def test_example_444():
    result = publish("***foo***")
    assert_node(result, [nodes.document, nodes.paragraph, nodes.emphasis, nodes.strong, "foo"])


def test_example_445():
    result = publish("_____foo_____")
    assert_node(result, [nodes.document, nodes.paragraph, nodes.emphasis, nodes.strong, nodes.strong, "foo"])


def test_example_446():
    result = publish("*foo _bar* baz_")
    assert_node(result, [nodes.document, nodes.paragraph, ([nodes.emphasis, "foo _bar"],
                                                           " baz_")])


def test_example_447():
    result = publish("*foo __bar *baz bim__ bam*")
    assert_node(result, [nodes.document, nodes.paragraph, nodes.emphasis, ("foo ",
                                                                           [nodes.strong, "bar *baz bim"],
                                                                           " bam")])


def test_example_448():
    result = publish("**foo **bar baz**")
    assert_node(result, [nodes.document, nodes.paragraph, ("**foo ",
                                                           [nodes.strong, "bar baz"])])


# TODO: Add test for Example 450, 451, 452 and 453


def test_example_455():
    result = publish("*a `*`*")
    assert_node(result, [nodes.document, nodes.paragraph, nodes.emphasis, ("a ",
                                                                           [nodes.literal, "*"])])


def test_example_456():
    result = publish("_a `_`_")
    assert_node(result, [nodes.document, nodes.paragraph, nodes.emphasis, ("a ",
                                                                           [nodes.literal, "_"])])
