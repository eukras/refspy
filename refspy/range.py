"""Data object for verse ranges."""

from typing import List, Self, Tuple
from pydantic import BaseModel, model_validator

from refspy.number import Number
from refspy.verse import verse, Verse


class Range(BaseModel):
    start: Verse
    end: Verse

    def tuple(self) -> Tuple[Verse, Verse]:
        return (self.start, self.end)

    @model_validator(mode="after")
    def check_verse_order(self) -> Self:
        """Enforce verse order within the Range.

        Raises:
            ValueError: If the start verse is greater than the end verse.
        """
        assert tuple(self.start) <= tuple(self.end)
        return self

    def __lt__(self, other: Self) -> bool:
        return tuple(self) < tuple(other)

    def overlaps(self, other: Self) -> bool:
        """Determine whether this reference overlaps the other.

        Overlap is when either's start or end falls within the other's range.

        Used in `refspy.reference.reference.overlaps()`
        """
        return any(
            [
                other.start <= self.start <= other.end,
                other.start <= self.end <= other.end,
                self.start <= other.start <= self.end,
                self.start <= other.end <= self.end,
            ]
        )

    def contains(self, other: Self) -> bool:
        """Determine whether this reference contains the other.

        Containment is when this reference's range includes the other's start
        and end.

        Used in `refspy.reference.reference.contains()`
        """
        return self.start <= other.start and self.end >= other.end

    def adjoins(self, other: Self) -> bool:
        """Determine whether this reference is adjacent to the other.

        Adjacency determines whether two ranges can be joined by
        `refspy.ranges.join_ranges()`.

        To keep things simple while covering most normal cases, adjacency is
        when:

        * Two verse ranges are adjacent.
        * Two inter-chapter verse ranges are adjacent.
        * Two chapter_range references are adjacent.
        * Two book_range references are adjacent.

        Note:
            We do not calculate adjacency for inter-book or inter-chapter
            references.
        """
        if any(
            [self.is_verse(), self.is_verse_range(), self.is_inter_chapter_range()]
        ) and any(
            [other.is_verse(), other.is_verse_range(), other.is_inter_chapter_range()]
        ):
            return (
                other.start.verse == self.end.verse + 1
                or self.start.verse == other.end.verse + 1
            )
        elif (
            self.same_book_as(other)
            and (self.is_chapter() or self.is_chapter_range())
            and (other.is_chapter() or other.is_chapter_range())
        ):
            return (
                other.start.chapter == self.end.chapter + 1
                or self.start.chapter == other.end.chapter + 1
            )
        elif (
            self.same_library_as(other)
            and (self.is_book() or self.is_book_range())
            and (other.is_book() or other.is_book_range())
        ):
            return (
                other.start.book == self.end.book + 1
                or self.start.book == other.end.book + 1
            )
        else:
            return False

    def merge(self, other: Self) -> Self:
        """Combine two overlapping ranges."""
        min_start_c, min_start_v = min(
            (self.start.chapter, self.start.verse),
            (other.start.chapter, other.start.verse),
        )
        max_end_c, max_end_v = max(
            (self.end.chapter, self.end.verse),
            (other.end.chapter, other.end.verse),
        )
        return self.__class__(
            start=verse(
                min(self.start.library, other.start.library),
                min(self.start.book, other.start.book),
                min_start_c,
                min_start_v,
            ),
            end=verse(
                max(self.end.library, other.end.library),
                max(self.end.book, other.end.book),
                max_end_c,
                max_end_v,
            ),
        )

    def join(self, other: Self):
        """Combine two adjacent ranges."""
        if self.start < other.start:
            return self.__class__(start=self.start, end=other.end)
        else:
            return self.__class__(start=other.start, end=self.end)

    def is_same_library(self) -> bool:
        return self.start.library == self.end.library

    def same_library_as(self, other: Self) -> bool:
        """Determine if two ranges are in the same library."""
        ids = set(
            [
                self.start.library,
                self.end.library,
                other.start.library,
                other.end.library,
            ]
        )
        return len(ids) == 1

    def is_same_book(self) -> bool:
        return self.is_same_library() and self.start.book == self.end.book

    def same_book_as(self, other: Self) -> bool:
        """Determine if two references are in the same book.

        To be in the same book they must also be in the same library.
        """
        ids = set([self.start.book, self.end.book, other.start.book, other.end.book])
        return self.same_library_as(other) and len(ids) == 1

    def is_same_chapter(self) -> bool:
        return (
            self.is_same_library()
            and self.is_same_book()
            and self.start.chapter == self.end.chapter
        )

    def same_chapter_as(self, other: Self) -> bool:
        """Determine if two references are in the same book.

        To be in the same book they must also be in the same library.
        """
        ids = {
            self.start.chapter,
            self.end.chapter,
            other.start.chapter,
            other.end.chapter,
        }
        return self.same_book_as(other) and len(ids) == 1

    def is_book(self) -> bool:
        """Determine if this range covers one whole book.

        Example:
            `Matthew`
        """
        return all(
            [
                self.start.library == self.end.library,
                self.start.book == self.end.book,
                (self.start.chapter, self.end.chapter) == (1, 999),
                (self.start.verse, self.end.verse) == (1, 999),
            ]
        )

    def is_book_range(self) -> bool:
        """Determine if this range goes from one whole book to another whole book.

        Example:
            `Matthew-John`
        """
        return all(
            [
                self.start.library == self.end.library,
                self.start.book != self.end.book,
                (self.start.chapter, self.end.chapter) == (1, 999),
                (self.start.verse, self.end.verse) == (1, 999),
            ]
        )

    def is_inter_book_range(self) -> bool:
        """Determine if this range spans multiple books.

        Example:
            `Matt 1:2-Mark 3:4`
        """
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

    def is_chapter(self) -> bool:
        """Determine if this range covers one whole chapter.

        Example:
            `Matthew 7`
        """
        return all(
            [
                self.start.library == self.end.library,
                self.start.book == self.end.book,
                self.start.chapter == self.end.chapter,
                (self.start.verse, self.end.verse) == (1, 999),
            ]
        )

    def is_chapter_range(self) -> bool:
        """Determine if this range goes from one whole chapter to another whole
        chapter.

        Example:
            `Matthew 5-8`
        """
        return all(
            [
                self.start.library == self.end.library,
                self.start.book == self.end.book,
                self.start.chapter != self.end.chapter,
                (self.start.verse, self.end.verse) == (1, 999),
            ]
        )

    def is_inter_chapter_range(self) -> bool:
        """Determine if this range spans multiple chapters within the same book.

        Example:
            `Matthew 1:2-3:4`
        """
        return all(
            [
                self.start.library == self.end.library,
                self.start.book == self.end.book,
                self.start.chapter != self.end.chapter,
                (self.start.verse, self.end.verse) != (1, 999),
            ]
        )

    def is_verse(self) -> bool:
        """Determine if this range covers one verse only.

        Example:
            `Matthew 7:8`
        """
        return all(
            [
                self.start.library == self.end.library,
                self.start.book == self.end.book,
                self.start.chapter == self.end.chapter,
                self.start.verse == self.end.verse,
            ]
        )

    def is_verse_range(self) -> bool:
        """Determine if this range covers multiple verses within the same book
        and chapter.

        Example:
            `Matthew 7:8-12`
        """
        return all(
            [
                self.start.library == self.end.library,
                self.start.book == self.end.book,
                self.start.chapter == self.end.chapter,
                self.start.verse != self.end.verse,
            ]
        )


