from refspy.book import Book
from refspy.library import Library

FIRST_BOOK = Book(
    id=1,
    name="Primo Booko",
    abbrev="Primo",
    aliases=[],
    chapters=10,
)

BIG_BOOK = Book(
    id=2,
    name="Big Book",
    abbrev="Big",
    aliases=["Large", "Bg"],
    chapters=50,
)

SMALL_BOOK = Book(
    id=3,
    name="Small Book",
    abbrev="Small",
    aliases=["Tiny", "Sm"],
    chapters=1,
)

BOOK_1 = Book(
    id=4,
    name="1 Book",
    abbrev="1 Bk",
    aliases=[],
    chapters=10,
)

BOOK_2 = Book(
    id=5,
    name="2 Book",
    abbrev="2 Bk",
    aliases=[],
    chapters=5,
)

BOOK_3 = Book(
    id=6,
    name="3 Book",
    abbrev="3 Bk",
    aliases=[],
    chapters=1,
)

LAST_BOOK = Book(
    id=7,
    name="Last Book",
    abbrev="Last",
    aliases=["Finale"],
    chapters=10,
)

TEST_LIBRARY = Library(
    id=1,
    name="Library",
    abbrev="Lib",
    books=[FIRST_BOOK, BIG_BOOK, SMALL_BOOK, BOOK_1, BOOK_2, BOOK_3, LAST_BOOK],
)

BOOK_4 = Book(
    id=1,
    name="4 Book",
    abbrev="4 Bk",
    aliases=[],
    chapters=5,
)

TEST_LIBRARY_2 = Library(
    id=2,
    name="2 Library",
    abbrev="2 Lib",
    books=[BOOK_4],
)
