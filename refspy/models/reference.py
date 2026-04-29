"""Data object for references.

References consist of lists of ranges and are entirely numerical objects.

They can be set to sort, merge, and join references when added together.
"""

import collections
from typing import Any, Self

from pydantic import BaseModel, Field

from refspy.types.number import Number
from refspy.models.range import Range, combine_ranges, merge_ranges, range as _range
from refspy.models.verse import Verse, verse


class Reference(BaseModel):
    """A reference object represents a list of verse ranges.

    References are entirely numeric entities. Matchers are used to find them in
    text, and formatters are used to turn them in to canonical links.

    It is common to want references to be sorted and combined. Combining means
    merging overlapping ranges and joining adjacent ones. This is done by creating
    references with sorted(), and the `merge`, and `combine` functions in
    `refspy.range.Range`, or calling the methods of the same name on references.

    Example:
        ```
        from reference import merge, combine

        assert reference(*sorted(ranges)) == reference(*ranges).sort()
        assert reference(*merge(ranges)) == reference(*ranges).merge()
        assert reference(*combine(ranges)) == reference(*ranges).combine()
        ```
    """

    ranges: list[Range] = Field(min_length=1)
    """
    A reference must contain at least one `refspy.range.Range`.

    Raises:
        ValueError: If ranges is empty
    """

    def tuple(self) -> tuple:
        """For hashing and comparisons"""
        return tuple([hash(_) for _ in self.ranges])

    def __hash__(self) -> int:
        """Unique ID for key values."""
        return hash(self.tuple())

    def __eq__(self, other) -> bool:  # <-- Should be Self; TypeError requires object
        return self.tuple() == other.tuple()

    def __add__(self, other: Self) -> Self:
        """Overload the addition operator to combine reference ranges into a new object."""
        return self.__class__(ranges=[*self.ranges, *other.ranges])

    def __lt__(self, other: Self) -> bool:
        """
        A simple implementation of '<' allows sorting and min/max.
        """
        common = min(len(self.ranges), len(other.ranges))
        for i in range(0, common):
            if self.ranges[i].start != other.ranges[i].start:
                return self.ranges[i].start < other.ranges[i].start
            if self.ranges[i].end != other.ranges[i].end:
                return self.ranges[i].end < other.ranges[i].end
        return False  # <-- all equal

    def equals(self, other: Self) -> bool:
        """
        Reference equality means that two references have identical ranges.

        Note:
            We don't use __eq__, as that is already defined in BaseModel.
        """
        return self.ranges == other.ranges

    def overlaps(self, other: Self) -> bool:
        """
        Two references overlap if ANY of their ranges overlap.
        """
        return any(
            [
                self_range.overlaps(other_range)
                for other_range in other.ranges
                for self_range in self.ranges
            ]
        )

    def contains(self, other: Self) -> bool:
        """
        A reference contains another if ALL the other's ranges are contained by
        ANY of it's own ranges.
        """
        return all(
            [
                any([self_range.contains(other_range) for self_range in self.ranges])
                for other_range in other.ranges
            ]
        )

    def adjoins(self, other: Self) -> bool:
        """Determine adjacency for ranges.

        A reference adjoins another if its maximum range adjoins the other's
        minimum or vice-versa. This usually only makes sense for simple
        references with a small number of ranges.

        See `refspy.reference.Reference.adjoins`.
        """
        return any(
            [
                max(self.ranges).adjoins(min(other.ranges)),
                min(self.ranges).adjoins(max(other.ranges)),
            ]
        )

    def count_books(self) -> int:
        """Return the total unique books contained in this reference.

        Allow that the same book ID could appear in multiple libraries.
        """
        library_books = set()
        for _ in self.ranges:
            library_books.add(tuple([_.start.library, _.start.book]))
            library_books.add(tuple([_.end.library, _.end.book]))
        return len(library_books)

    def is_book(self: Self) -> bool:
        """Determine if reference is a whole book."""
        return self.ranges[0].is_book()

    def is_chapter(self: Self) -> bool:
        """Determine if reference is a whole chapter."""
        return self.ranges[0].is_chapter()

    def first_verse(self) -> Verse:
        """Find the first verse.

        Only sensible if sorted=True

        Note:
            Consider sorting on the fly if sorted=False
        """
        return self.ranges[0].start

    def last_verse(self) -> Verse:
        """Find the last verse.

        Only sensible if sorted=True

        Note:
            Consider sorting on the fly if sorted=False
        """
        return self.ranges[-1].end

    def last_range(self) -> Range:
        """Find the last verse.

        Only sensible if sorted=True

        Note:
            Consider sorting on the fly if sorted=False
        """
        return self.ranges[-1]

    def sort(self) -> Self:
        """Return a sorted reference."""
        return self.__class__(ranges=sorted(self.ranges))

    def merge(self) -> Self:
        """Return a merged reference.

        A merged reference is sorted, and has any overlapping ranges merged.
        """
        return self.__class__(ranges=merge_ranges(self.ranges))

    def combine(self) -> Self:
        """Return a combined reference.

        A combined reference is sorted, merged, and has any adjacent ranges combined.
        """
        return self.__class__(ranges=combine_ranges(self.ranges))


