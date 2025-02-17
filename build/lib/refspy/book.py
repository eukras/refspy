"""Data object for a book.

Books are referenced by their names, abbrevs (short names), and aliases.

Attributes:
    id: 13
    name: '1 Thesslonians'
    abbrev: '1 Thess'
    aliases: ['1 Th'],
    chapters: 5

Note:
    Aliases should be capitalised.

If the book has a number (e.g. '1' Corinthians), then the
`refspy.language.Language` object's `number_prefixes` property defines any
substitute prefixes like 'I' or 'First'.

A book with only one chapter will be formatted without chapter numbers.
"""

from typing import List
from pydantic import BaseModel

from refspy.number import Number


class Book(BaseModel):
    id: Number
    name: str
    abbrev: str
    aliases: List[str]
    chapters: int
