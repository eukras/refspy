from typing import Dict, Tuple

from refspy.format import Format
from refspy.range import Range
from refspy.reference import Reference
from refspy.types.book import Book
from refspy.utils import string_together
from refspy.verse import Number, Verse


class Formatter:
    """
    Format an arbitrary reference, using supplied formatting options.
    """

    def __init__(
        self,
        books: Dict[Tuple[Number, Number], Book],
        book_aliases: Dict[str, Tuple[Number, Number]],
    ) -> None:
        self.books = books
        self.book_aliases = book_aliases

    def format(
        self, reference: Reference, options: Format, if_invalid="[INVALID]"
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
                out += self.make_divider(next_range, last_verse, options)
            if next_range.is_book_range():
                out += self.make_book_range(next_range, last_verse, options)
            elif next_range.is_inter_book_range():
                out += self.make_inter_book_range(next_range, last_verse, options)
            elif next_range.is_book():
                out += self.make_book(next_range, last_verse, options)
            elif next_range.is_chapter_range():
                out += self.make_chapter_range(next_range, last_verse, options)
            elif next_range.is_inter_chapter_range():
                out += self.make_inter_chapter_range(next_range, last_verse, options)
            elif next_range.is_chapter():
                out += self.make_chapter(next_range, last_verse, options)
            elif next_range.is_verse_range():
                out += self.make_verse_range(next_range, last_verse, options)
            elif next_range.is_verse():
                out += self.make_verse(next_range, last_verse, options)
            else:
                out += if_invalid
            last_verse = next_range.start
        return out

    def make_divider(self, _: Range, last: Verse | None, options: Format) -> str:
        if last is None:
            return ""
        if any(
            [
                _.start.library != last.library,
                _.start.book != last.book,
                _.start.chapter != last.chapter,
            ]
        ):
            return options.semicolon
        else:
            return options.comma

    def make_book_range(self, _: Range, last: Verse | None, options: Format) -> str:
        start_book = self.books[_.start.library, _.start.book]
        start_book_name = getattr(start_book, options.property or "", "")
        end_book = self.books[_.end.library, _.end.book]
        end_book_name = getattr(end_book, options.property or "", "")
        return string_together(start_book_name, options.dash, end_book_name)

    def make_inter_book_range(
        self, _: Range, last: Verse | None, options: Format
    ) -> str:
        start_book = self.books[_.start.library, _.start.book]
        start_book_name = getattr(start_book, options.property or "", "")
        if _.start.verse == 1 and _.end.verse == 999:
            start_number = string_together(_.start.chapter)
        else:
            start_number = string_together(
                (_.start.chapter, options.colon, _.start.verse)
            )
        end_book = self.books[_.end.library, _.end.book]
        end_book_name = getattr(end_book, options.property or "", "")
        if _.end.verse == 1 and _.end.verse == 999:
            end_number = string_together(_.end.chapter)
        else:
            end_number = string_together(_.end.chapter, options.colon, _.end.verse)

        return options.space.join(
            [start_book_name, start_number, options.dash, end_book_name, end_number]
        )

    def make_book(self, _: Range, last: Verse | None, options: Format) -> str:
        start_book = self.books[_.start.library, _.start.book]
        start_book_name = getattr(start_book, options.property or "", "")
        return start_book_name

    def book_name_if_required(
        self, _: Range, last: Verse | None, options: Format
    ) -> str:
        book_name = ""
        if last is None:
            book_name = self.make_book(_, last, options)
        elif _.start.library != last.library or _.start.book != last.book:
            book_name = self.make_book(_, last, options)
        if book_name != "":
            return book_name + options.space
        return ""

    def make_chapter_range(self, _: Range, last: Verse | None, options: Format) -> str:
        return string_together(
            self.book_name_if_required(_, last, options),
            _.start.chapter,
            options.dash,
            _.end.chapter,
        )

    def make_inter_chapter_range(
        self, _: Range, last: Verse | None, options: Format
    ) -> str:
        return string_together(
            self.book_name_if_required(_, last, options),
            _.start.chapter,
            options.colon,
            _.start.verse,
            options.dash,
            _.end.chapter,
            options.colon,
            _.end.verse,
        )

    def make_chapter(self, _: Range, last: Verse | None, options: Format) -> str:
        return string_together(
            self.book_name_if_required(_, last, options), _.start.chapter
        )

    def chapter_number_if_required(
        self, _: Range, last: Verse | None, options: Format
    ) -> str:
        book = self.books[_.start.library, _.start.book]
        if last is None:
            if book.depth == 2:
                return string_together(_.start.chapter, options.colon)
        elif (
            _.start.library != last.library
            or _.start.book != last.book
            or _.start.chapter != last.chapter
        ):
            if book.depth == 2:
                return string_together(_.start.chapter, options.colon)
        return ""

    def make_verse_range(self, _: Range, last: Verse | None, options: Format) -> str:
        return string_together(
            self.book_name_if_required(_, last, options),
            self.chapter_number_if_required(_, last, options),
            _.start.verse,
            options.dash,
            _.end.verse,
        )

    def make_verse(self, _: Range, last: Verse | None, options: Format) -> str:
        return string_together(
            self.book_name_if_required(_, last, options),
            self.chapter_number_if_required(_, last, options),
            _.start.verse,
        )
