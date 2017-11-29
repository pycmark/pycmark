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


def test_example_302():
    text = ("&nbsp; &amp; &copy; &AElig; &Dcaron;\n"
            "&frac34; &HilbertSpace; &DifferentialD;\n"
            "&ClockwiseContourIntegral; &ngE;\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.paragraph, ("\xa0 & © Æ Ď\n"
                                                           "¾ ℋ ⅆ\n"
                                                           "∲ ≧̸")])


def test_example_303():
    result = publish("&#35; &#1234; &#992; &#98765432; &#0;")
    assert_node(result, [nodes.document, nodes.paragraph, "# Ӓ Ϡ � �"])


def test_example_304():
    text = ("&nbsp &x; &#; &#x;\n"
            "&ThisIsNotDefined; &hi?;")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.paragraph, text])


def test_example_305():
    result = publish("&copy")
    assert_node(result, [nodes.document, nodes.paragraph, "&copy"])


def test_example_306():
    result = publish("&MadeUpEntity;")
    assert_node(result, [nodes.document, nodes.paragraph, "&MadeUpEntity;"])

# TODO: add test for combination with HTML tags and link (Example 308, 309, 310)


def test_example_311():
    text = ("``` f&ouml;&ouml;\n"
            "foo\n"
            "```\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.literal_block, "foo\n"])
    assert_node(result[0], classes=["language-föö"])


def test_example_312():
    result = publish("`f&ouml;&ouml;`")
    assert_node(result, [nodes.document, nodes.paragraph, nodes.literal, "f&ouml;&ouml;"])


def test_example_313():
    result = publish("    f&ouml;f&ouml;")
    assert_node(result, [nodes.document, nodes.literal_block, "f&ouml;f&ouml;"])


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


def test_example_459():
    result = publish("""[link](/uri "title")""")
    assert_node(result, [nodes.document, nodes.paragraph, nodes.reference, "link"])
    assert_node(result[0][0], refuri="/uri", reftitle='title')


def test_example_460():
    result = publish("[link](/uri)")
    assert_node(result, [nodes.document, nodes.paragraph, nodes.reference, "link"])
    assert_node(result[0][0], refuri="/uri")


def test_example_461():
    result = publish("[link]()")
    assert_node(result, [nodes.document, nodes.paragraph, nodes.reference, "link"])
    assert_node(result[0][0], refuri="")


def test_example_462():
    result = publish("[link](<>)")
    assert_node(result, [nodes.document, nodes.paragraph, nodes.reference, "link"])
    assert_node(result[0][0], refuri="")


def test_example_463():
    text = "[link](/my uri)"
    result = publish(text)
    assert_node(result, [nodes.document, nodes.paragraph, text])


def test_example_464():
    text = "[link](</my uri>)"
    result = publish(text)
    assert_node(result, [nodes.document, nodes.paragraph, text])


def test_example_465():
    text = ("[link](foo\n"
            "bar)\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.paragraph, text.strip()])


def test_example_466():
    text = ("[link](<foo\n"
            "bar>)\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.paragraph, text.strip()])


def test_example_467():
    result = publish("[link](\(foo\))")
    assert_node(result, [nodes.document, nodes.paragraph, nodes.reference, "link"])
    assert_node(result[0][0], refuri="(foo)")


def test_example_468():
    result = publish("[link](foo(and(bar)))")
    assert_node(result, [nodes.document, nodes.paragraph, nodes.reference, "link"])
    assert_node(result[0][0], refuri="foo(and(bar))")


def test_example_469():
    result = publish("[link](foo\(and\(bar\))")
    assert_node(result, [nodes.document, nodes.paragraph, nodes.reference, "link"])
    assert_node(result[0][0], refuri="foo(and(bar)")


def test_example_470():
    result = publish("[link](<foo(and(bar)>)")
    assert_node(result, [nodes.document, nodes.paragraph, nodes.reference, "link"])
    assert_node(result[0][0], refuri="foo(and(bar)")


def test_example_471():
    result = publish("[link](foo\)\:)")
    assert_node(result, [nodes.document, nodes.paragraph, nodes.reference, "link"])
    assert_node(result[0][0], refuri="foo):")


def test_example_472():
    text = ("[link](#fragment)\n"
            "\n"
            "[link](http://example.com#fragment)\n"
            "\n"
            "[link](http://example.com?foo=3#frag)\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.paragraph, nodes.reference, "link"],
                                          [nodes.paragraph, nodes.reference, "link"],
                                          [nodes.paragraph, nodes.reference, "link"])])
    assert_node(result[0][0], refuri="#fragment")
    assert_node(result[1][0], refuri="http://example.com#fragment")
    assert_node(result[2][0], refuri="http://example.com?foo=3#frag")


def test_example_473():
    result = publish("[link](foo\bar)")
    assert_node(result, [nodes.document, nodes.paragraph, nodes.reference, "link"])
    assert_node(result[0][0], refuri="foo\bar")


def test_example_474():
    result = publish("[link](foo%20b&auml;)")
    assert_node(result, [nodes.document, nodes.paragraph, nodes.reference, "link"])
    assert_node(result[0][0], refuri="foo%20bä")


def test_example_474_2():
    result = publish("[link](<foo%20b&auml;>)")
    assert_node(result, [nodes.document, nodes.paragraph, nodes.reference, "link"])
    assert_node(result[0][0], refuri="foo%20bä")


def test_example_475():
    result = publish("""[link]("title")""")
    assert_node(result, [nodes.document, nodes.paragraph, nodes.reference, "link"])
    assert_node(result[0][0], refuri='"title"')


def test_example_476():
    text = ("""[link](/url "title")\n"""
            """[link](/url 'title')\n"""
            """[link](/url (title))\n""")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.paragraph, ([nodes.reference, "link"],
                                                           "\n",
                                                           [nodes.reference, "link"],
                                                           "\n",
                                                           [nodes.reference, "link"])])
    assert_node(result[0][0], refuri="/url", reftitle="title")
    assert_node(result[0][2], refuri="/url", reftitle="title")
    assert_node(result[0][4], refuri="/url", reftitle="title")


