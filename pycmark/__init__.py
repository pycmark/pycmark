"""
    pycmark
    ~~~~~~~

    CommonMark parser for docutils.

    :copyright: Copyright 2017-2019 by Takeshi KOMIYA
    :license: Apache License 2.0, see LICENSE for details.
"""

from typing import List, Type

from docutils import nodes, parsers
from docutils.transforms import Transform

import pycmark.utils.compat  # Patch docutils  # NOQA
from pycmark.blockparser import BlockParser, BlockProcessor
from pycmark.blockparser.container_processors import (
    BlockQuoteProcessor,
    BulletListProcessor,
    NonEmptyBulletListProcessor,
    OneBasedOrderedListProcessor,
    OrderedListProcessor,
)
from pycmark.blockparser.html_processors import (
    CdataHTMLBlockProcessor,
    CommentHTMLBlockProcessor,
    CompleteTagsHTMLBlockProcessor,
    DeclarationHTMLBlockProcessor,
    ProcessingInstructionHTMLBlockProcessor,
    ScriptHTMLBlockProcessor,
    StandardTagsHTMLBlockProcessor,
)
from pycmark.blockparser.link_processors import (
    LinkReferenceDefinitionProcessor
)
from pycmark.blockparser.std_processors import (
    ATXHeadingProcessor,
    BacktickFencedCodeBlockProcessor,
    BlankLineProcessor,
    IndentedCodeBlockProcessor,
    ParagraphProcessor,
    SetextHeadingProcessor,
    ThematicBreakProcessor,
    TildeFencedCodeBlockProcessor,
)
from pycmark.inlineparser import InlineProcessor
from pycmark.inlineparser.link_processors import (
    LinkCloserProcessor,
    LinkOpenerProcessor,
)
from pycmark.inlineparser.std_processors import (
    BackslashEscapeProcessor,
    CodeSpanProcessor,
    EmailAutolinkProcessor,
    EmphasisProcessor,
    EntityReferenceProcessor,
    HardLinebreakProcessor,
    RawHTMLProcessor,
    SoftLinebreakProcessor,
    URIAutolinkProcessor,
)
from pycmark.readers import LineReader
from pycmark.transforms import (
    BlanklineFilter,
    BracketConverter,
    EmphasisConverter,
    InlineTransform,
    LinebreakFilter,
    SectionTreeConstructor,
    SparseTextConverter,
    TextNodeConnector,
    TightListsCompactor,
    TightListsDetector,
)


class Parser(parsers.Parser):
    """CommonMark parser for docutils."""

    supported = ('markdown', 'commonmark', 'md')

    def get_block_processors(self) -> List[Type[BlockProcessor]]:
        """Returns block processors. Overrided by subclasses."""
        return [
            ATXHeadingProcessor,
            BacktickFencedCodeBlockProcessor,
            BlankLineProcessor,
            BlockQuoteProcessor,
            BulletListProcessor,
            CdataHTMLBlockProcessor,
            CommentHTMLBlockProcessor,
            CompleteTagsHTMLBlockProcessor,
            DeclarationHTMLBlockProcessor,
            IndentedCodeBlockProcessor,
            LinkReferenceDefinitionProcessor,
            NonEmptyBulletListProcessor,
            OneBasedOrderedListProcessor,
            OrderedListProcessor,
            ParagraphProcessor,
            ProcessingInstructionHTMLBlockProcessor,
            ScriptHTMLBlockProcessor,
            SetextHeadingProcessor,
            StandardTagsHTMLBlockProcessor,
            ThematicBreakProcessor,
            TildeFencedCodeBlockProcessor,
        ]

    def get_inline_processors(self) -> List[Type[InlineProcessor]]:
        """Returns inline processors. Overrided by subclasses."""
        return [
            BackslashEscapeProcessor,
            CodeSpanProcessor,
            EmailAutolinkProcessor,
            EmphasisProcessor,
            EntityReferenceProcessor,
            HardLinebreakProcessor,
            LinkCloserProcessor,
            LinkOpenerProcessor,
            RawHTMLProcessor,
            SoftLinebreakProcessor,
            URIAutolinkProcessor,
        ]

    def get_transforms(self) -> List[Type[Transform]]:
        return [
            BlanklineFilter,
            BracketConverter,
            EmphasisConverter,
            InlineTransform,
            LinebreakFilter,
            SectionTreeConstructor,
            SparseTextConverter,
            TextNodeConnector,
            TightListsCompactor,
            TightListsDetector,
        ]

    def create_block_parser(self) -> BlockParser:
        """Creates a block parser and returns it.

        Internally, ``get_block_processors()`` is called to create a parser.
        So you can change the processors by subclassing.
        """
        parser = BlockParser()
        for processor in self.get_block_processors():
            parser.add_processor(processor(parser))
        return parser

    def parse(self, inputtext: str, document: nodes.document) -> None:
        """Parses a text and build document."""
        document.settings.inline_processors = self.get_inline_processors()
        reader = LineReader(inputtext.splitlines(True), source=document['source'])
        block_parser = self.create_block_parser()
        block_parser.parse(reader, document)