# -----------------------------------
# Shorthand constructor functions
# -----------------------------------


def reference(*args: Range, **kwargs: Any) -> Reference:
    """
    Construct a Reference object from `refspy.range.Range` arguments.

    Example:
        ```
        ref = reference(
            _range(verse(1, 2, 3, 3), verse(1, 2, 3, 4)),
            _range(verse(1, 2, 3, 6), verse(1, 2, 3, 7))
        )
        ```
    """
    return Reference(ranges=list(args), **kwargs)


def book_reference(library_id: Number, book_id: Number) -> Reference:
    """
    Shorthand function for creating book references from `refspy.number.Number`
    values.
    """
    return reference(
        _range(
            verse(library_id, book_id, 1, 1),
            verse(library_id, book_id, 999, 999),
        )
    )


def chapter_reference(
    library_id: Number, book_id: Number, chapter_id: Number
) -> Reference:
    """
    Shorthand function for creating chapter references from
    `refspy.number.Number` values.
    """
    return reference(
        _range(
            verse(library_id, book_id, chapter_id, 1),
            verse(library_id, book_id, chapter_id, 999),
        )
    )


def verse_reference(
    library_id: Number,
    book_id: Number,
    chapter_id: Number,
    verse_id: Number,
    verse_end_id: Number | None = None,
) -> Reference:
    """
    Shorthand function for creating verse or range references from
    `refspy.number.Number` values.

    See `refspy.manager.Manager.bcv`
    """
    return reference(
        _range(
            verse(library_id, book_id, chapter_id, verse_id),
            verse(library_id, book_id, chapter_id, verse_end_id or verse_id),
        )
    )


# -----------------------------------
# Manipulation functions
# -----------------------------------


def sort_references(references: list[Reference]) -> list[Reference]:
    """
    Return the same references in sorted order based on their ranges.

    References implement `__lt__()`, so are innately sortable.

    Note:
        - use `unique_references(sorted_references(references))` to make the
          sorted list unique.
    """
    return sorted(references)


def unique_references(references: list[Reference]) -> list[Reference]:
    """
    Return references in the same order, but without duplicates

    References implement `__hash__()`, so can be used in sets. Sets retain
    the order of inserted items.
    """
    ordered = {hash(ref): ref for ref in references}
    return list(ordered.values())


def split_reference(reference: Reference) -> list[Reference]:
    """Split a single references into a list of references, one for each range it contains."""
    references = []
    for rng in reference.ranges:
        references.append(Reference(ranges=[rng]))
    return references


def join_references(references: list[Reference]) -> Reference:
    """Join a list of references into a single reference"""
    ranges = []
    for ref in references:
        for rng in ref.ranges:
            ranges.append(rng)
    return reference(*ranges)


def count_references(references: list[Reference]) -> list[tuple[Reference, int]]:
    """
    Return tuples [(ref, count)].

    Because references implement __hash__(), this can be done with the
    `collections.Counter`. Transform the resulting dict_items iterator into regular
    tuples for simple typing.
    """
    return [(ref, i) for ref, i in collections.Counter(references).items()]

    # reference_count = []
    # for ref in reference_list:
    #     found = False
    #     for key, (counted_ref, count) in enumerate(reference_count):
    #         if ref == counted_ref and not found:
    #             reference_count[key] = (counted_ref, count + 1)
    #             found = True
    #     if not found:
    #         reference_count.append((ref, 1))
    # return reference_count