def test_example_477():
    result = publish("""[link](/url "title \\"&quot;")""")
    assert_node(result, [nodes.document, nodes.paragraph, nodes.reference, "link"])
    assert_node(result[0][0], refuri="/url", reftitle='title ""')


def test_example_478():
    result = publish("""[link](/url\xa0"title")""")
    assert_node(result, [nodes.document, nodes.paragraph, nodes.reference, "link"])
    assert_node(result[0][0], refuri='/url\xa0"title"')


def test_example_479():
    text = '[link](/url "title "and" title")'
    result = publish(text)
    assert_node(result, [nodes.document, nodes.paragraph, text])


def test_example_480():
    result = publish("""[link](/url 'title "and" title')""")
    assert_node(result, [nodes.document, nodes.paragraph, nodes.reference, "link"])
    assert_node(result[0][0], refuri="/url", reftitle='title "and" title')


def test_example_481():
    text = ('[link](   /uri\n'
            '  "title"  )\n')
    result = publish(text)
    assert_node(result, [nodes.document, nodes.paragraph, nodes.reference, "link"])
    assert_node(result[0][0], refuri="/uri", reftitle="title")


def test_example_482():
    result = publish("[link] (/uri)")
    assert_node(result, [nodes.document, nodes.paragraph, "[link] (/uri)"])


def test_example_483():
    result = publish("[link [foo [bar]]](/uri)")
    assert_node(result, [nodes.document, nodes.paragraph, nodes.reference, "link [foo [bar]]"])
    assert_node(result[0][0], refuri="/uri")


def test_example_484():
    result = publish("[link] bar](/uri)")
    assert_node(result, [nodes.document, nodes.paragraph, "[link] bar](/uri)"])


def test_example_485():
    result = publish("[link [bar](/uri)")
    assert_node(result, [nodes.document, nodes.paragraph, ("[link ",
                                                           [nodes.reference, "bar"])])


