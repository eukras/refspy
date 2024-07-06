"""A facade for all major interface functions.

See `refspy.refspy()` for a useful helper function.
"""

from typing import Dict, Generator, List, Optional, Tuple

from pydantic import TypeAdapter

from refspy.book import Book
from refspy.format import ABBREV_FORMAT, NAME_FORMAT, NUMBER_FORMAT
from refspy.formatter import Formatter
from refspy.indexers import (
    index_book_aliases,
    index_books,
    index_libraries,
)
from refspy.language import Language
from refspy.library import Library
from refspy.matcher import Matcher
from refspy.navigator import Navigator
from refspy.range import combine, merge, range, sort
from refspy.reference import (
    Reference,
    book_reference,
    chapter_reference,
    reference,
    verse_reference,
)
from refspy.utils import url_param
from refspy.verse import Number, verse


class Manager:
    """
    The manager object integrates the main library features into a single
    convenient facade.
    """

    def __init__(self, libraries: List[Library], language: Language):
        self.libraries: Dict[Number, Library] = index_libraries(libraries)
        """A lookup dictionary for Libraries by library.id """

        self.books: Dict[Tuple[Number, Number], Book] = index_books(libraries)
        """A lookup dictionary for Books by (library.id, book.id)"""

        self.book_aliases: Dict[str, Tuple[Number, Number]] = index_book_aliases(
            libraries
        )
        """A lookup dictionary for (library.id, book.id) by book alias strings."""

        self.language: Language = language
        self.matcher: Matcher = Matcher(self.books, self.book_aliases, self.language)
        self.formatter: Formatter = Formatter(self.books, self.book_aliases)
        self.navigator: Navigator = Navigator(self.books, self.book_aliases)

    # -----------------------------------
    # Merging functions
    # -----------------------------------

    def sort_references(self, references: List[Reference]) -> List[Reference]:
        """Sort references by their lowest range."""
        return sorted(references)

    def merge_references(self, references: List[Reference]) -> Reference:
        """For a list of references, merge their ranges into a new reference.

        Merging means combining ranges that overlap.
        """
        ranges = []
        for ref in references:
            ranges.extend(ref.ranges)
        new_ref = reference(*merge(ranges))
        return new_ref

    def combine_references(self, references: List[Reference]) -> Reference:
        """For a list of references, combine their ranges into a new reference.

        Combining means sorting ranges, merging overlaps, and joining adjacent
        records.
        """
        ranges = []
        for ref in references:
            ranges.extend(ref.ranges)
        new_ref = reference(*combine(ranges))
        return new_ref

    # -----------------------------------
    # Iteration functions
    # -----------------------------------

    def collate(
        self, references: List[Reference]
    ) -> List[Tuple[Library, List[Tuple[Book, List[Reference]]]]]:
        """
        A collation groups single-book references by library and book,
        providing Library and Book objects for iteration. Multi-book references
        are ignored.
        """
        library_list = list()
        for library_id, books_dict in self.collate_by_id(references).items():
            book_list = list()
            for book_id, references in books_dict.items():
                book_list.append(tuple([self.books[library_id, book_id], references]))
            library_list.append(tuple([self.libraries[library_id], book_list]))
        return library_list

    def collate_by_id(
        self, references: List[Reference]
    ) -> Dict[Number, Dict[Number, List[Reference]]]:
        """
        A collation groups single-book references by library and book IDs.
        Multi-book references are ignored.
        """
        collation = dict()
        for ref in [_ for _ in references if _.count_books() == 1]:
            v1 = ref.ranges[0].start
            if v1.library not in collation:
                collation[v1.library] = dict()
            if v1.book not in collation[v1.library]:
                collation[v1.library][v1.book] = list()
            collation[v1.library][v1.book].append(ref)
        return collation

    # -----------------------------------
    # Matching functions
    # -----------------------------------

    def first_reference(self, text: str) -> Tuple[str | None, Reference | None]:
        """
        Return the first tuple of (match_str, reference) found by
        `refspy.manager.Manager.generate_references()`
        """
        generator = self.matcher.generate_references(text)
        return next(generator, (None, None))

    def find_references(
        self, text: str, include_books: bool = False, include_nones: bool = False
    ) -> List[Tuple[str, Reference | None]]:
        """
        Return a list of tuples of (match_str, reference) found by
        `refspy.manager.Manager.generate_references()`
        """
        generator = self.matcher.generate_references(text, include_books, include_nones)
        return list(generator)

    def generate_references(
        self, text: str, include_books: bool = False, include_nones: bool = False
    ) -> Generator[Tuple[str, Reference | None], None, None]:
        """
        Generate tuples of (match_str, reference) for provided text.

        Task delegated to `refspy.matcher.Matcher.generate_references()`.

        Args:
            text: a string to search for references
            include_books: Whether to yield book names without reference numbers
            include_nones: Whether to yield (match_str, None) for malformed
                references.

        Yield:
            A tuple of `(match_str, reference)` for each valid reference.
        """
        yield from self.matcher.generate_references(text, include_books, include_nones)

    # -----------------------------------
    # Reference creator functions
    # -----------------------------------

    def bcv(
        self,
        alias: str,
        c: Number | None = None,
        v: Number | None = None,
        v_end: Number | None = None,
    ) -> Reference:
        """Construct a reference from a book alias and chapter/verse numbers.

        Omitting optional arguments will construct a reference to a whole book
        or chapter.

        Args:
            v_end: constructs a verse range from `v` to `v_end`.

        Raises:
            ValueError: If the book_alias is missing, or the number values are
                out of range.
        """
        if alias not in self.book_aliases:
            raise ValueError(f'Book alias "{alias}" not found.')
        library_id, book_id = self.book_aliases[alias]
        ta = TypeAdapter(Number)
        if c is None:
            return book_reference(library_id, book_id)
        if v is None:
            return chapter_reference(library_id, book_id, ta.validate_python(c))

        print("VAL 1", c, v)
        print(
            "VAL 2",
            ta.validate_python(c),
            ta.validate_python(v),
        )
        if not v_end:
            return verse_reference(
                library_id,
                book_id,
                ta.validate_python(c),
                ta.validate_python(v),
            )
        else:
            return reference(
                range(
                    verse(
                        library_id,
                        book_id,
                        ta.validate_python(c),
                        ta.validate_python(v),
                    ),
                    verse(
                        library_id,
                        book_id,
                        ta.validate_python(c),
                        ta.validate_python(v_end),
                    ),
                )
            )

    def bcr(
        self, alias: str, c: Number, v_ranges: List[Number | Tuple[Number, Number]]
    ) -> Reference:
        if alias not in self.book_aliases:
            raise ValueError(f'Book alias "{alias}" not found.')
        library_id, book_id = self.book_aliases[alias]
        ranges = []
        for val in v_ranges:
            if isinstance(val, tuple):
                v_start, v_end = val
                ranges.append(
                    range(
                        verse(library_id, book_id, c, v_start),
                        verse(library_id, book_id, c, v_end),
                    )
                )
            elif isinstance(val, int):
                v_start = v_end = val
                ranges.append(
                    range(
                        verse(library_id, book_id, c, v_start),
                        verse(library_id, book_id, c, v_end),
                    )
                )
        return reference(*ranges)

    def r(self, text: str) -> Reference | None:
        """
        Return the first matching reference in the given text, preferring
        references with chapter or verse numbers rather than whole books.
        """
        _, reference = self.first_reference(text)
        return reference

    # -----------------------------------
    # Navigation functions
    # -----------------------------------

    def next_chapter(self, ref: Reference) -> Reference | None:
        """Get the next chapter to the one containing this reference.

        This loops over the end of books using `refspy.book.Book.chapters`.
        This does not loop beyond the end of libraries.
        """
        return self.navigator.next_chapter(ref)

    def prev_chapter(self, ref: Reference) -> Reference | None:
        """Get the previous chapter to the one containing this reference.

        This loops over the end of books using `refspy.book.Book.chapters`, but
        not beyond the end of libraries.
        """
        return self.navigator.prev_chapter(ref)

    # -----------------------------------
    # Manipulation functions
    # -----------------------------------

    def book(self, ref: Reference) -> Book:
        """Get the book object for this reference's first range."""
        v1 = ref.ranges[0].start
        return self.books[v1.library, v1.book]

    def book_reference(self, ref: Reference) -> Reference:
        """Create a reference to the book containing this reference's first
        range."""
        v1 = ref.ranges[0].start
        return reference(
            range(
                verse(v1.library, v1.book, 1, 1),
                verse(v1.library, v1.book, 999, 999),
            )
        )

    def chapter_reference(self, ref: Reference) -> Reference:
        """Create a reference to the chapter containing this reference's first
        range."""
        v1 = ref.ranges[0].start
        return reference(
            range(
                verse(v1.library, v1.book, v1.chapter, 1),
                verse(v1.library, v1.book, v1.chapter, 999),
            )
        )

    # -----------------------------------
    # Formatting functions
    # -----------------------------------

    def numbers(self, ref: Reference) -> str:
        """Format a reference with only the reference number."""
        return self.formatter.format(ref, NUMBER_FORMAT)

    def name(self, ref: Reference) -> str:
        """Format a reference using its full name."""
        return self.formatter.format(ref, NAME_FORMAT)

    def abbrev(self, ref: Reference) -> str:
        """Format a reference using its abbreviated name."""
        return self.formatter.format(ref, ABBREV_FORMAT)

    def param(self, ref: Reference) -> str:
        """Format a reference using its code."""
        return url_param(self.formatter.format(ref, ABBREV_FORMAT))
