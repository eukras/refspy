"""A facade for all major interface functions.

See `refspy.refspy()` for a useful helper function.
"""

import re
from typing import Dict, Generator, List, Tuple

from pydantic import TypeAdapter
from refspy.book import Book
from refspy.format import (
    ABBREV_BOOK_FORMAT,
    ABBREV_NAME_FORMAT,
    BOOK_FORMAT,
    NAME_FORMAT,
    NUMBER_FORMAT,
)
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
from refspy.range import combine, merge, range
from refspy.reference import (
    Reference,
    book_reference,
    chapter_reference,
    reference,
    verse_reference,
)
from refspy.utils import pluralize, url_param, url_escape
from refspy.verse import Number, verse


"""
References can always be formatted with Manager.template(ref). If no
pattern argument is supplied, the default short format will be used, e.g.
'Rom 12:1-7'. or ref.abbrev_name()
"""
DEFAULT_TEMPLATE_PATTERN = "{ABBREV_NAME}"


class Manager:
    """
    The manager object integrates the main library features into a single
    convenient facade.
    """

    def __init__(
        self,
        libraries: List[Library],
        language: Language,
        include_two_letter_aliases=True,
    ):
        """
        Construct a new Manager object.

        Args:
            libraries: A list of libraries like NT, OT.
            language: A language object like ENGLISH.
            include_two_letter_aliases: Whether to allow `len(alias) == 2`
                (default: True)
        """
        self.libraries: Dict[Number, Library] = index_libraries(libraries)
        """A lookup dictionary for Libraries by library.id """

        self.books: Dict[Tuple[Number, Number], Book] = index_books(libraries)
        """A lookup dictionary for Books by (library.id, book.id)"""

        self.book_aliases: Dict[str, Tuple[Number, Number]] = index_book_aliases(
            libraries, include_two_letter_aliases=include_two_letter_aliases
        )
        """A lookup dictionary for (library.id, book.id) by book alias strings."""

        self.language: Language = language
        """Language-specific program data."""

        self.matcher: Matcher = Matcher(self.books, self.book_aliases, self.language)
        """Delegate reference matching tasks."""

        self.formatter: Formatter = Formatter(self.books, self.book_aliases)
        """Delegate formatting tasks."""

        self.navigator: Navigator = Navigator(self.books, self.book_aliases)
        """Delegate navigation tasks."""

    # -----------------------------------
    # Index and summary functions
    # -----------------------------------

    def make_index_references(self, references: List[Reference]) -> List[Reference]:
        """Return a sorted list of References; no combining or simplifying."""
        index = []
        collation = self.collate(
            sorted([ref for ref in references if ref and not ref.is_book()])
        )
        for _, book_collation in collation:
            for _, reference_list in book_collation:
                sorted_ref = self.sort_references(reference_list)
                index.append(sorted_ref)
        return index

    def make_index(
        self,
        references: List[Reference],
        pattern: str | None = None,
    ) -> str | None:
        """
        Return a one-line list of references in order of appearance.

        Args:
            pattern: a formatting string suitable for links, see
                `refspy.manager.Manager.template()`.

        Note:
            If no template pattern is provided, reference formatting
            will default to `refspy.manager.Manager.abbrev_name()`
        """
        if indexes := self.make_index_references(references):
            return ", ".join([self.template(ref, pattern) for ref in indexes])
        else:
            return None

    def make_summary_references(self, references: List[Reference]) -> List[Reference]:
        """Return a sorted, combined, simplified list of References."""
        collation = self.collate(
            sorted([ref for ref in references if ref and not ref.is_book()])
        )
        summary = []
        for _, book_collation in collation:
            for _, reference_list in book_collation:
                compact_ref = self.combine_references(reference_list)
                summary.append(compact_ref)
        return summary

    def make_summary(
        self, references: List[Reference], pattern: str | None = None
    ) -> str | None:
        """
        Return a string showing a sorted, combined, list of References.

        Args:
            pattern: a formatting string suitable for links, see
                `refspy.manager.Manager.template()`.

        Note:
            If no template pattern is provided, reference formatting
            will default to `refspy.manager.Manager.abbrev_name()`.

        Args:
            max_chapters: The maximum number of chapter hotspots to return.
            min_references: The minimal references per chapter that qualifies as a hotspot.
        """
        if summaries := self.make_summary_references(references):
            return ", ".join([self.template(ref, pattern) for ref in summaries])
        else:
            return None

    def make_hotspot_tuples(
        self,
        references: List[Reference],
        max_chapters: int = 7,
        min_references: int = 2,
    ) -> List[Tuple[Reference, int]]:
        """
        Find the most referenced chapters in a set of references.

        Args:
            max_chapters: The maximum number of chapter hotspots to return.
            min_references: The minimal references per chapter that qualifies as a hotspot.

        Return:
            a list of tuples of (chapter reference, count) in descending frequency
        """
        if not references:
            return []
        totals = dict()
        for _ in self.sort_references(references).ranges:
            for tuple in [
                (_.start.library, _.start.book, _.start.chapter),
                (_.end.library, _.end.book, _.end.chapter),
            ]:
                if tuple in totals:
                    totals[tuple] += 1
                else:
                    totals[tuple] = 1
        hotspots = [
            (chapter_reference(*tuple), int(total / 2))
            for tuple, total in totals.items()
            if total / 2 >= min_references
        ]
        hotspots_desc = sorted(hotspots, key=lambda item: item[1], reverse=True)
        return hotspots_desc[:max_chapters]

    def make_hotspot_references(
        self,
        references: List[Reference],
        max_chapters: int = 7,
        min_references: int = 2,
    ) -> List[Reference]:
        """
        Return chapter references in descending order of frequency.

        Args:
            max_chapters: The maximum number of chapter hotspots to return.
            min_references: The minimal references per chapter that qualifies as a hotspot.
        """
        tuples = self.make_hotspot_tuples(references, max_chapters, min_references)
        return [ref for ref, _ in tuples]

    def make_hotspots(
        self,
        references: List[Reference],
        max_chapters: int = 7,
        min_references: int = 2,
        pattern: str | None = None,
    ) -> str | None:
        """
        Return chapter references in descending order of frequency, as a text
        string, e.g. "Rom 3, 1 Cor 6", or None.

        Args:
            max_chapters: The maximum number of chapter hotspots to return.
            min_references: The minimal references per chapter that qualifies as a hotspot.
            pattern: an optional template pattern for formatting references
        """
        if refs := self.make_hotspot_references(
            references, max_chapters=max_chapters, min_references=min_references
        ):
            return ", ".join([self.template(ref, pattern) for ref in refs])
        else:
            return None

    # -----------------------------------
    # Merging functions
    # -----------------------------------

    def sort_references(self, references: List[Reference]) -> Reference:
        """For a list of references, make a single reference containing their sorted ranges."""

        ranges = []
        for ref in references:
            for rng in ref.ranges:
                ranges.append(rng)
        return reference(*sorted(ranges))

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
        Generate tuples of (match_str, reference) for provided text.manager

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
        """Return the first matching reference in the given text.

        Book names and malformed references are not matched.
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

    def get_book(self, ref: Reference) -> Book:
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

    def name(self, ref: Reference) -> str:
        """Format a reference."""
        return self.formatter.format(ref, NAME_FORMAT)

    def book(self, ref: Reference) -> str:
        """Format a reference using only the book part of its name."""
        return self.formatter.format(ref, BOOK_FORMAT)

    def abbrev_name(self, ref: Reference) -> str:
        """Format an abbreviated reference."""
        return self.formatter.format(ref, ABBREV_NAME_FORMAT)

    def abbrev_book(self, ref: Reference) -> str:
        """Format an abbreviated reference using only the book part of its name."""
        return self.formatter.format(ref, ABBREV_BOOK_FORMAT)

    def numbers(self, ref: Reference) -> str:
        """Format a reference using only the number part of its name.

        The number part is the same for full names and abreviated names.
        """
        return self.formatter.format(ref, NUMBER_FORMAT)

    # -----------------------------------
    # Template formatting functions
    # -----------------------------------

    def template(self, reference: Reference | None, pattern: str | None = None) -> str:
        """
        Substitute formatting values in a string:

            * `{NAME}` -> "1 Corinthians 2:3–4"
            * `{BOOK}` -> "1 Corinthians"
            * `{NUMBERS}` -> "2:3–4"
            * `{ABBREV_NAME}` -> "1 Cor 2:3–4"
            * `{ABBREV_BOOK}` -> "1 Cor"
            * `{ABBREV_NUMBERS}` -> "2:3–4"
            * `{ESC_NAME}` -> "1%20Corinthians%202%3A3-4"
            * `{ESC_BOOK}` -> "1%20Corinthians"
            * `{ESC_NUMBERS}` -> "2%3A3-4"
            * `{ESC_ABBREV_NAME}` -> "1%20Cor%202%3A3-4"
            * `{ESC_ABBREV_BOOK}` -> "1%20Cor"
            * `{ESC_ABBREV_NUMBERS}` -> "2%3A3-4"
            * `{PARAM_NAME}`-> "1cor+2.3-4"
            * `{PARAM_BOOK}` -> "1cor"
            * `{PARAM_NUMBERS}` -> "2.3-4"

        For efficiency, we calculate only the values required by the template
        string.
        """
        if reference is None:
            return ""

        out = pattern if pattern else DEFAULT_TEMPLATE_PATTERN

        regexp = re.compile(r"\{[A-Z_]+\}")
        matches = regexp.findall(out)
        numbers = self.numbers(reference)
        for _ in matches:
            if _ == "{NAME}":
                out = out.replace("{NAME}", self.name(reference))
            elif _ == "{BOOK}":
                out = out.replace("{BOOK}", self.book(reference))
            elif _ == "{NUMBERS}":
                out = out.replace("{NUMBERS}", numbers)
            elif _ == "{ASCII_NUMBERS}":
                out = out.replace("{ASCII_NUMBERS}", numbers.replace("–", "-"))
            elif _ == "{ABBREV_NAME}":
                out = out.replace("{ABBREV_NAME}", self.abbrev_name(reference))
            elif _ == "{ABBREV_BOOK}":
                out = out.replace("{ABBREV_BOOK}", self.abbrev_name(reference))
            elif _ == "{ESC_NAME}":
                out = out.replace("{ESC_NAME}", url_escape(self.name(reference)))
            elif _ == "{ESC_BOOK}":
                out = out.replace("{ESC_BOOK}", url_escape(self.book(reference)))
            elif _ == "{ESC_NUMBERS}":
                out = out.replace("{ESC_NUMBERS}", url_escape(numbers))
            elif _ == "{ESC_ASCII_NUMBERS}":
                out = out.replace(
                    "{ESC_ASCII_NUMBERS}",
                    url_escape(numbers.replace("–", "-")),
                )
            elif _ == "{ESC_ABBREV_NAME}":
                out = out.replace(
                    "{ESC_ABBREV_NAME}", url_escape(self.abbrev_name(reference))
                )
            elif _ == "{ESC_ABBREV_BOOK}":
                out = out.replace(
                    "{ESC_ABBREV_BOOK}",
                    url_escape(self.abbrev_book(reference)),
                )
            elif _ == "{PARAM_NAME}":
                out = out.replace("{PARAM_NAME}", url_param(self.name(reference)))
            elif _ == "{PARAM_BOOK}":
                out = out.replace("{PARAM_BOOK}", url_param(numbers))
            elif _ == "{PARAM_NUMBERS}":
                out = out.replace("{PARAM_NUMBERS}", url_param(numbers))
        return out
