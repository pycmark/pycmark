# -*- coding: utf-8 -*-
"""
    test_readers
    ~~~~~~~~~~~~

    :copyright: Copyright 2017 by Takeshi KOMIYA
    :license: BSD, see LICENSE for details.
"""

from pycmark.blockparser import BlockProcessor
from pycmark.readers import LineReader, BlockQuoteReader, ListItemReader, LazyLineReader


text = ("Lorem ipsum dolor sit amet, \n"
        "consectetur adipiscing elit, \n"
        "\n"
        "    sed do eiusmod tempor incididunt \n"
        "    ut labore et dolore magna aliqua.\n"
        "\n"
        "Ut enim ad minim veniam, quis nostrud")

quoted_text = ("> Lorem ipsum dolor sit amet, \n"
               " consectetur adipiscing elit, \n"
               "\n"
               "sed do eiusmod tempor incididunt \n"
               "ut labore et dolore magna aliqua.")


def test_LineReader():
    reader = LineReader(text.splitlines(), source='dummy.md')
    assert reader.eof() is False
    assert reader.get_source_and_line() == ('dummy.md', 0)

    # read first line
    assert reader.readline() == "Lorem ipsum dolor sit amet, "
    assert reader.current_line == "Lorem ipsum dolor sit amet, "
    assert reader.fetch() == "Lorem ipsum dolor sit amet, "
    assert reader.fetch(1) == "consectetur adipiscing elit, "
    assert reader.next_line == "consectetur adipiscing elit, "
    assert reader.fetch(2) == ""
    assert reader.get_source_and_line() == ('dummy.md', 1)

    # read second line
    assert reader.readline() == "consectetur adipiscing elit, "
    assert reader.current_line == "consectetur adipiscing elit, "
    assert reader.fetch() == "consectetur adipiscing elit, "
    assert reader.fetch(1) == ""
    assert reader.get_source_and_line() == ('dummy.md', 2)

    # rollback a line
    reader.step(-1)
    assert reader.current_line == "Lorem ipsum dolor sit amet, "
    assert reader.get_source_and_line() == ('dummy.md', 1)

    # step a line again
    reader.step()
    assert reader.current_line == "consectetur adipiscing elit, "

    # read until the end
    assert reader.readline() == ""
    assert reader.readline() == "    sed do eiusmod tempor incididunt "
    assert reader.readline() == "    ut labore et dolore magna aliqua."
    assert reader.readline() == ""
    assert reader.readline() == "Ut enim ad minim veniam, quis nostrud"
    assert reader.eof() is True

    try:
        assert reader.readline()
        assert False, "reader does not raise IOError on EOF"
    except IOError:
        pass


def test_BlockQuoteReader():
    reader = LineReader(quoted_text.splitlines(True), source='dummy.md')
    quoted_reader = BlockQuoteReader(reader)
    assert quoted_reader.eof() is False
    assert quoted_reader.get_source_and_line() == ('dummy.md', 0)

    # read first line
    assert quoted_reader.readline() == "Lorem ipsum dolor sit amet, \n"
    assert quoted_reader.current_line == "Lorem ipsum dolor sit amet, \n"
    assert quoted_reader.fetch() == "Lorem ipsum dolor sit amet, \n"
    assert quoted_reader.get_source_and_line() == ('dummy.md', 1)

    # laziness: off
    try:
        quoted_reader.readline()
        assert False
    except IOError:
        pass

    # lazyness allows texts hanging on quoted block
    assert quoted_reader.readline(lazy=True) == " consectetur adipiscing elit, \n"

    # empty line causes IOError
    try:
        quoted_reader.readline()
        assert False
    except IOError:
        pass

    # empty line causes IOError even if lazy
    try:
        quoted_reader.readline(lazy=True)
        assert False
    except IOError:
        pass

    assert reader.readline() == '\n'
    assert reader.readline() == "sed do eiusmod tempor incididunt \n"
    assert reader.readline() == "ut labore et dolore magna aliqua."


def test_LazyLineReader():
    reader = LineReader(quoted_text.splitlines(True), source='dummy.md')
    lazy_reader = LazyLineReader(BlockQuoteReader(reader))
    assert lazy_reader.eof() is False
    assert lazy_reader.get_source_and_line() == ('dummy.md', 0)

    # read first line
    assert lazy_reader.readline() == "Lorem ipsum dolor sit amet, \n"
    assert lazy_reader.current_line == "Lorem ipsum dolor sit amet, \n"
    assert lazy_reader.fetch() == "Lorem ipsum dolor sit amet, \n"
    assert lazy_reader.get_source_and_line() == ('dummy.md', 1)

    # read second line
    assert lazy_reader.readline() == " consectetur adipiscing elit, \n"

    # empty line causes IOError
    try:
        lazy_reader.readline()
        assert False
    except IOError:
        pass

    assert reader.readline() == '\n'
    assert reader.readline() == "sed do eiusmod tempor incididunt \n"
    assert reader.readline() == "ut labore et dolore magna aliqua."


def test_ListItemReader():
    text = ("- Lorem ipsum dolor sit amet, \n"
            "- consectetur adipiscing elit, \n"
            "\n"
            "  sed do eiusmod tempor incididunt \n"
            "ut labore et dolore magna aliqua.")
    reader = LineReader(text.splitlines(True))
    list_reader = ListItemReader(reader, 2, BlockProcessor(None))
    assert list_reader.readline() == "Lorem ipsum dolor sit amet, \n"

    # reached next item
    try:
        list_reader.readline()
        assert False
    except IOError:
        pass

    list_reader = ListItemReader(reader, 2, BlockProcessor(None))
    assert list_reader.readline() == "consectetur adipiscing elit, \n"
    assert list_reader.readline() == "\n"
    assert list_reader.readline() == "sed do eiusmod tempor incididunt \n"

    # reached the end of list
    try:
        list_reader.readline()
        assert False
    except IOError:
        pass

    # can read the next line with laziness
    assert list_reader.readline(lazy=True) == "ut labore et dolore magna aliqua."


def test_ListItemReader2():
    text = ("> 1. > Blockquote\n"
            "continued here.\n")
    reader = LineReader(text.splitlines(True))
    reader = BlockQuoteReader(reader)
    reader = ListItemReader(reader, 3, BlockProcessor(None))
    reader = BlockQuoteReader(reader)
    reader = LazyLineReader(reader)
    assert reader.readline() == 'Blockquote\n'
    assert reader.eof() is False
    assert reader.next_line == 'continued here.\n'
    assert reader.readline() == 'continued here.\n'
