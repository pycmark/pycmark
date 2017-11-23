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


class SparseTextConverter(Transform):
    default_priority = 900

    def apply(self):
        for node in self.document.traverse(addnodes.SparseText):
            pos = node.parent.index(node)
            node.parent.remove(node)
            node.parent.insert(pos, nodes.Text(node))


class EmphasisConverter(Transform):
    default_priority = 900

    def apply(self):
        for node in self.document.traverse(nodes.TextElement):
            while True:
                delimiters = list(n for n in node.children if isinstance(n, addnodes.delimiter))
                closers = list(d for d in delimiters if d['can_close'])
                if len(closers) == 0:
                    break
                closer = closers[0]
                opener = self.find_opener(delimiters, closer)
                if opener is None:
                    closer['can_close'] = False
                    continue

                if opener['curr_length'] >= 2 and closer['curr_length'] >= 2:
                    length = 2
                    emph_node = nodes.strong()
                else:
                    length = 1
                    emph_node = nodes.emphasis()

                opener_pos = node.index(opener)
                closer_pos = node.index(closer)
                for subnode in node[opener_pos + 1:closer_pos]:
                    node.remove(subnode)
                    emph_node += subnode
                self.deactivate_delimiters(emph_node)

                node.insert(opener_pos + 1, emph_node)
                opener.shrink(length)
                closer.shrink(length)

            self.deactivate_delimiters(node)

    def find_opener(self, delimiters, closer):
        pos = delimiters.index(closer)
        for opener in reversed(delimiters[:pos]):
            if opener['can_open'] is False:
                continue
            elif opener['marker'][0] != closer['marker'][0]:
                continue
            else:
                odd_match = ((closer['can_open'] or opener['can_close']) and
                             (opener['orig_length'] + closer['orig_length']) % 3 == 0)
                if not odd_match:
                    return opener

        return None

    def deactivate_delimiters(self, node):
        delimiters = list(n for n in node.children if isinstance(n, addnodes.delimiter))
        for delim in delimiters:
            marker = str(delim)
            delim.replace_self(nodes.Text(marker, marker))


class TextNodeConnector(Transform):
    default_priority = 950  # must be executed after SparseTextConverter

    def apply(self):
        for node in self.document.traverse(nodes.TextElement):
            pos = 0
            while len(node) > pos + 1:
                if isinstance(node[pos], nodes.Text) and isinstance(node[pos + 1], nodes.Text):
                    text = node[pos] + node[pos + 1]
                    node.remove(node[pos + 1])
                    node.remove(node[pos])
                    node.insert(pos, nodes.Text(text, text))
                else:
                    pos += 1
