from typing import List, Self, Tuple
from pydantic import BaseModel, model_validator

from refspy.verse import Number, verse, Verse
from refspy.utils import string_together

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
        return any(
            [
                other.start <= self.start <= other.end,
                other.start <= self.end <= other.end,
                self.start <= other.start <= self.end,
                self.start <= other.end <= self.end,
            ]
        )

    def contains(self, other: Self) -> bool:
        return self.start <= other.start and self.end >= other.end

    def adjoins(self, other: Self) -> bool:
        """
        To keep things simple, a range adjoins another if:
        - It is a verse or range in the same chapter, and is located one verse away
        - It is a chapter in the same book, and is located one chapter away
        """
        if self.same_chapter_as(other):
            return (
                other.start.verse == self.end.verse + 1
                or self.start.verse == other.end.verse + 1
            )
        elif self.same_book_as(other):
            return (
                other.start.chapter == self.end.chapter + 1
                or self.start.chapter == other.end.chapter + 1
            )
        else:
            return False

    def same_library_as(self, other: Self) -> bool:
        ids = {
            self.start.library,
            self.end.library,
            other.start.library,
            other.end.library,
        }
        return len(ids) == 1

    def same_book_as(self, other: Self) -> bool:
        ids = {self.start.book, self.end.book, other.start.book, other.end.book}
        return self.same_library_as(other) and len(ids) == 1

    def same_chapter_as(self, other: Self) -> bool:
        ids = {
            self.start.chapter,
            self.end.chapter,
            other.start.chapter,
            other.end.chapter,
        }
        return self.same_book_as(other) and len(ids) == 1

    def single_library(self) -> bool:
        return self.start.library == self.end.library

    def single_book(self) -> bool:
        return self.single_library() and self.start.book == self.end.book

    def single_chapter(self) -> bool:
        return self.single_book() and self.start.chapter == self.end.chapter

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
