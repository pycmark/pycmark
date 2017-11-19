# -*- coding: utf-8 -*-
"""
    test_readers
    ~~~~~~~~~~~~

    :copyright: Copyright 2017 by Takeshi KOMIYA
    :license: BSD, see LICENSE for details.
"""

from pycmark.readers import LineReader


text = ("Lorem ipsum dolor sit amet, \n"
        "consectetur adipiscing elit, \n"
        "\n"
        "    sed do eiusmod tempor incididunt \n"
        "    ut labore et dolore magna aliqua.\n"
        "\n"
        "Ut enim ad minim veniam, quis nostrud")


def test_LineReader():
    reader = LineReader(text.splitlines())
    assert reader.eof() is False

    # read first line
    assert reader.readline() == "Lorem ipsum dolor sit amet, "
    assert reader.current_line == "Lorem ipsum dolor sit amet, "
    assert reader.fetch() == "Lorem ipsum dolor sit amet, "
    assert reader.fetch(1) == "consectetur adipiscing elit, "
    assert reader.next_line == "consectetur adipiscing elit, "
    assert reader.fetch(2) == ""

    # read second line
    assert reader.readline() == "consectetur adipiscing elit, "
    assert reader.current_line == "consectetur adipiscing elit, "
    assert reader.fetch() == "consectetur adipiscing elit, "
    assert reader.fetch(1) == ""

    # rollback a line
    reader.step(-1)
    assert reader.current_line == "Lorem ipsum dolor sit amet, "

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