def range(start: Verse, end: Verse) -> Range:
    """A shorthand contructor for Range objects.

    Args:
        start: the `refspy.verse.Verse` at the start of the range.
        end: the `refspy.verse.Verse` at the end of the range.

    Note:
        To specify a single verse reference, supply a range with
        the same verse as the start and the end.
    """
    return Range(start=start, end=end)


def merge(ranges: List[Range], skip_sort: bool = False) -> List[Range]:
    """Merge overlapping ranges within a sorted list.

    This performs a sort before merging unless skip_sort=True.
    """
    if not ranges:
        return []
    sorted_ranges = ranges if skip_sort else sorted(ranges)
    new_ranges = []
    last_range = sorted_ranges[0]
    if sorted_ranges:
        for this_range in sorted_ranges[1:]:
            if last_range.overlaps(this_range):
                last_range = last_range.merge(this_range)
            else:
                new_ranges.append(last_range)
                last_range = this_range
    new_ranges.append(last_range)
    return new_ranges


def combine(ranges: List[Range], skip_merge: bool = False) -> List[Range]:
    """Join adjacent ranges within a sorted and merged list

    This performs a sort and merge before combining, unless skip_merge=True.
    """
    if not ranges:
        return []
    merged_ranges = ranges if skip_merge else merge(ranges)
    new_ranges = []
    last_range = merged_ranges[0]
    if merged_ranges:
        for this_range in merged_ranges[1:]:
            if last_range.adjoins(this_range):
                last_range = last_range.join(this_range)
            else:
                new_ranges.append(last_range)
                last_range = this_range
    new_ranges.append(last_range)
    return new_ranges


def book_range(
    library_id: Number, book_id: Number, book_end_id: Number | None = None
) -> Range:
    """
    Shorthand function for creating book references from `refspy.number.Number`
    values.
    """
    return range(
        verse(library_id, book_id, 1, 1),
        verse(library_id, book_end_id or book_id, 999, 999),
    )


def chapter_range(
    library_id: Number,
    book_id: Number,
    chapter_id: Number,
    chapter_end_id: Number | None = None,
) -> Range:
    """
    Shorthand function for creating chapter references from
    `refspy.number.Number` values.
    """
    return range(
        verse(library_id, book_id, chapter_id, 1),
        verse(library_id, book_id, chapter_end_id or chapter_id, 999),
    )


def verse_range(
    library_id: Number,
    book_id: Number,
    chapter_id: Number,
    verse_id: Number,
    verse_end_id: Number | None = None,
) -> Range:
    """
    Shorthand function for creating verse or range references from
    `refspy.number.Number` values.

    See `refspy.manager.Manager.bcv`
    """
    return range(
        verse(library_id, book_id, chapter_id, verse_id),
        verse(library_id, book_id, chapter_id, verse_end_id or verse_id),
    )
