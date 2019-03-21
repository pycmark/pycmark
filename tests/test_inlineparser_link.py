"""
    test_inlineparser_link
    ~~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2017-2019 by Takeshi KOMIYA
    :license: Apache License 2.0, see LICENSE for details.
"""

from docutils import nodes
from utils import publish, assert_node


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
    assert_node(result, [nodes.document, nodes.paragraph, ("[link](",
                                                           [nodes.raw, "<foo\nbar>"],
                                                           ")")])


def test_example_467():
    result = publish(r"[link](\(foo\))")
    assert_node(result, [nodes.document, nodes.paragraph, nodes.reference, "link"])
    assert_node(result[0][0], refuri="(foo)")


def test_example_468():
    result = publish("[link](foo(and(bar)))")
    assert_node(result, [nodes.document, nodes.paragraph, nodes.reference, "link"])
    assert_node(result[0][0], refuri="foo(and(bar))")


def test_example_469():
    result = publish(r"[link](foo\(and\(bar\))")
    assert_node(result, [nodes.document, nodes.paragraph, nodes.reference, "link"])
    assert_node(result[0][0], refuri="foo(and(bar)")


def test_example_470():
    result = publish("[link](<foo(and(bar)>)")
    assert_node(result, [nodes.document, nodes.paragraph, nodes.reference, "link"])
    assert_node(result[0][0], refuri="foo(and(bar)")


def test_example_471():
    result = publish(r"[link](foo\)\:)")
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
    result = publish("[link](foo\\bar)")
    assert_node(result, [nodes.document, nodes.paragraph, nodes.reference, "link"])
    assert_node(result[0][0], refuri="foo%5Cbar")


def test_example_474():
    result = publish("[link](foo%20b&auml;)")
    assert_node(result, [nodes.document, nodes.paragraph, nodes.reference, "link"])
    assert_node(result[0][0], refuri="foo%20b%C3%A4")


def test_example_474_2():
    result = publish("[link](<foo%20b&auml;>)")
    assert_node(result, [nodes.document, nodes.paragraph, nodes.reference, "link"])
    assert_node(result[0][0], refuri="foo%20b%C3%A4")


def test_example_475():
    result = publish("""[link]("title")""")
    assert_node(result, [nodes.document, nodes.paragraph, nodes.reference, "link"])
    assert_node(result[0][0], refuri='%22title%22')


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
    assert_node(result[0][0], refuri='/url%C2%A0%22title%22')


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


def test_example_488():
    result = publish("[![moon](moon.jpg)](/uri)")
    assert_node(result, [nodes.document, nodes.paragraph, nodes.reference, nodes.image])
    assert_node(result[0][0], refuri="/uri")
    assert_node(result[0][0][0], uri="moon.jpg", alt="moon")


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


def test_example_491():
    result = publish("![[[foo](uri1)](uri2)](uri3)")
    assert_node(result, [nodes.document, nodes.paragraph, nodes.image])
    assert_node(result[0][0], uri="uri3", alt="[foo](uri2)")


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


def test_example_495():
    result = publish('[foo <bar attr="](baz)">')
    assert_node(result, [nodes.document, nodes.paragraph, ("[foo ",
                                                           [nodes.raw, '<bar attr="](baz)">'])])


def test_example_496():
    result = publish("[foo`](/uri)`")
    assert_node(result, [nodes.document, nodes.paragraph, ("[foo",
                                                           [nodes.literal, "](/uri)"])])


def test_example_497():
    result = publish("[foo<http://example.com/?search=](uri)>")
    assert_node(result, [nodes.document, nodes.paragraph, ("[foo",
                                                           [nodes.reference, "http://example.com/?search=](uri)"])])


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


def test_example_507():
    text = ('[foo <bar attr="][ref]">\n'
            '\n'
            '[ref]: /uri\n')
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.paragraph, ("[foo ",
                                                             [nodes.raw, '<bar attr="][ref]">'])],
                                          nodes.target)])


def test_example_508():
    text = ("[foo`][ref]`\n"
            "\n"
            "[ref]: /uri\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.paragraph, ("[foo",
                                                             [nodes.literal, "][ref]"])],
                                          nodes.target)])


def test_example_509():
    text = ("[foo<http://example.com/?search=][ref]>\n"
            "\n"
            "[ref]: /uri\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.paragraph, ("[foo",
                                                             [nodes.reference, "http://example.com/?search=][ref]"])],
                                          nodes.target)])


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
    assert_node(result, [nodes.document, ([nodes.paragraph, "[bar][foo!]"],
                                          nodes.target)])


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
                                                             "\n[]")],
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
    assert_node(result[0][0], uri="train.jpg", alt="foo bar", title="train & tracks")


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
    assert_node(result[0][0], uri="train.jpg", alt="foo bar", title="train & tracks")


def test_example_548():
    text = ("""![foo *bar*][foobar]\n"""
            """\n"""
            """[FOOBAR]: train.jpg "train & tracks"\n""")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.paragraph, nodes.image],
                                          nodes.target)])
    assert_node(result[0][0], uri="train.jpg", alt="foo bar", title="train & tracks")


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
