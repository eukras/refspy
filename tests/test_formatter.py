from context import *

from refspy.formatter import Formatter
from refspy.format import ABBREV_NAME_FORMAT, NAME_FORMAT, NUMBER_FORMAT
from refspy.indexers import index_book_aliases, index_books
from refspy.range import range
from refspy.reference import reference
from refspy.verse import verse

from tests.data import TEST_LIBRARY, TEST_LIBRARY_2

books = index_books([TEST_LIBRARY, TEST_LIBRARY_2])
book_aliases = index_book_aliases([TEST_LIBRARY, TEST_LIBRARY_2])
fmt = Formatter(books, book_aliases)


def test_book_reference():
    ref = reference(range(verse(1, 2, 1, 1), verse(1, 2, 999, 999)))

    assert fmt.format(ref, NAME_FORMAT) == "Big Book"


def test_book_range():
    ref = reference(range(verse(1, 2, 1, 1), verse(1, 3, 999, 999)))

    assert fmt.format(ref, ABBREV_NAME_FORMAT) == "Big–Small"


def test_chapter_reference():
    ref = reference(range(verse(1, 2, 3, 1), verse(1, 2, 3, 999)))

    assert fmt.format(ref, NAME_FORMAT) == "Big Book 3"


def test_chapter_range():
    ref = reference(range(verse(1, 2, 3, 1), verse(1, 2, 4, 999)))

    assert fmt.format(ref, NAME_FORMAT) == "Big Book 3–4"


def test_single_range():
    ref = reference(range(verse(1, 2, 1, 1), verse(1, 2, 1, 2)))

    assert fmt.format(ref, NAME_FORMAT) == "Big Book 1:1–2"
    assert fmt.format(ref, ABBREV_NAME_FORMAT) == "Big 1:1–2"
    assert fmt.format(ref, NUMBER_FORMAT) == "1:1–2"


def test_multiple_verse_range():
    ref = reference(
        range(verse(1, 2, 1, 1), verse(1, 2, 1, 2)),
        range(verse(1, 2, 1, 7), verse(1, 2, 1, 9)),
    )

    assert fmt.format(ref, NAME_FORMAT) == "Big Book 1:1–2, 7–9"


def test_inter_chapter_ranges():
    ref = reference(
        range(verse(1, 2, 1, 20), verse(1, 2, 2, 10)),
        range(verse(1, 2, 3, 21), verse(1, 2, 4, 11)),
    )

    assert fmt.format(ref, NAME_FORMAT) == "Big Book 1:20–2:10; 3:21–4:11"


def test_multiple_chapter_range():
    ref = reference(
        range(verse(1, 2, 1, 1), verse(1, 2, 1, 2)),
        range(verse(1, 2, 2, 1), verse(1, 2, 2, 2)),
    )

    assert fmt.format(ref, NAME_FORMAT) == "Big Book 1:1–2; 2:1–2"


def test_multiple_book_range():
    ref = reference(
        range(verse(1, 2, 1, 1), verse(1, 2, 1, 2)),
        range(verse(1, 3, 1, 1), verse(1, 3, 1, 2)),
    )

    assert fmt.format(ref, NAME_FORMAT) == "Big Book 1:1–2; Small Book 1–2"


def test_multiple_library_range():
    ref = reference(
        range(verse(1, 2, 1, 1), verse(1, 2, 1, 2)),
        range(verse(2, 1, 2, 1), verse(2, 1, 2, 1)),
    )
    assert fmt.format(ref, NAME_FORMAT) == "Big Book 1:1–2; 4 Book 2:1"


def test_book_chapters_greater_than_1():
    """
    Book ID 2 is Big Book; references should show chapter numbers.
    """
    ref = reference(
        range(verse(1, 2, 1, 1), verse(1, 2, 1, 2)),
    )
    assert fmt.format(ref, NAME_FORMAT) == "Big Book 1:1–2"


def test_book_chapter_equal_1():
    """
    Book ID 3 is Small Book; references should not show chapter numbers.
    """
    ref = reference(
        range(verse(1, 3, 1, 1), verse(1, 3, 1, 2)),
    )
    assert fmt.format(ref, NAME_FORMAT) == "Small Book 1–2"
