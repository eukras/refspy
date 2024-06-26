from typing import Annotated, Tuple, Self

from annotated_types import Gt, Lt
from pydantic import BaseModel

Number = Annotated[int, Gt(0), Lt(1000)]
Index = Annotated[int, Gt(1001001001), Lt(999999999999)]

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
        """
        For tuple conversion, just make iterable

        (Which we would, except for TupleGenerator type issue in Pydantic.)
        """
        return (self.library, self.book, self.chapter, self.verse)

    @classmethod
    def from_index(cls, index: Index) -> Self:
        """
        Convert a verse's index number to it's tuple form.
        """
        lbc, v = divmod(index, 1000)
        lb, c = divmod(lbc, 1000)
        l, b = divmod(lb, 1000)
        print(l, b, c, v)
        return cls(library=l, book=b, chapter=c, verse=v)

    def __lt__(self, other: Self) -> bool:
        return self.tuple() < other.tuple()

    def __le__(self, other: Self) -> bool:
        return self.tuple() <= other.tuple()

    def __gt__(self, other: Self) -> bool:
        return self.tuple() > other.tuple()

    def __ge__(self, other: Self) -> bool:
        return self.tuple() >= other.tuple()

    def index(self) -> Index:
        """
        Convert a verse tuple to an indexing integer.

        e.g. (1, 2, 3, 4) -> 1002003004

        Assumes 1000 limit on numbers.
        """
        return (
            (self.library * 1000 + self.book) * 1000 + self.chapter
        ) * 1000 + self.verse


def verse(library: Number, book: Number, chapter: Number, verse: Number) -> Verse:
    """
    Shorthand constructor for Verse.
    """
    return Verse(library=library, book=book, chapter=chapter, verse=verse)
