# -*- coding: utf-8 -*-
"""
    pycmark
    ~~~~~~~

    CommonMark parser for docutils.

    :copyright: Copyright 2017 by Takeshi KOMIYA
    :license: BSD, see LICENSE for details.
"""

from docutils import nodes
from docutils.parsers import Parser
from pycmark.readers import LineReader
from pycmark.blockparser import BlockParser
from pycmark.blockparser.std_processors import (
    ThematicBreakProcessor,
    ATXHeadingProcessor,
    IndentedCodeBlockProcessor,
    BlankLineProcessor,
    FencedCodeBlockProcessor,
    ParagraphProcessor,
)
from pycmark.blockparser.html_processors import (
    ScriptHTMLBlockProcessor,
    CommentHTMLBlockProcessor,
    ProcessingInstructionHTMLBlockProcessor,
    DeclarationHTMLBlockProcessor,
    CdataHTMLBlockProcessor,
    StandardTagsHTMLBlockProcessor,
    CompleteTagsHTMLBlockProcessor,
)
from pycmark.blockparser.container_processors import (
    BlockQuoteProcessor,
    BulletListProcessor,
    NonEmptyBulletListProcessor,
    OrderedListProcessor,
    OneBasedOrderedListProcessor,
)
from pycmark.inlineparser import InlineParser
from pycmark.inlineparser.std_processors import (
    BackslashEscapeProcessor,
    EntityReferenceProcessor,
    CodeSpanProcessor,
    EmphasisProcessor,
    AutolinkProcessor,
)
from pycmark.transforms import (
    TightListsDetector,
    TightListsCompactor,
    BlanklineFilter,
    SparseTextConverter,
    EmphasisConverter,
    TextNodeConnector,
)


def is_text_container(node):
    return isinstance(node, nodes.TextElement) and not isinstance(node, nodes.FixedTextElement)


class CommonMarkParser(Parser):
    """CommonMark parser for docutils."""

    supported = ('markdown', 'commonmark', 'md')

    def get_block_processors(self):
        """Returns block processors. Overrided by subclasses."""
        return [
            ThematicBreakProcessor,
            ATXHeadingProcessor,
            IndentedCodeBlockProcessor,
            BlankLineProcessor,
            FencedCodeBlockProcessor,
            ScriptHTMLBlockProcessor,
            CommentHTMLBlockProcessor,
            ProcessingInstructionHTMLBlockProcessor,
            DeclarationHTMLBlockProcessor,
            CdataHTMLBlockProcessor,
            StandardTagsHTMLBlockProcessor,
            CompleteTagsHTMLBlockProcessor,
            BlockQuoteProcessor,
            BulletListProcessor,
            NonEmptyBulletListProcessor,
            OrderedListProcessor,
            OneBasedOrderedListProcessor,
            ParagraphProcessor,
        ]

    def get_inline_processors(self):
        """Returns inline processors. Overrided by subclasses."""
        return [
            BackslashEscapeProcessor,
            EntityReferenceProcessor,
            CodeSpanProcessor,
            EmphasisProcessor,
            AutolinkProcessor,
        ]

    def get_transforms(self):
        return [
            TightListsDetector,
            TightListsCompactor,
            BlanklineFilter,
            SparseTextConverter,
            EmphasisConverter,
            TextNodeConnector,
        ]

    def create_block_parser(self):
        """Creates a block parser and returns it.

        Internally, ``get_block_processors()`` is called to create a parser.
        So you can change the processors by subclassing.
        """
        parser = BlockParser()
        for processor in self.get_block_processors():
            parser.add_processor(processor(parser))
        return parser

    def create_inline_parser(self):
        """Creates a inline parser and returns it.

        Internally, ``get_inline_processors()`` is called to create a parser.
        So you can change the processors by subclassing."""
        parser = InlineParser()
        for processor in self.get_inline_processors():
            parser.add_processor(processor(parser))
        return parser

    def parse(self, inputtext, document):
        """Parses a text and build document."""
        reader = LineReader(inputtext.splitlines(True), source=document['source'])
        block_parser = self.create_block_parser()
        block_parser.parse(reader, document)

        inline_parser = self.create_inline_parser()
        for node in document.traverse(is_text_container):
            inline_parser.parse(node)
