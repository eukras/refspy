from typing import Dict, Generator, List, Tuple
from weakref import ref

from refspy.format import ABBREV_FORMAT, CODE_FORMAT, NAME_FORMAT, NUMBER_FORMAT
from refspy.formatter import Formatter
from refspy.indexes import (
    index_book_aliases,
    index_books,
    index_libraries,
    index_library_aliases,
)
from refspy.language import Language
from refspy.matcher import Matcher
from refspy.navigator import Navigator
from refspy.range import range
from refspy.reference import (
    Reference,
    book_reference,
    chapter_reference,
    is_book_reference,
    reference,
    verse_reference,
)
from refspy.types.book import Book
from refspy.types.library import Library
from refspy.verse import Number, verse


class Manager:
    """
    The manager object integrates the main library features into a single
    convenient facade.
    """

    def __init__(self, libraries: List[Library], language: Language):
        self.libraries = index_libraries(libraries)
        self.books = index_books(libraries)
        self.library_aliases = index_library_aliases(libraries)
        self.book_aliases = index_book_aliases(libraries)
        self.language = language
        self.matcher = Matcher(self.books, self.book_aliases, self.language)
        self.formatter = Formatter(self.books, self.book_aliases)
        self.navigator = Navigator(self.books, self.book_aliases)

    # -----------------------------------
    # Merge functions
    # -----------------------------------

    def merge(self, references: List[Reference]) -> Reference:
        if references:
            if len(references) == 1:
                return references[0]
            else:
                sum = references[0]
                for ref in references[1:]:
                    sum += ref
                return sum
        else:
            raise ValueError("Reference list for merge must not be empty")

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
        Because we match book names and reference numbers separately, finding
        the first reference in "Book 1:2" means "1:2" to refspy. So we return
        the first reference with verse numbers if there is one, otherwise just
        the first reference.

        - Book -> Return first match
          ^^^^
        - Book 2 -> Return first match
          ^^^^^^
        - Book 2:2 -> Return second match
          ^^^^ ^^^
        """
        generator = self.matcher.generate_references(text)
        return next(generator, (None, None))

    def find_references(
        self, text: str, include_books=False
    ) -> List[Tuple[str, Reference]]:
        generator = self.matcher.generate_references(text, include_books)
        return list(generator)

    def generate_references(
        self, text: str, include_books: bool = False
    ) -> Generator[Tuple[str, Reference], None, None]:
        yield from self.matcher.generate_references(text, include_books)

    # -----------------------------------
    # Reference creator functions
    # -----------------------------------

    def bcv(self, alias: str, c=None, v=None, v_end=None) -> Reference:
        if alias not in self.book_aliases:
            raise ValueError(f'Book alias "{alias}" not found.')
        library_id, book_id = self.book_aliases[alias]
        if c is None:
            return book_reference(library_id, book_id)
        if v is None:
            return chapter_reference(library_id, book_id, c)
        if v_end is None:
            return verse_reference(library_id, book_id, c, v)
        return reference(
            [
                range(
                    verse(library_id, book_id, c, v),
                    verse(library_id, book_id, c, v_end),
                )
            ]
        )

    def bcr(
        self, alias: str, c: Number, v_ranges: List[Number | Tuple[Number, Number]]
    ) -> Reference:
        if alias not in self.book_aliases:
            raise ValueError(f'Book alias "{alias}" not found.')
        library_id, book_id = self.book_aliases[alias]
        ranges = []
        for val in v_ranges:
            print("V_RANGES", v_ranges)
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
        return reference(ranges)

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
        return self.navigator.next_chapter(ref)

    def prev_chapter(self, ref: Reference) -> Reference | None:
        return self.navigator.prev_chapter(ref)

    # -----------------------------------
    # Manipulation functions
    # -----------------------------------

    def book(self, ref: Reference) -> Book:
        v1 = ref.ranges[0].start
        return self.books[v1.library, v1.book]

    def book_reference(self, ref: Reference) -> Reference:
        v1 = ref.ranges[0].start
        return reference(
            [
                range(
                    verse(v1.library, v1.book, 1, 1),
                    verse(v1.library, v1.book, 999, 999),
                )
            ]
        )

    def chapter_reference(self, ref: Reference) -> Reference:
        v1 = ref.ranges[0].start
        return reference(
            [
                range(
                    verse(v1.library, v1.book, v1.chapter, 1),
                    verse(v1.library, v1.book, v1.chapter, 999),
                )
            ]
        )

    # -----------------------------------
    # Formatting functions
    # -----------------------------------

    def numbers(self, ref: Reference) -> str:
        return self.formatter.format(ref, NUMBER_FORMAT)

    def name(self, ref: Reference) -> str:
        return self.formatter.format(ref, NAME_FORMAT)

    def abbrev(self, ref: Reference) -> str:
        return self.formatter.format(ref, ABBREV_FORMAT)

    def code(self, ref: Reference) -> str:
        return self.formatter.format(ref, CODE_FORMAT)