def test_example_486():
    result = publish("[link \\[bar](/uri)")
    assert_node(result, [nodes.document, nodes.paragraph, nodes.reference, "link [bar"])


def test_example_487():
    result = publish("[link *foo **bar** `#`*](/uri)")
    assert_node(result, [nodes.document, nodes.paragraph, nodes.reference, ("link ",
                                                                            [nodes.emphasis, ("foo ",
                                                                                              [nodes.strong, "bar"],
                                                                                              " ",
                                                                                              [nodes.literal, "#"])])])


# TODO: add test for combination with image (Example 488)


def test_example_489():
    result = publish("[foo [bar](/uri)](/uri)")
    assert_node(result, [nodes.document, nodes.paragraph, ("[foo ",
                                                           [nodes.reference, "bar"],
                                                           "](/uri)")])


def test_example_490():
    result = publish("[foo *[bar [baz](/uri)](/uri)*](/uri)")
    assert_node(result, [nodes.document, nodes.paragraph, ("[foo ",
                                                           [nodes.emphasis, ("[bar ",
                                                                             [nodes.reference, "baz"],
                                                                             "](/uri)")],
                                                           "](/uri)")])

# TODO: add test for combination with image (Example 491)


def test_example_492():
    result = publish("*[foo*](/uri)")
    assert_node(result, [nodes.document, nodes.paragraph, ("*",
                                                           [nodes.reference, "foo*"])])


def test_example_493():
    result = publish("[foo *bar](baz*)")
    assert_node(result, [nodes.document, nodes.paragraph, nodes.reference, "foo *bar"])
    assert_node(result[0][0], refuri="baz*")


def test_example_494():
    result = publish("*foo [bar* baz]")
    assert_node(result, [nodes.document, nodes.paragraph, ([nodes.emphasis, "foo [bar"],
                                                           " baz]")])


# TODO: add test for combination with HTML tags (Example 495)


def test_example_496():
    result = publish("[foo`](/uri)`")
    assert_node(result, [nodes.document, nodes.paragraph, ("[foo",
                                                           [nodes.literal, "](/uri)"])])


# TODO: add test for combination with HTML tags (Example 497)


def test_example_499():
    text = ("[link [foo [bar]]][ref]\n"
            "\n"
            "[ref]: /uri\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.paragraph, nodes.reference, "link [foo [bar]]"],
                                          nodes.target)])
    assert_node(result[0][0], refuri="/uri")


def test_example_500():
    text = ("[link \\[bar][ref]\n"
            "\n"
            "[ref]: /uri\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.paragraph, nodes.reference, "link [bar"],
                                          nodes.target)])
    assert_node(result[0][0], refuri="/uri")


def test_example_501():
    text = ("[link *foo **bar** `#`*][ref]\n"
            "\n"
            "[ref]: /uri\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.paragraph, nodes.reference, ("link ",
                                                                              [nodes.emphasis, ("foo ",
                                                                                                [nodes.strong, "bar"],
                                                                                                " ",
                                                                                                [nodes.literal, "#"]
                                                                                                )])],
                                          nodes.target)])
    assert_node(result[0][0], refuri="/uri")


def test_example_502():
    text = ("[![moon](moon.jpg)][ref]\n"
            "\n"
            "[ref]: /uri\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.paragraph, nodes.reference, nodes.image],
                                          nodes.target)])
    assert_node(result[0][0], refuri="/uri")
    assert_node(result[0][0][0], uri="moon.jpg", alt="moon")


def test_example_503():
    text = ("[foo [bar](/uri)][ref]\n"
            "\n"
            "[ref]: /uri\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.paragraph, ("[foo ",
                                                             [nodes.reference, "bar"],
                                                             "]",
                                                             [nodes.reference, "ref"])],
                                          nodes.target)])
    assert_node(result[0][1], refuri="/uri")
    assert_node(result[0][3], refuri="/uri")


def test_example_504():
    text = ("[foo *bar [baz][ref]*][ref]\n"
            "\n"
            "[ref]: /uri\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.paragraph, ("[foo ",
                                                             [nodes.emphasis, ("bar ",
                                                                               [nodes.reference, "baz"])],
                                                             "]",
                                                             [nodes.reference, "ref"])],
                                          nodes.target)])


