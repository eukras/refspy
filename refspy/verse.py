"""Data object for a verse.

Attributes:
    library: 1
    book: 2
    chapter: 3
    verse: 4
"""

from typing import Tuple, Self

from pydantic import BaseModel

from refspy.index import Index
from refspy.number import Number


VerseTuple = Tuple[Number, Number, Number, Number]


class Verse(BaseModel):
    """
    Library, Book, Chapter, Verse
    """

    library: Number
    book: Number
    chapter: Number
    verse: Number

    def tuple(self) -> VerseTuple:
        """A sortable tuple for comparison operations."""
        return (self.library, self.book, self.chapter, self.verse)

    def __lt__(self, other: Self) -> bool:
        """Compare verses by comparing tuples."""
        return self.tuple() < other.tuple()

    def __le__(self, other: Self) -> bool:
        """Compare verses by comparing tuples."""
        return self.tuple() <= other.tuple()

    def __gt__(self, other: Self) -> bool:
        """Compare verses by comparing tuples."""
        return self.tuple() > other.tuple()

    def __ge__(self, other: Self) -> bool:
        """Compare verses by comparing tuples."""
        return self.tuple() >= other.tuple()

    @classmethod
    def from_index(cls, index: Index) -> Self:
        """
        Convert a verse's index number to its tuple form.

        Example:
            ```
            verse = Verse.from_index(1002003004)
            ```
        """
        lbc, v = divmod(index, 1000)
        lb, c = divmod(lbc, 1000)
        l, b = divmod(lb, 1000)
        return cls(library=l, book=b, chapter=c, verse=v)

    def index(self) -> Index:
        """Create a `refspy.index.Index` number representing this verse.

        Example:
            `verse(1, 2, 3, 4)` becomes `1002003004`
        """
        return (
            (self.library * 1000 + self.book) * 1000 + self.chapter
        ) * 1000 + self.verse


def verse(library: Number, book: Number, chapter: Number, verse: Number) -> Verse:
    """A shorthand constructor for verses."""
    return Verse(library=library, book=book, chapter=chapter, verse=verse)
