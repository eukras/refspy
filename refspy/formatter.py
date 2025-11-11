"""Format Reference objects using Format objects."""

from refspy.models.language import Language
from refspy.languages.english import ENGLISH

from refspy.models.book import Book
from refspy.models.format import Format
from refspy.models.range import Range
from refspy.models.reference import Reference
from refspy.models.verse import Verse

from refspy.types.number import Number

from refspy.constants import EM_DASH, SPACE
from refspy.utils import string_together


class Formatter:
    """
    Format an arbitrary reference, using supplied formatting options.

    References contain lists of `refspy.range.Range` objects. These can span
    arbitrary verses across multiple libraries, and can be arranged in any
    order. The formatter formats the individual ranges correctly and also
    indicates any changes between books and chapters.
    """

    def __init__(
        self,
        books: dict[tuple[Number, Number], Book],
        book_aliases: dict[str, tuple[Number, Number]],
    ) -> None:
        self.books = books
        self.book_aliases = book_aliases

    def format(
        self,
        reference: Reference,
        format: Format,
        if_invalid="[INVALID]",
    ) -> str:
        """
        Compare each range with the one before and decide whether we need to add
        the book name or chapter number to each range. This will work for
        sorted and unsorted references, but sorted references will be more compact.
        """
        out = ""
        last_verse = None
        for next_range in reference.ranges:
            if len(out) > 0:
                out += self.make_divider(next_range, last_verse, format)
            if next_range.is_book_range():
                out += self.make_book_range(next_range, format)
            elif next_range.is_inter_book_range():
                out += self.make_inter_book_range(next_range, format)
            elif next_range.is_book():
                out += self.make_book(next_range, format)
            elif next_range.is_chapter_range():
                out += self.make_chapter_range(next_range, last_verse, format)
            elif next_range.is_inter_chapter_range():
                out += self.make_inter_chapter_range(next_range, last_verse, format)
            elif next_range.is_chapter():
                out += self.make_chapter(next_range, last_verse, format)
            elif next_range.is_verse_range():
                out += self.make_verse_range(next_range, last_verse, format)
            elif next_range.is_verse():
                out += self.make_verse(next_range, last_verse, format)
            else:
                out += if_invalid
            last_verse = next_range.start
        return out

    def link_format(self) -> Format:
        """
        Follow English format conventions because they are more widely
        used by linkable resources.
        """
        return Format(
            colon=ENGLISH.syntax.format_colon,
            comma=ENGLISH.syntax.format_comma,
            dash=ENGLISH.syntax.format_dash,
            semicolon=ENGLISH.syntax.format_semicolon,
            book_only=False,
            number_only=False,
            property="abbrev",
        )

    def name_format(self, language: Language) -> Format:
        return Format(
            colon=language.syntax.format_colon,
            comma=language.syntax.format_comma,
            dash=language.syntax.format_dash,
            semicolon=language.syntax.format_semicolon,
            book_only=False,
            number_only=False,
            property="name",
        )

    def book_format(self, language: Language) -> Format:
        return Format(
            colon=language.syntax.format_colon,
            comma=language.syntax.format_comma,
            dash=language.syntax.format_dash,
            semicolon=language.syntax.format_semicolon,
            book_only=True,
            number_only=False,
            property="name",
        )

    def number_format(self, language: Language) -> Format:
        return Format(
            colon=language.syntax.format_colon,
            comma=language.syntax.format_comma,
            dash=language.syntax.format_dash,
            semicolon=language.syntax.format_semicolon,
            book_only=False,
            number_only=True,
            property=None,
        )

    def abbrev_name_format(self, language: Language) -> Format:
        return Format(
            colon=language.syntax.format_colon,
            comma=language.syntax.format_comma,
            dash=language.syntax.format_dash,
            semicolon=language.syntax.format_semicolon,
            book_only=False,
            number_only=False,
            property="abbrev",
        )

    def abbrev_book_format(self, language: Language) -> Format:
        return Format(
            colon=language.syntax.format_colon,
            comma=language.syntax.format_comma,
            dash=language.syntax.format_dash,
            semicolon=language.syntax.format_semicolon,
            book_only=True,
            number_only=False,
            property="abbrev",
        )

    def abbrev_number_format(self, language: Language) -> Format:
        return Format(
            colon=language.syntax.format_colon,
            comma=language.syntax.format_comma,
            dash=language.syntax.format_dash,
            semicolon=language.syntax.format_semicolon,
            book_only=False,
            number_only=True,
            property="abbrev",
        )

    def make_divider(self, _: Range, last: Verse | None, format: Format) -> str:
        """Provide a separator between ranges.

        This will be a semicolon or comma.
        """
        if last is None:
            return ""
        if any(
            [
                _.start.library != last.library,
                _.start.book != last.book,
                _.start.chapter != last.chapter,
            ]
        ):
            return format.semicolon
        else:
            return format.comma

    def make_book_range(self, _: Range, format: Format) -> str:
        """Format a range between two whole books.

        See `refspy.range.Range.is_book_range` .

        Example:
            `Matthew-John`
        """
        start_book = self.books[_.start.library, _.start.book]
        start_book_name = getattr(start_book, format.property or "", "")
        end_book = self.books[_.end.library, _.end.book]
        end_book_name = getattr(end_book, format.property or "", "")
        return string_together(start_book_name, EM_DASH, end_book_name)

    def make_inter_book_range(self, _: Range, format: Format) -> str:
        """Format a range that spans multiple books (or libraries).

        See `refspy.range.Range.is_inter_book_range` .

        Example:
            `Matt 15:15-John 15:15`
        """
        start_book = self.books[_.start.library, _.start.book]
        start_book_name = getattr(start_book, format.property or "", "")
        if _.start.verse == 1 and _.end.verse == 999:
            start_number = string_together(_.start.chapter)
        else:
            start_number = string_together(_.start.chapter, format.colon, _.start.verse)
        end_book = self.books[_.end.library, _.end.book]
        end_book_name = getattr(end_book, format.property or "", "")
        if _.start.verse == 1 and _.end.verse == 999:
            end_number = string_together(_.end.chapter)
        else:
            end_number = string_together(_.end.chapter, format.colon, _.end.verse)

        return SPACE.join(
            [start_book_name, start_number, format.dash, end_book_name, end_number]
        )

    def make_book(self, _: Range, format: Format) -> str:
        """Format a range that spans multiple books (or libraries).

        See `refspy.range.Range.is_book` .

        Example:
            `Matthew`
        """
        start_book = self.books[_.start.library, _.start.book]
        start_book_name = getattr(start_book, format.property or "", "")
        return start_book_name

    def book_name_if_required(
        self, _: Range, last: Verse | None, format: Format
    ) -> str:
        """Format the book name (and a space) if the next range is in a
        different book.

        Example:
            `Matthew `
        """
        if format.number_only:
            return ""
        book_name = ""
        if last is None:
            book_name = self.make_book(_, format)
        elif _.start.library != last.library or _.start.book != last.book:
            book_name = self.make_book(_, format)
        if book_name != "":
            if format.book_only:
                return book_name
            else:
                return book_name + SPACE
        return ""

    def make_chapter_range(self, _: Range, last: Verse | None, format: Format) -> str:
        """Format a range that spans whole chapters.

        Add the book name, if required.

        See `refspy.range.Range.is_chapter_range` .

        Example:
            `1-2` or `Matthew 1-2`
        """
        return string_together(
            self.book_name_if_required(_, last, format),
            _.start.chapter,
            format.dash,
            _.end.chapter,
        )

    def make_inter_chapter_range(
        self, _: Range, last: Verse | None, format: Format
    ) -> str:
        """Format a range that spans different chapters.

        Add the book name, if required.

        See `refspy.range.Range.is_inter_chapter_range` .

        Example:
            `1:1-2:2` or `Matthew 1:1-2:2`
        """
        return string_together(
            self.book_name_if_required(_, last, format),
            _.start.chapter,
            format.colon,
            _.start.verse,
            format.dash,
            _.end.chapter,
            format.colon,
            _.end.verse,
        )

    def make_chapter(self, _: Range, last: Verse | None, format: Format) -> str:
        """Format a range that spans different chapters.

        Add the book name, if required.

        See `refspy.range.Range.is_chapter`.

        Example:
            `1` or `Matthew 1`
        """
        return string_together(
            self.book_name_if_required(_, last, format), _.start.chapter
        )

    def chapter_number_if_required(
        self, _: Range, last: Verse | None, format: Format
    ) -> str:
        """Format the chapter number and colon if the next range is in a
        different book.

        Example:
            `1:`
        """
        if format.book_only:
            return ""
        book = self.books[_.start.library, _.start.book]
        if last is None:
            if book.chapters > 1:
                return string_together(_.start.chapter, format.colon)
        elif (
            _.start.library != last.library
            or _.start.book != last.book
            or _.start.chapter != last.chapter
        ):
            if book.chapters > 1:
                return string_together(_.start.chapter, format.colon)
        return ""

    def make_verse_range(self, _: Range, last: Verse | None, format: Format) -> str:
        """Format a range of different verses within a single chapter.

        Add the chapter number and book name, if required.

        See `refspy.range.Range.is_verse_range` .

        Example:
            `2-3` or `1:2-3` or `Matthew 1:2-3`

        Note:
            We abbreviate the second number if possible. See `abbreviate_range()`.
        """
        if format.book_only:
            return ""
        return string_together(
            self.book_name_if_required(_, last, format),
            self.chapter_number_if_required(_, last, format),
            "" if format.book_only else _.start.verse,
            "" if format.book_only else format.dash,
            "" if format.book_only else _.end.verse,
        )

    def make_verse(self, _: Range, last: Verse | None, format: Format) -> str:
        """Format a single verse number.

        Add the chapter number and book name, if required.

        See `refspy.range.Range.is_verse` .

        Example:
            `2` or `1:2` or `Matthew 1:2`
        """
        return string_together(
            self.book_name_if_required(_, last, format),
            self.chapter_number_if_required(_, last, format),
            "" if format.book_only else _.start.verse,
        )
