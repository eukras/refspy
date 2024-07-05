"""Data object for a library of books.

Libraries have names, abbrevs (short names), and a list of the books that they
contain.

Attributes:
    id: 7
    name: '1 Corinthians'
    abbrev: '1 Cor'
    books: [],

See `refspy.libraries.en_US` for a complete example.
"""

from typing import List

from pydantic import BaseModel

from refspy.book import Book
from refspy.number import Number


class Library(BaseModel):
    id: Number
    name: str
    abbrev: str
    books: List[Book]