def test_example_505():
    text = ("*[foo*][ref]\n"
            "\n"
            "[ref]: /uri\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.paragraph, ("*",
                                                             [nodes.reference, "foo*"])],
                                          nodes.target)])


def test_example_506():
    text = ("[foo *bar][ref]\n"
            "\n"
            "[ref]: /uri\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.paragraph, nodes.reference, "foo *bar"],
                                          nodes.target)])


# TODO: add test for combination with HTML tags (Example 507)


def test_example_508():
    text = ("[foo`][ref]`\n"
            "\n"
            "[ref]: /uri\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.paragraph, ("[foo",
                                                             [nodes.literal, "][ref]"])],
                                          nodes.target)])


# TODO: add test for combination with HTML tags (Example 509)


def test_example_510():
    text = ("""[foo][BaR]\n"""
            """\n"""
            """[bar]: /url "title"\n""")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.paragraph, nodes.reference, "foo"],
                                          nodes.target)])
    assert_node(result[0][0], refuri="/url", reftitle="title")


def test_example_511():
    text = ("[Толпой][Толпой] is a Russian word.\n"
            "\n"
            "[ТОЛПОЙ]: /url\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.paragraph, ([nodes.reference, "Толпой"],
                                                             " is a Russian word.")],
                                          nodes.target)])
    assert_node(result[0][0], refuri="/url")


def test_example_512():
    text = ("[Foo\n"
            "  bar]: /url\n"
            "\n"
            "[Baz][Foo bar]\n")
    result = publish(text)
    assert_node(result, [nodes.document, (nodes.target,
                                          [nodes.paragraph, nodes.reference, "Baz"])])
    assert_node(result[1][0], refuri="/url")


def test_example_513():
    text = ("""[foo] [bar]\n"""
            """\n"""
            """[bar]: /url "title"\n""")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.paragraph, ("[foo] ",
                                                             [nodes.reference, "bar"])],
                                          nodes.target)])
    assert_node(result[0][1], refuri="/url", reftitle="title")


def test_example_514():
    text = ("""[foo]\n"""
            """[bar]\n"""
            """\n"""
            """[bar]: /url "title"\n""")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.paragraph, ("[foo]\n",
                                                             [nodes.reference, "bar"])],
                                          nodes.target)])
    assert_node(result[0][1], refuri="/url", reftitle="title")


def test_example_515():
    text = ("[foo]: /url1\n"
            "\n"
            "[foo]: /url2\n"
            "\n"
            "[bar][foo]\n")
    result = publish(text)
    assert_node(result, [nodes.document, (nodes.target,
                                          nodes.target,
                                          [nodes.paragraph, nodes.reference, "bar"])])
    assert_node(result[2][0], refuri="/url1")


def test_example_516():
    text = ("[bar][foo\\!]\n"
            "\n"
            "[foo!]: /url\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.paragraph, nodes.reference, "bar"],
                                          nodes.target)])
    assert_node(result[0][0], refuri="/url")


def test_example_517():
    text = ("[foo][ref[]\n"
            "\n"
            "[ref[]: /uri\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.paragraph, "[foo][ref[]"],
                                          [nodes.paragraph, "[ref[]: /uri"])])


def test_example_518():
    text = ("[foo][ref[bar]]\n"
            "\n"
            "[ref[bar]]: /uri\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.paragraph, "[foo][ref[bar]]"],
                                          [nodes.paragraph, "[ref[bar]]: /uri"])])


def test_example_519():
    text = ("[[[foo]]]\n"
            "\n"
            "[[[foo]]]: /url\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.paragraph, "[[[foo]]]"],
                                          [nodes.paragraph, "[[[foo]]]: /url"])])


def test_example_520():
    text = ("[foo][ref\\[]\n"
            "\n"
            "[ref\\[]: /uri\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.paragraph, nodes.reference, "foo"],
                                          nodes.target)])


