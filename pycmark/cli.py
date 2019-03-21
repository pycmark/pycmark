"""
    pycmark.cli
    ~~~~~~~~~~~

    command line tools for pycmark.

    :copyright: Copyright 2017-2019 by Takeshi KOMIYA
    :license: Apache License 2.0, see LICENSE for details.
"""

from docutils.core import publish_cmdline

from pycmark import CommonMarkParser


def md2html() -> None:
    publish_cmdline(parser=CommonMarkParser(), writer_name='html5')
