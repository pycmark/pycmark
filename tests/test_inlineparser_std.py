"""
    test_inlineparser_std
    ~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2017-2019 by Takeshi KOMIYA
    :license: Apache License 2.0, see LICENSE for details.
"""

from docutils import nodes
from utils import publish, assert_node

from pycmark import addnodes


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


def test_example_301():
    text = ("``` foo\\+bar\n"
            "foo\n"
            "```\n")
    result = publish(text)
    assert_node(result[0], nodes.literal_block, classes=['code', 'language-foo+bar'])


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
    result = publish("&#X22; &#XD06; &#xcab;")
    assert_node(result, [nodes.document, nodes.paragraph, '" ആ ಫ'])


def test_example_305():
    text = ("&nbsp &x; &#; &#x;\n"
            "&ThisIsNotDefined; &hi?;")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.paragraph, text])


def test_example_306():
    result = publish("&copy")
    assert_node(result, [nodes.document, nodes.paragraph, "&copy"])


def test_example_307():
    result = publish("&MadeUpEntity;")
    assert_node(result, [nodes.document, nodes.paragraph, "&MadeUpEntity;"])


def test_example_308():
    result = publish('<a href="&ouml;&ouml;.html">')
    assert_node(result, [nodes.document, nodes.raw, '<a href="&ouml;&ouml;.html">'])


def test_example_309():
    result = publish('[foo](/f&ouml;&ouml; "f&ouml;&ouml;")')
    assert_node(result, [nodes.document, nodes.paragraph, nodes.reference, "foo"])
    assert_node(result[0][0], refuri="/f%C3%B6%C3%B6", reftitle="föö")


def test_example_310():
    text = ('[foo]\n'
            '\n'
            '[foo]: /f&ouml;&ouml; "f&ouml;&ouml;"\n')
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.paragraph, nodes.reference, "foo"],
                                          nodes.target)])
    assert_node(result[0][0], refuri="/f%C3%B6%C3%B6", reftitle="föö")


def test_example_311():
    text = ("``` f&ouml;&ouml;\n"
            "foo\n"
            "```\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.literal_block, "foo\n"])
    assert_node(result[0], classes=["code", "language-föö"])


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


def test_example_319():
    result = publish("`a\xa0\xa0b`")
    assert_node(result, [nodes.document, nodes.paragraph, nodes.literal, "a\xa0\xa0b"])


def test_example_321():
    result = publish(r"`foo\`bar`")
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


def test_example_325():
    result = publish("""<a href="`">`""")
    assert_node(result, [nodes.document, nodes.paragraph, ([nodes.raw, '<a href="`">'],
                                                           "`")])


def test_example_327():
    result = publish("<http://foo.bar.`baz>`")
    assert_node(result, [nodes.document, nodes.paragraph, ([nodes.reference, "http://foo.bar.`baz"],
                                                           "`")])


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


def test_example_384():
    result = publish("*foo [bar](/url)*")
    assert_node(result, [nodes.document, nodes.paragraph, nodes.emphasis, ("foo ",
                                                                           [nodes.reference, "bar"])])


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


def test_example_391_2():
    result = publish("*foo**bar*")
    assert_node(result, [nodes.document, nodes.paragraph, nodes.emphasis, "foo**bar"])


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


def test_example_396():
    result = publish("*foo [*bar*](/url)*")
    assert_node(result, [nodes.document, nodes.paragraph, nodes.emphasis, ("foo ",
                                                                           [nodes.reference, nodes.emphasis, "bar"])])


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
    result = publish(r"foo *\**")
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


def test_example_450():
    result = publish("*[bar*](/url)")
    assert_node(result, [nodes.document, nodes.paragraph, ("*",
                                                           [nodes.reference, "bar*"])])


def test_example_451():
    result = publish("_foo [bar_](/url)")
    assert_node(result, [nodes.document, nodes.paragraph, ("_foo ",
                                                           [nodes.reference, "bar_"])])


def test_example_452():
    result = publish('*<img src="foo" title="*"/>')
    assert_node(result, [nodes.document, nodes.paragraph, ("*",
                                                           [nodes.raw, '<img src="foo" title="*"/>'])])


def test_example_453():
    result = publish('**<a href="**">')
    assert_node(result, [nodes.document, nodes.paragraph, ("**",
                                                           [nodes.raw, '<a href="**">'])])


def test_example_455():
    result = publish("*a `*`*")
    assert_node(result, [nodes.document, nodes.paragraph, nodes.emphasis, ("a ",
                                                                           [nodes.literal, "*"])])


def test_example_456():
    result = publish("_a `_`_")
    assert_node(result, [nodes.document, nodes.paragraph, nodes.emphasis, ("a ",
                                                                           [nodes.literal, "_"])])


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
    result = publish(r"<foo\+@bar.example.com>")
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


def test_example_584():
    result = publish("<a><bab><c2c>")
    assert_node(result, [nodes.document, nodes.paragraph, ([nodes.raw, "<a>"],
                                                           [nodes.raw, "<bab>"],
                                                           [nodes.raw, "<c2c>"])])
    assert_node(result[0][0], format='html')
    assert_node(result[0][1], format='html')
    assert_node(result[0][2], format='html')


def test_example_585():
    result = publish("<a/><b2/>")
    assert_node(result, [nodes.document, nodes.paragraph, ([nodes.raw, "<a/>"],
                                                           [nodes.raw, "<b2/>"])])


def test_example_586():
    text = ('<a  /><b2\n'
            'data="foo" >\n')
    result = publish(text)
    assert_node(result, [nodes.document, nodes.paragraph, ([nodes.raw, "<a  />"],
                                                           [nodes.raw, '<b2\ndata="foo" >'])])


def test_example_587():
    text = ("""<a foo="bar" bam = 'baz <em>"</em>'\n"""
            """_boolean zoop:33=zoop:33 />\n""")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.paragraph, nodes.raw, text.strip()])


