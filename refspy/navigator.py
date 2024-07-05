"""Navigation functions for Reference objects"""

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
        """
        Note:
            Taking prev and next from references makes the most sense if ranges
            are sorted or have been collated by book and chapter.
        Example:

            Using the Navigator module on its own:

            ```
            from refspy.indexers import index_book_aliases, index_books
            from refspy.libraries.en_US import NT, OT
            from refspy.navigator import Navigator
            from refspy.reference import chapter_reference

            libraries = [OT, NT]
            navigator = Navigator(
                index_books(libraries),
                index_book_aliases(libraries)
            )
            matt_1 = chapter_reference(NT.id, 1, 1)
            matt_2 = chapter_reference(NT.id, 1, 2)
            assert navigator.next_chapter(matt_1) == matt_2
            assert navigator.prev_chapter(matt_1) is None
            ```

        Example:

            Using the navigator within the `refspy` package.

            ```
            from refspy import refspy

            __ = refspy()
            matt_1 = __.bcv('Matt', 1)
            matt_2 = __.bcv('Matt', 2)
            assert __.next_chapter(matt_1) == matt_2
            assert __.prev_chapter(matt_1) is None
            ```
        """

        self.books: Dict[Tuple[Number, Number], Book] = books
        """Lookup `refspy.book.Book` by `(library.id, book.id)`."""

        self.book_aliases: Dict[str, Tuple[Number, Number]] = book_aliases
        """Lookup `(library.id, book.id)` by book alias."""

    def prev_chapter(self, ref: Reference) -> Reference | None:
        """Find a reference to the previous chapter.

        We step into preceding books but not preceding libraries.

        Returns:
            None: If this is the first chapter of a `refspy.library.Library`.
        """
        v1 = ref.ranges[0].start
        if v1.chapter > 1:
            return reference(
                range(
                    verse(v1.library, v1.book, v1.chapter - 1, 1),
                    verse(v1.library, v1.book, v1.chapter - 1, 999),
                )
            )
        else:
            if (v1.library, v1.book - 1) not in self.books:
                return None
            prev_book = self.books[v1.library, v1.book - 1]
            end_chapter = prev_book.chapters
            return reference(
                range(
                    verse(v1.library, prev_book.id, end_chapter, 1),
                    verse(v1.library, prev_book.id, end_chapter, 999),
                )
            )

    def next_chapter(self, ref: Reference) -> Reference | None:
        """Find a reference to the next chapter.

        We step into succeeding books but not succeeding libraries.

        Returns:
            None: if this is the last chapter of a `refspy.library.Library`.
        """
        v1 = ref.ranges[0].start
        end_chapter = self.books[v1.library, v1.book].chapters
        if v1.chapter < end_chapter:
            return reference(
                range(
                    verse(v1.library, v1.book, v1.chapter + 1, 1),
                    verse(v1.library, v1.book, v1.chapter + 1, 999),
                )
            )
        else:
            if (v1.library, v1.book + 1) not in self.books:
                return None
            next_book = self.books[v1.library, v1.book + 1]
            return reference(
                range(
                    verse(v1.library, next_book.id, 1, 1),
                    verse(v1.library, next_book.id, 1, 999),
                )
            )
