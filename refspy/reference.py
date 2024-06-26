from typing import List, Self, Tuple

from pydantic import BaseModel, Field

from refspy.range import Range, range
from refspy.verse import Number, Verse, verse


class Reference(BaseModel):
    """
    A reference is a sorted, non-empty list of range objects.

    For unsorted, just use a list of references.
    """

    ranges: List[Range] = Field(min_length=1)

    def __add__(self, other: Self):
        return reference([*self.ranges, *other.ranges])

    def __lt__(self, other: Self):
        return self.ranges[0].start < other.ranges[0].start

    def insert(self, range: Range):
        position = 0
        while position < len(self.ranges):
            current = self.ranges[position]
            if current.start > range.start and current.end > range.end:
                self.ranges.insert(position, range)
                return  # <-- Done
            position += 1
        self.ranges.append(range)

    def equals(self, other: Self) -> bool:
        return self.ranges == other.ranges

    def count_books(self) -> int:
        book_ids = set()
        for _ in self.ranges:
            book_ids.add(_.start.book)
            book_ids.add(_.end.book)
        return len(book_ids)

    def merge_ranges(self) -> None:
        """
        for each sorted range:
            if adjacent or overlapping to next, combine them
        """
        new_ranges = []
        for new_range in self.ranges:
            if len(new_ranges) > 0 and (
                new_ranges[-1].overlaps(new_range) or new_ranges[-1].adjoins(new_range)
            ):
                new_ranges[-1].merge(new_range)
            else:
                new_ranges.append(new_range)
        self.ranges = new_ranges


def reference(points: List[Verse | Range | Tuple[Verse, Verse]]) -> Reference:
    """
    Construct a Reference object from a list of arguments which can be a Verse
    or a Tuple of Verses, representing a Range.

    ref = reference([
        verse(1, 2, 3, 4),
        range(verse(1, 2, 3, 6), verse(1, 2, 3, 7))
        verse(1,2,3,11)
    ])
    """
    ranges: List[Range] = []
    for _ in points:
        if isinstance(_, tuple):
            ranges.append(Range(start=_[0], end=_[1]))
        if isinstance(_, Range):
            ranges.append(_)
        if isinstance(_, Verse):
            ranges.append(Range(start=_, end=_))
    return Reference(ranges=sorted(ranges))


def book_reference(library_id: Number, book_id: Number) -> Reference:
    return reference(
        [
            range(
                verse(library_id, book_id, 1, 1),
                verse(library_id, book_id, 999, 999),
            )
        ]
    )


def is_book_reference(reference: Reference) -> bool:
    if len(reference.ranges) == 1:
        _ = reference.ranges[0]
        if all(
            [
                _.start.library == _.end.library,
                _.start.book == _.end.book,
                (_.start.chapter, _.end.chapter) == (1, 999),
                (_.start.verse, _.end.verse) == (1, 999),
            ]
        ):
            return True
    return False


def chapter_reference(
    library_id: Number, book_id: Number, chapter_id: Number
) -> Reference:
    return reference(
        [
            range(
                verse(library_id, book_id, chapter_id, 1),
                verse(library_id, book_id, chapter_id, 999),
            )
        ]
    )


def verse_reference(
    library_id: Number, book_id: Number, chapter_id: Number, verse_id: Number
) -> Reference:
    return reference(
        [
            range(
                verse(library_id, book_id, chapter_id, verse_id),
                verse(library_id, book_id, chapter_id, verse_id),
            )
        ]
    )


def last_start_verse(reference: Reference) -> Verse:
    if not reference.ranges:
        raise ValueError("No verse ranges in reference")
    return reference.ranges[-1].start