def test_example_588():
    result = publish('Foo <responsive-image src="foo.jpg" />')
    assert_node(result, [nodes.document, nodes.paragraph, ("Foo ",
                                                           [nodes.raw, '<responsive-image src="foo.jpg" />'])])


def test_example_589():
    result = publish("<33> <__>")
    assert_node(result, [nodes.document, nodes.paragraph, "<33> <__>"])


def test_example_590():
    text = '<a h*#ref="hi">'
    result = publish(text)
    assert_node(result, [nodes.document, nodes.paragraph, text])


def test_example_591():
    text = """<a href="hi'> <a href=hi'>"""
    result = publish(text)
    assert_node(result, [nodes.document, nodes.paragraph, text])


def test_example_592():
    text = ("< a><\n"
            "foo><bar/ >\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.paragraph, text.strip()])


def test_example_593():
    text = "<a href='bar'title=title>"
    result = publish(text)
    assert_node(result, [nodes.document, nodes.paragraph, text])


def test_example_594():
    result = publish("</a></foo >")
    assert_node(result, [nodes.document, nodes.paragraph, ([nodes.raw, "</a>"],
                                                           [nodes.raw, "</foo >"])])


def test_example_595():
    text = '</a href="foo">'
    result = publish(text)
    assert_node(result, [nodes.document, nodes.paragraph, text])


def test_example_596():
    text = ("foo <!-- this is a\n"
            "comment - with hyphen -->\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.paragraph, ("foo ",
                                                           [nodes.raw, "<!-- this is a\ncomment - with hyphen -->"])])


def test_example_597():
    text = "foo <!-- not a comment -- two hyphens -->"
    result = publish(text)
    assert_node(result, [nodes.document, nodes.paragraph, text])


def test_example_598():
    text = ("foo <!--> foo -->\n"
            "\n"
            "foo <!-- foo--->\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.paragraph, "foo <!--> foo -->"],
                                          [nodes.paragraph, "foo <!-- foo--->"])])


def test_example_599():
    result = publish("foo <?php echo $a; ?>\n")
    assert_node(result, [nodes.document, nodes.paragraph, ("foo ",
                                                           [nodes.raw, "<?php echo $a; ?>"])])


def test_example_600():
    result = publish("foo <!ELEMENT br EMPTY>\n")
    assert_node(result, [nodes.document, nodes.paragraph, ("foo ",
                                                           [nodes.raw, "<!ELEMENT br EMPTY>"])])


def test_example_601():
    result = publish("foo <![CDATA[>&<]]>\n")
    assert_node(result, [nodes.document, nodes.paragraph, ("foo ",
                                                           [nodes.raw, "<![CDATA[>&<]]>"])])


def test_example_602():
    result = publish('foo <a href="&ouml;">\n')
    assert_node(result, [nodes.document, nodes.paragraph, ("foo ",
                                                           [nodes.raw, '<a href="&ouml;">'])])


def test_example_603():
    result = publish('foo <a href="\\*">\n')
    assert_node(result, [nodes.document, nodes.paragraph, ("foo ",
                                                           [nodes.raw, '<a href="\\*">'])])


def test_example_604():
    text = '<a href="\"">'
    result = publish(text)
    assert_node(result, [nodes.document, nodes.paragraph, text])


def test_example_605():
    text = ("foo  \n"
            "baz\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.paragraph, ("foo", addnodes.linebreak, "baz")])


def test_example_606():
    text = ("foo\\\n"
            "baz\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.paragraph, ("foo", addnodes.linebreak, "baz")])


def test_example_607():
    text = ("foo       \n"
            "baz\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.paragraph, ("foo", addnodes.linebreak, "baz")])


def test_example_608():
    text = ("foo  \n"
            "     bar\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.paragraph, ("foo", addnodes.linebreak, "bar")])


def test_example_610():
    text = ("*foo  \n"
            "baz*\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.paragraph, nodes.emphasis,
                         ("foo", addnodes.linebreak, "baz")])


def test_example_611():
    text = ("`code  \n"
            "span`\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.paragraph, nodes.literal, "code span"])


# TODO: add test for HTML tags (Example 614 and 615)


def test_example_616():
    result = publish("foo\\")
    assert_node(result, [nodes.document, nodes.paragraph, "foo\\"])


def test_example_617():
    result = publish("foo  ")
    assert_node(result, [nodes.document, nodes.paragraph, "foo"])


def test_example_618():
    result = publish("### foo\\")
    assert_node(result, [nodes.document, nodes.section, nodes.title, "foo\\"])


def test_example_619():
    result = publish("### foo  ")
    assert_node(result, [nodes.document, nodes.section, nodes.title, "foo"])


def test_example_621():
    text = ("foo \n"
            " baz\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.paragraph, "foo\nbaz"])