def test_example_521():
    text = ("[bar\\\\]: /uri\n"
            "\n"
            "[bar\\\\]\n")
    result = publish(text)
    assert_node(result, [nodes.document, (nodes.target,
                                          [nodes.paragraph, nodes.reference, "bar\\"])])


def test_example_522():
    text = ("[]\n"
            "\n"
            "[]: /uri\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.paragraph, "[]"],
                                          [nodes.paragraph, "[]: /uri"])])


def test_example_523():
    text = ("[\n"
            " ]\n"
            "\n"
            "[\n"
            " ]: /uri\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.paragraph, "[\n]"],
                                          [nodes.paragraph, "[\n]: /uri"])])


def test_example_524():
    text = ("""[foo][]\n"""
            """\n"""
            """[foo]: /url "title"\n""")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.paragraph, nodes.reference, "foo"],
                                          nodes.target)])
    assert_node(result[0][0], refuri="/url", reftitle="title")


def test_example_525():
    text = ("""[*foo* bar][]\n"""
            """\n"""
            """[*foo* bar]: /url "title"\n""")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.paragraph, nodes.reference, ([nodes.emphasis, "foo"],
                                                                              " bar")],
                                          nodes.target)])
    assert_node(result[0][0], refuri="/url", reftitle="title")


def test_example_526():
    text = ("""[Foo][]\n"""
            """\n"""
            """[foo]: /url "title"\n""")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.paragraph, nodes.reference, "Foo"],
                                          nodes.target)])
    assert_node(result[0][0], refuri="/url", reftitle="title")


def test_example_527():
    text = ("""[foo] \n"""
            """[]\n"""
            """\n"""
            """[foo]: /url "title"\n""")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.paragraph, ([nodes.reference, "foo"],
                                                             " \n[]")],
                                          nodes.target)])
    assert_node(result[0][0], refuri="/url", reftitle="title")


def test_example_528():
    text = ("""[foo]\n"""
            """\n"""
            """[foo]: /url "title"\n""")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.paragraph, nodes.reference, "foo"],
                                          nodes.target)])
    assert_node(result[0][0], refuri="/url", reftitle="title")


def test_example_529():
    text = ("""[*foo* bar]\n"""
            """\n"""
            """[*foo* bar]: /url "title"\n""")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.paragraph, nodes.reference, ([nodes.emphasis, "foo"],
                                                                              " bar")],
                                          nodes.target)])
    assert_node(result[0][0], refuri="/url", reftitle="title")


def test_example_530():
    text = ("""[[*foo* bar]]\n"""
            """\n"""
            """[*foo* bar]: /url "title"\n""")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.paragraph, ("[",
                                                             [nodes.reference, ([nodes.emphasis, "foo"],
                                                                                " bar")],
                                                             "]")],
                                          nodes.target)])
    assert_node(result[0][1], refuri="/url", reftitle="title")


def test_example_531():
    text = ("[[bar [foo]\n"
            "\n"
            "[foo]: /url\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.paragraph, ("[[bar ",
                                                             [nodes.reference, "foo"])],
                                          nodes.target)])
    assert_node(result[0][1], refuri="/url")


def test_example_532():
    text = ("""[Foo]\n"""
            """\n"""
            """[foo]: /url "title"\n""")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.paragraph, nodes.reference, "Foo"],
                                          nodes.target)])
    assert_node(result[0][0], refuri="/url", reftitle="title")


def test_example_533():
    text = ("[foo] bar\n"
            "\n"
            "[foo]: /url\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.paragraph, ([nodes.reference, "foo"],
                                                             " bar")],
                                          nodes.target)])
    assert_node(result[0][0], refuri="/url")


def test_example_534():
    text = ("""\\[foo]\n"""
            """\n"""
            """[foo]: /url "title"\n""")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.paragraph, "[foo]"],
                                          nodes.target)])


def test_example_535():
    text = ("[foo*]: /url\n"
            "\n"
            "*[foo*]\n")
    result = publish(text)
    assert_node(result, [nodes.document, (nodes.target,
                                          [nodes.paragraph, ("*",
                                                             [nodes.reference, "foo*"])])])


