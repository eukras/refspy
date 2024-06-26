from typing import List, Self, Tuple
from pydantic import BaseModel, model_validator

from refspy.verse import Number, verse, Verse

RangeTuple = Tuple[Verse, Verse]
RangeList = List[RangeTuple]


class Range(BaseModel):
    start: Verse
    end: Verse

    def tuple(self) -> RangeTuple:
        return (self.start, self.end)

    @model_validator(mode="after")
    def check_verse_order(self) -> Self:
        assert tuple(self.start) <= tuple(self.end)
        return self

    def __lt__(self, other: Self) -> bool:
        return tuple(self) < tuple(other)

    def get_library_and_book(self) -> Tuple[Number, Number]:
        return (self.start.library, self.start.book)

    def overlaps(self, other: Self) -> bool:
        return (self.start <= other.start and self.end >= other.start) or (
            self.start <= other.end and self.end >= other.end
        )

    def contains(self, other: Self) -> bool:
        return self.start <= other.start and self.end >= other.end

    def single_chapter(self) -> bool:
        return all(
            [
                len(set([self.start.library, self.end.library])) == 1,
                len(set([self.start.book, self.end.book])) == 1,
                len(set([self.start.chapter, self.end.chapter])) == 1,
            ]
        )

    def is_book_range(self) -> bool:
        return all(
            [
                self.start.library == self.end.library,
                self.start.book != self.end.book,
                self.start.chapter == 1,
                self.end.chapter == 999,
                self.start.verse == 1,
                self.end.verse == 999,
            ]
        )

    def is_inter_book_range(self) -> bool:
        return all(
            [
                self.start.library == self.end.library,
                self.start.book != self.end.book,
                any(
                    [
                        self.start.chapter != 1,
                        self.end.chapter != 999,
                    ]
                ),
            ]
        )

    def is_book(self) -> bool:
        return all(
            [
                self.start.library == self.end.library,
                self.start.book == self.end.book,
                self.start.chapter == 1,
                self.end.chapter == 999,
                self.start.verse == 1,
                self.end.verse == 999,
            ]
        )

    def is_chapter_range(self) -> bool:
        return all(
            [
                self.start.library == self.end.library,
                self.start.book == self.end.book,
                self.start.chapter != self.end.chapter,
                self.start.verse == 1,
                self.end.verse == 999,
            ]
        )

    def is_inter_chapter_range(self) -> bool:
        return all(
            [
                self.start.library == self.end.library,
                self.start.book == self.end.book,
                self.start.chapter != self.end.chapter,
                any(
                    [
                        self.start.verse != 1,
                        self.end.verse != 999,
                    ]
                ),
            ]
        )

    def is_chapter(self) -> bool:
        return all(
            [
                self.start.library == self.end.library,
                self.start.book == self.end.book,
                self.start.chapter == self.end.chapter,
                self.start.verse == 1,
                self.end.verse == 999,
            ]
        )

    def is_verse_range(self) -> bool:
        return all(
            [
                self.start.library == self.end.library,
                self.start.book == self.end.book,
                self.start.chapter == self.end.chapter,
                self.start.verse != self.end.verse,
            ]
        )

    def is_verse(self) -> bool:
        return all(
            [
                self.start.library == self.end.library,
                self.start.book == self.end.book,
                self.start.chapter == self.end.chapter,
                self.start.verse == self.end.verse,
            ]
        )

    def adjoins(self, other: Self) -> bool:
        return False


class ChapterRange(Range):
    @model_validator(mode="after")
    def check_chapter_range(self) -> Self:
        assert self.start.verse == 1 and self.end.verse == 999
        return self


class BookRange(ChapterRange):
    @model_validator(mode="after")
    def check_book_range(self) -> Self:
        assert self.start.chapter == 1 and self.end.chapter == 999
        return self


def range(start: Verse, end: Verse) -> Range:
    """
    Shorthand contructor for Range.
    """
    return Range(start=start, end=end)


def chapter_range(start: Verse, end: Verse) -> ChapterRange:
    """
    Shorthand contructor for Range.
    """
    return ChapterRange(start=start, end=end)


def book_range(start: Verse, end: Verse) -> BookRange:
    """
    Shorthand contructor for Range.
    """
    return BookRange(start=start, end=end)


def chapter(library: Number, book: Number, chapter: Number) -> ChapterRange:
    """
    Shorthand constructor for BookRange
    """
    return chapter_range(
        verse(library, book, chapter, 1), verse(library, book, chapter, 999)
    )


def book(library: Number, book: Number) -> BookRange:
    """
    Shorthand constructor for BookRange
    """
    return book_range(verse(library, book, 1, 1), verse(library, book, 999, 999))
