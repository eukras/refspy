from typing import Dict, Tuple

from refspy.book import Book
from refspy.range import range
from refspy.reference import Reference, reference
from refspy.verse import Number, verse


class Navigator:
    def __init__(
        self,
        books: Dict[Tuple[Number, Number], Book],
        book_aliases: Dict[str, Tuple[Number, Number]],
    ) -> None:
        self.books = books
        self.book_aliases = book_aliases

    def prev_chapter(self, ref: Reference) -> Reference | None:
        v1 = ref.ranges[0].start
        if v1.chapter > 1:
            return reference(
                [
                    range(
                        verse(v1.library, v1.book, v1.chapter - 1, 1),
                        verse(v1.library, v1.book, v1.chapter - 1, 999),
                    )
                ]
            )
        else:
            if (v1.library, v1.book - 1) not in self.books:
                return None
            prev_book = self.books[v1.library, v1.book - 1]
            end_chapter = prev_book.chapters
            return reference(
                [
                    range(
                        verse(v1.library, prev_book.id, end_chapter, 1),
                        verse(v1.library, prev_book.id, end_chapter, 999),
                    )
                ]
            )

    def next_chapter(self, ref: Reference) -> Reference | None:
        v1 = ref.ranges[0].start
        end_chapter = self.books[v1.library, v1.book].chapters
        if v1.chapter < end_chapter:
            return reference(
                [
                    range(
                        verse(v1.library, v1.book, v1.chapter + 1, 1),
                        verse(v1.library, v1.book, v1.chapter + 1, 999),
                    )
                ]
            )
        else:
            if (v1.library, v1.book + 1) not in self.books:
                return None
            next_book = self.books[v1.library, v1.book + 1]
            return reference(
                [
                    range(
                        verse(v1.library, next_book.id, 1, 1),
                        verse(v1.library, next_book.id, 1, 999),
                    )
                ]
            )
