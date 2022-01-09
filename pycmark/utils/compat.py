"""
    pycmark.utils.compat
    ~~~~~~~~~~~~~~~~~~~~

    Utilities for compatibility.

    :copyright: Copyright 2017-2019 by Takeshi KOMIYA
    :license: Apache License 2.0, see LICENSE for details.
"""

from typing import Any, Generator

from docutils.nodes import Node

if not hasattr(Node, 'findall'):  # for docutils-0.17 or older
    def findall(self, *args: Any, **kwargs: Any) -> Generator[Node, None, None]:
        for node in self.traverse(*args, **kwargs):
            yield node

    Node.findall = findall  # type: ignore
