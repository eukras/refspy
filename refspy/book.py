"""Data object for a book.

Books have names, abbrevs (short names), and codes (suited to URL params), plus
any aliases it is known by.

Attributes:
    id: 13
    name: '1 Thesslonians'
    abbrev: '1 Thess'
    code: '1thess'
    depth: 2
    aliases: ['1 Th'],
    chapters: 5

If the book has a number (e.g. '1' Corinthians), then the
`refspy.language.Language` object's `number_prefixes` property defines any
substitute prefixes like 'I' or 'First'.

A book with only one chapter has a reference depth of 1, meaning only verse
numbers are used in its references. Depth may in future be used to support
books with sections (`depth=3`), otherwise we would just check if
`book.chapters == 1`.
"""

from typing import List
from pydantic import BaseModel

from refspy.number import Number


class Book(BaseModel):
    id: Number
    name: str
    abbrev: str
    code: str
    depth: int
    aliases: List[str]
    chapters: int
