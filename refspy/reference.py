"""Data object for references.

References consist of lists of ranges and are entirely numerical objects.

They can be set to sort, merge, and join references when added together.
"""

from typing import Any, List, Self

from pydantic import BaseModel, Field

from refspy.range import Range, combine, merge, range
from refspy.verse import Number, Verse, verse


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

    ranges: List[Range] = Field(min_length=1)
    """
    A reference must contain at least one `refspy.range.Range`.

    Raises:
        ValueError: If ranges is empty
    """

    def __add__(self, other: Self) -> Self:
        """Overload the addition operator to combine reference ranges into a new object.

        The most aggressive sort/merge/join settings from the two References will
        be used in the new Reference.
        """
        return self.__class__(ranges=[*self.ranges, *other.ranges])

    def __lt__(self, other: Self) -> bool:
        """
        A simple implementation of '<' allows sorting and min/max.

        Note:
            Consider sorting first verse ASC and last verse DESC.
        """
        return self.ranges[0].start < other.ranges[0].start

    def equals(self, other: Self) -> bool:
        """
        Reference equality means that two references have identical ranges.

        Note:
            Consider comparing after any differences in sort/merge/join have
            been reconciled.

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
        return self.__class__(ranges=merge(self.ranges))

    def combine(self) -> Self:
        """Return a combined reference.

        A combined reference is sorted, merged, and has any adjacent ranges combined.
        """
        return self.__class__(ranges=combine(self.ranges))


def reference(*args: Range, **kwargs: Any) -> Reference:
    """
    Construct a Reference object from `refspy.range.Range` arguments.

    Example:
        ```
        ref = reference(
            range(verse(1, 2, 3, 3), verse(1, 2, 3, 4)),
            range(verse(1, 2, 3, 6), verse(1, 2, 3, 7))
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
        range(
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
        range(
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
        range(
            verse(library_id, book_id, chapter_id, verse_id),
            verse(library_id, book_id, chapter_id, verse_end_id or verse_id),
        )
    )
