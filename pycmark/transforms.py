"""
    pycmark.transforms
    ~~~~~~~~~~~~~~~~~~

    Transform classes for BlockParser.

    :copyright: Copyright 2017-2019 by Takeshi KOMIYA
    :license: Apache License 2.0, see LICENSE for details.
"""

from typing import List, cast

from docutils import nodes
from docutils.nodes import Element, FixedTextElement, Node, Text, TextElement
from docutils.transforms import Transform

from pycmark import addnodes
from pycmark.inlineparser import InlineParser
from pycmark.utils import transplant_nodes


class BlanklineFilter(Transform):
    default_priority = 200

    def apply(self, **kwargs) -> None:
        for node in self.document.traverse(addnodes.blankline):
            node.parent.remove(node)


class LinebreakFilter(Transform):
    default_priority = 200

    def apply(self, **kwargs) -> None:
        for node in self.document.traverse(addnodes.linebreak):
            self.document.reporter.warning("A hard line break detected, ignored.",
                                           source=node.parent.source, line=node.parent.line)
            node.replace_self(addnodes.SparseText('\n', 0, 1))


class TightListsDetector(Transform):
    default_priority = BlanklineFilter.default_priority - 10

    def apply(self, **kwargs) -> None:
        self.detect(self.document)

    def detect(self, document: Element) -> None:
        def is_list_node(node: Node) -> bool:
            return isinstance(node, (nodes.bullet_list, nodes.enumerated_list))

        def has_loose_element(node: Element) -> bool:
            return any(isinstance(subnode, addnodes.blankline) for subnode in node[1:])

        for node in document.traverse(is_list_node):  # type: Element
            children = cast(List[nodes.list_item], node)
            if any(has_loose_element(item) for item in children):
                node['tight'] = False
            else:
                node['tight'] = True

            # detect loose lists in list_items
            for list_item in children:
                self.detect(list_item)


class TightListsCompactor(Transform):
    default_priority = 300

    def apply(self, **kwargs) -> None:
        def is_tight_list(node: Node) -> bool:
            return (isinstance(node, (nodes.bullet_list, nodes.enumerated_list)) and
                    node['tight'] is True)

        for list_node in self.document.traverse(is_tight_list):  # type: List[Element]
            for list_item in list_node:
                for para in list_item[:]:
                    pos = list_item.index(para)
                    if isinstance(para, nodes.paragraph):
                        for i, text in enumerate(para[:]):
                            para.remove(text)
                            list_item.insert(pos + i + 1, text)
                        list_item.remove(para)


class SectionTreeConstructor(Transform):
    default_priority = 200

    def apply(self, **kwargs) -> None:
        def is_container_node(node: Node) -> bool:
            return isinstance(node, (nodes.document, nodes.block_quote, nodes.list_item))

        for node in self.document.traverse(is_container_node):  # type: Element
            self.construct_section_tree(node)

    def construct_section_tree(self, container: Element) -> None:
        current_depth = 0
        last_section = None
        for node in container[:]:
            if isinstance(node, nodes.section):
                if current_depth + 1 < node['depth']:
                    msg = ('Invalid deep section "%s" (<h%d>) appeared. Recognized a <h%d>.' %
                           (node.astext(), node['depth'], current_depth + 1))
                    self.document.reporter.warning(msg, source=node[0].source, line=node[0].line)
                    node['depth'] = current_depth + 1
                elif current_depth >= node['depth']:
                    # leave the section
                    for _ in range(current_depth - node['depth'] + 1):
                        if last_section is not None:
                            last_section = last_section.parent

                if last_section:
                    node.parent.remove(node)
                    last_section += node

                current_depth = node['depth']
                last_section = node
            else:
                if last_section:
                    node.parent.remove(node)
                    last_section += node


class InlineTransform(Transform):
    default_priority = 150

    def apply(self, **kwargs) -> None:
        def is_text_container(node: Node) -> bool:
            return isinstance(node, TextElement) and not isinstance(node, FixedTextElement)

        parser = self.create_parser()
        for node in self.document.traverse(is_text_container):  # type: TextElement
            parser.parse(node)

    def create_parser(self) -> InlineParser:
        parser = InlineParser()
        for processor in self.document.settings.inline_processors:
            parser.add_processor(processor(parser))

        return parser


class SparseTextConverter(Transform):
    default_priority = 250

    def apply(self, **kwargs) -> None:
        for node in self.document.traverse(addnodes.SparseText):
            pos = node.parent.index(node)
            node.parent.remove(node)
            node.parent.insert(pos, Text(str(node)))


class EmphasisConverter(Transform):
    default_priority = 250

    def __init__(self, document: Element, startnode: Node = None) -> None:
        # override __init__() to accept any Element node as ``document``.
        self.document = document  # type: ignore
        self.startnode = startnode
        self.language = None

    def apply(self, **kwargs) -> None:
        for node in self.document.traverse(TextElement):
            while True:
                markers = list(n for n in node.children if isinstance(n, addnodes.emphasis))
                closers = list(d for d in markers if d['can_close'])
                if len(closers) == 0:
                    break
                closer = closers[0]
                opener = self.find_opener(markers, closer)
                if opener is None:
                    closer['can_close'] = False
                    continue

                if opener['curr_length'] >= 2 and closer['curr_length'] >= 2:
                    length = 2
                    emph_node: Element = nodes.strong()
                else:
                    length = 1
                    emph_node = nodes.emphasis()

                transplant_nodes(node, emph_node, start=opener, end=closer)
                self.deactivate_markers(emph_node)

                opener_pos = node.index(opener)
                node.insert(opener_pos + 1, emph_node)
                opener.shrink(length)
                closer.shrink(length)

            self.deactivate_markers(node)

    def find_opener(self, markers: List[addnodes.emphasis], closer: addnodes.emphasis) -> addnodes.emphasis:
        pos = markers.index(closer)
        for opener in reversed(markers[:pos]):
            if opener['can_open'] is False:
                continue
            elif opener['marker'][0] != closer['marker'][0]:
                continue
            elif (opener['interior'] and opener['orig_length'] % 3 == 0 and
                  closer['interior'] and closer['orig_length'] % 3 == 0):
                return opener
            else:
                odd_match = ((closer['interior'] or opener['interior']) and
                             (opener['orig_length'] + closer['orig_length']) % 3 == 0)
                if not odd_match:
                    return opener

        return None

    def deactivate_markers(self, node: Element) -> None:
        markers = list(n for n in node.children if isinstance(n, addnodes.emphasis))
        for delim in markers:
            marker = str(delim)
            delim.replace_self(Text(marker, marker))


class BracketConverter(Transform):
    default_priority = 250

    def apply(self, **kwargs) -> None:
        for node in self.document.traverse(addnodes.bracket):
            node.replace_self(Text(node['marker']))


class TextNodeConnector(Transform):
    default_priority = SparseTextConverter.default_priority + 10

    def apply(self, **kwargs) -> None:
        for node in self.document.traverse(TextElement):
            pos = 0
            while len(node) > pos + 1:
                if isinstance(node[pos], Text) and isinstance(node[pos + 1], Text):
                    text = node[pos] + node[pos + 1]  # type: ignore
                    node.remove(node[pos + 1])
                    node.remove(node[pos])
                    node.insert(pos, Text(text, text))
                else:
                    pos += 1
