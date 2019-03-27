"""
    utils
    ~~~~~

    :copyright: Copyright 2017-2019 by Takeshi KOMIYA
    :license: Apache License 2.0, see LICENSE for details.
"""

from docutils.core import publish_doctree
from docutils.readers.standalone import Reader

from pycmark import CommonMarkParser
from pycmark.transforms import LinebreakFilter

from sphinx import assert_node  # NOQA


class TestReader(Reader):
    def get_transforms(self):
        return []  # skip all of transforms!


class TestParser(CommonMarkParser):
    def get_transforms(self):
        transforms = super().get_transforms()
        transforms.remove(LinebreakFilter)
        return transforms


def publish(text):
    return publish_doctree(source=text,
                           source_path='dummy.md',
                           reader=TestReader(),
                           parser=TestParser())