def test_example_536():
    text = ("[foo][bar]\n"
            "\n"
            "[foo]: /url1\n"
            "[bar]: /url2\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.paragraph, nodes.reference, "foo"],
                                          nodes.target,
                                          nodes.target)])
    assert_node(result[0][0], refuri="/url2")


def test_example_537():
    text = ("[foo][]\n"
            "\n"
            "[foo]: /url1\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.paragraph, nodes.reference, "foo"],
                                          nodes.target)])
    assert_node(result[0][0], refuri="/url1")


def test_example_538():
    text = ("[foo]()\n"
            "\n"
            "[foo]: /url1\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.paragraph, nodes.reference, "foo"],
                                          nodes.target)])
    assert_node(result[0][0], refuri="")


def test_example_539():
    text = ("[foo](not a link)\n"
            "\n"
            "[foo]: /url1\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.paragraph, ([nodes.reference, "foo"],
                                                             "(not a link)")],
                                          nodes.target)])
    assert_node(result[0][0], refuri="/url1")


def test_example_540():
    text = ("[foo][bar][baz]\n"
            "\n"
            "[baz]: /url\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.paragraph, ("[foo]",
                                                             [nodes.reference, "bar"])],
                                          nodes.target)])
    assert_node(result[0][1], refuri="/url")


def test_example_541():
    text = ("[foo][bar][baz]\n"
            "\n"
            "[baz]: /url1\n"
            "[bar]: /url2\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.paragraph, ([nodes.reference, "foo"],
                                                             [nodes.reference, "baz"])],
                                          nodes.target,
                                          nodes.target)])
    assert_node(result[0][0], refuri="/url2")
    assert_node(result[0][1], refuri="/url1")


def test_example_542():
    text = ("[foo][bar][baz]\n"
            "\n"
            "[baz]: /url1\n"
            "[foo]: /url2\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.paragraph, ("[foo]",
                                                             [nodes.reference, "bar"])],
                                          nodes.target,
                                          nodes.target)])
    assert_node(result[0][1], refuri="/url1")


def test_example_543():
    result = publish('![foo](/url "title")')
    assert_node(result, [nodes.document, nodes.paragraph, nodes.image])
    assert_node(result[0][0], uri="/url", alt="foo", title="title")


def test_example_544():
    text = ("""![foo *bar*]\n"""
            """\n"""
            """[foo *bar*]: train.jpg "train & tracks"\n""")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.paragraph, nodes.image],
                                          nodes.target)])
    assert_node(result[0][0], uri="train.jpg", alt="foo *bar*", title="train & tracks")


def test_example_545():
    result = publish("![foo ![bar](/url)](/url2)")
    assert_node(result, [nodes.document, nodes.paragraph, nodes.image])
    assert_node(result[0][0], uri="/url2", alt="foo bar")


def test_example_546():
    result = publish("![foo [bar](/url)](/url2)")
    assert_node(result, [nodes.document, nodes.paragraph, nodes.image])
    assert_node(result[0][0], uri="/url2", alt="foo bar")


def test_example_547():
    text = ("""![foo *bar*][]\n"""
            """\n"""
            """[foo *bar*]: train.jpg "train & tracks"\n""")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.paragraph, nodes.image],
                                          nodes.target)])
    assert_node(result[0][0], uri="train.jpg", alt="foo *bar*", title="train & tracks")


def test_example_548():
    text = ("""![foo *bar*][foobar]\n"""
            """\n"""
            """[FOOBAR]: train.jpg "train & tracks"\n""")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.paragraph, nodes.image],
                                          nodes.target)])
    assert_node(result[0][0], uri="train.jpg", alt="foo *bar*", title="train & tracks")


def test_example_549():
    result = publish("![foo](train.jpg)")
    assert_node(result, [nodes.document, nodes.paragraph, nodes.image])
    assert_node(result[0][0], uri="train.jpg", alt="foo")


def test_example_550():
    result = publish('My ![foo bar](/path/to/train.jpg  "title"   )')
    assert_node(result, [nodes.document, nodes.paragraph, ("My ",
                                                           nodes.image)])
    assert_node(result[0][1], uri="/path/to/train.jpg", alt="foo bar", title="title")


