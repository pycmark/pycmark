# -*- coding: utf-8 -*-
"""
    pycmark.transforms
    ~~~~~~~~~~~~~~~~~~

    Transform classes for BlockParser.

    :copyright: Copyright 2017 by Takeshi KOMIYA
    :license: BSD, see LICENSE for details.
"""

from docutils import nodes
from docutils.transforms import Transform
from pycmark import addnodes


class BlanklineFilter(Transform):
    default_priority = 500

    def apply(self):
        for node in self.document.traverse(addnodes.blankline):
            node.parent.remove(node)


class TightListsDetector(Transform):
    default_priority = BlanklineFilter.default_priority - 1  # must be eariler than BlanklineFilter

    def apply(self):
        # type: () -> None
        self.detect(self.document)

    def detect(self, document):
        # type: (nodes.Element) -> None
        def is_list_node(node):
            # type: (nodes.Node) -> bool
            return isinstance(node, (nodes.bullet_list, nodes.enumerated_list))

        def has_loose_element(node):
            # type: (nodes.Element) -> bool
            return any(isinstance(subnode, addnodes.blankline) for subnode in node)

        for node in document.traverse(is_list_node):
            if any(has_loose_element(item) for item in node):
                node['tight'] = False
            else:
                node['tight'] = True

            # detect loose lists in list_items
            for list_item in node:
                self.detect(list_item)


class TightListsCompactor(Transform):
    default_priority = 999

    def apply(self):
        def is_tight_list(node):
            # type: (nodes.Node) -> bool
            return (isinstance(node, (nodes.bullet_list, nodes.enumerated_list)) and
                    node['tight'] is True)

        for list_node in self.document.traverse(is_tight_list):
            for list_item in list_node:
                for para in list_item[:]:
                    pos = list_item.index(para)
                    if isinstance(para, nodes.paragraph):
                        for i, text in enumerate(para[:]):
                            para.remove(text)
                            list_item.insert(pos + i + 1, text)
                        list_item.remove(para)
