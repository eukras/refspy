from refspy.types.book import Book
from refspy.library import Library

FIRST_BOOK = Book(
    id=1,
    name="First Book",
    abbrev="First",
    code="first",
    depth=2,
    aliases=["primo"],
    chapters=10,
)

BIG_BOOK = Book(
    id=2,
    name="Big Book",
    abbrev="Big",
    code="big",
    depth=2,
    aliases=["large"],
    chapters=50,
)

SMALL_BOOK = Book(
    id=3,
    name="Small Book",
    abbrev="Small",
    code="small",
    depth=1,
    aliases=["tiny"],
    chapters=1,
)

BOOK_2 = Book(
    id=4,
    name="2 Book",
    abbrev="2 Bk",
    code="2bk",
    depth=2,
    aliases=[],
    chapters=10,
)

LAST_BOOK = Book(
    id=5,
    name="Last Book",
    abbrev="Last",
    code="last",
    depth=2,
    aliases=["finale"],
    chapters=10,
)

TEST_LIBRARY = Library(
    id=1,
    name="Library",
    abbrev="Lib",
    code="lib",
    books=[FIRST_BOOK, BIG_BOOK, SMALL_BOOK, BOOK_2, LAST_BOOK],
)

BOOK_3 = Book(
    id=1,
    name="3 Book",
    abbrev="3 Bk",
    code="3bk",
    depth=2,
    aliases=[],
    chapters=10,
)

TEST_LIBRARY_2 = Library(
    id=2,
    name="2 Library",
    abbrev="2 Lib",
    code="2lib",
    books=[BOOK_3],
)