def test_example_551():
    result = publish("![foo](<url>)")
    assert_node(result, [nodes.document, nodes.paragraph, nodes.image])
    assert_node(result[0][0], uri="url", alt="foo")


def test_example_552():
    result = publish("![](/url)")
    assert_node(result, [nodes.document, nodes.paragraph, nodes.image])
    assert_node(result[0][0], uri="/url", alt="")


def test_example_561():
    text = ("""![[foo]]\n"""
            """\n"""
            """[[foo]]: /url "title"\n""")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.paragraph, "![[foo]]"],
                                          [nodes.paragraph, '[[foo]]: /url "title"'])])


def test_example_565():
    result = publish("<http://foo.bar.baz>")
    assert_node(result, [nodes.document, nodes.paragraph, nodes.reference, "http://foo.bar.baz"])
    assert_node(result[0][0], refuri="http://foo.bar.baz")


def test_example_566():
    result = publish("<http://foo.bar.baz/test?q=hello&id=22&boolean>")
    assert_node(result, [nodes.document, nodes.paragraph, nodes.reference,
                         "http://foo.bar.baz/test?q=hello&id=22&boolean"])
    assert_node(result[0][0], refuri="http://foo.bar.baz/test?q=hello&id=22&boolean")


def test_example_567():
    result = publish("<irc://foo.bar:2233/baz>")
    assert_node(result, [nodes.document, nodes.paragraph, nodes.reference, "irc://foo.bar:2233/baz"])


def test_example_568():
    result = publish("<MAILTO:FOO@BAR.BAZ>")
    assert_node(result, [nodes.document, nodes.paragraph, nodes.reference, "MAILTO:FOO@BAR.BAZ"])


def test_example_569():
    result = publish("<a+b+c:d>")
    assert_node(result, [nodes.document, nodes.paragraph, nodes.reference, "a+b+c:d"])


def test_example_570():
    result = publish("<made-up-scheme://foo,bar>")
    assert_node(result, [nodes.document, nodes.paragraph, nodes.reference, "made-up-scheme://foo,bar"])


def test_example_573():
    result = publish("<http://foo.bar/baz bim>")
    assert_node(result, [nodes.document, nodes.paragraph, "<http://foo.bar/baz bim>"])


def test_example_574():
    result = publish("<http://example.com/\\[\\>")
    assert_node(result, [nodes.document, nodes.paragraph, nodes.reference, "http://example.com/\\[\\"])


def test_example_575():
    result = publish("<foo@bar.example.com>")
    assert_node(result, [nodes.document, nodes.paragraph, nodes.reference, "foo@bar.example.com"])
    assert_node(result[0][0], refuri='mailto:foo@bar.example.com')


def test_example_576():
    result = publish("<foo+special@Bar.baz-bar0.com>")
    assert_node(result, [nodes.document, nodes.paragraph, nodes.reference, "foo+special@Bar.baz-bar0.com"])


def test_example_577():
    result = publish("<foo\+@bar.example.com>")
    assert_node(result, [nodes.document, nodes.paragraph, "<foo+@bar.example.com>"])


def test_example_578():
    result = publish("<>")
    assert_node(result, [nodes.document, nodes.paragraph, "<>"])


def test_example_579():
    result = publish("< http://foo.bar >")
    assert_node(result, [nodes.document, nodes.paragraph, "< http://foo.bar >"])


def test_example_580():
    result = publish("<m:abc>")
    assert_node(result, [nodes.document, nodes.paragraph, "<m:abc>"])


def test_example_581():
    result = publish("<foo.bar.baz>")
    assert_node(result, [nodes.document, nodes.paragraph, "<foo.bar.baz>"])


def test_example_582():
    result = publish("http://example.com")
    assert_node(result, [nodes.document, nodes.paragraph, "http://example.com"])


def test_example_583():
    result = publish("foo@bar.example.com")
    assert_node(result, [nodes.document, nodes.paragraph, "foo@bar.example.com"])
