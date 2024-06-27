"""
Basic integration tests at the Manager facade level.
THis file doubles as an example of intended usage.
Unit testing to occur in each supordinate file.
"""

import pytest

from context import *

from refspy.languages.english import ENGLISH
from refspy.manager import Manager
from refspy.range import range
from refspy.reference import reference
from refspy.types.book import Book
from refspy.types.library import Library
from refspy.verse import verse

BOOK = Book(
    id=2, name="Book", abbrev="Bk", code="bk", depth=2, aliases=["vol"], chapters=3
)

LIBRARY = Library(id=1, name="Library", abbrev="Lib", code="lib", books=[BOOK])

# 'Book 1:1–2' in Library
REFERENCES = [
    reference(
        [range(verse(LIBRARY.id, BOOK.id, 1, 1), verse(LIBRARY.id, BOOK.id, 1, 2))]
    )
]

__ = Manager([LIBRARY], ENGLISH)


def test_init():
    """
    Initialising a reference manager should create indexes for all the aliases.
    """
    assert __.libraries[LIBRARY.id] == LIBRARY
    assert __.library_aliases["Library"] == LIBRARY.id
    assert __.library_aliases["Lib"] == LIBRARY.id
    # assert __.library_aliases["lib"] == LIBRARY.id
    assert __.book_aliases["Book"] == (LIBRARY.id, BOOK.id)
    assert __.book_aliases["Bk"] == (LIBRARY.id, BOOK.id)
    # assert __.book_aliases["bk"] == (LIBRARY.id, BOOK.id)
    # assert __.book_aliases["vol"] == (LIBRARY.id, BOOK.id)


def test_non_unique():
    """
    Repeating any name/alias/code values raise an error.
    """
    with pytest.raises(ValueError):
        _ = Manager([LIBRARY, LIBRARY], ENGLISH)


def collate_by_id():
    __ = Manager([LIBRARY], ENGLISH)
    collation = __.collate(REFERENCES)
    for library_id, book_collation in collation:
        assert library_id == LIBRARY.id
        for book_id, book_references in book_collation:
            assert book_id == BOOK.id
            assert book_references == REFERENCES


def test_collate():
    __ = Manager([LIBRARY], ENGLISH)
    collation = __.collate(REFERENCES)
    for library, book_collation in collation:
        assert library == LIBRARY
        for book, book_references in book_collation:
            assert book == BOOK
            assert book_references == REFERENCES


def test_first_reference():
    text = "Book 1:1"
    _, reference = __.first_reference(text)
    assert reference is not None
    assert __.name(reference) == text


def test_find_references():
    tuples = __.find_references("Book 1:1–2:4")
    _, reference = tuples[0]
    assert reference is not None
    assert __.name(reference) == "Book 1:1–2:4"


def test_find_all():
    text = "Book 1:1, Book 2:2"
    tuples = list(__.find_references(text))
    assert tuples[0] == ("Book 1:1", __.r("Book 1:1"))
    assert tuples[1] == ("Book 2:2", __.r("Book 2:2"))


def test_next_chapter():
    __ = Manager([LIBRARY], ENGLISH)
    ch_1 = __.bcv("Book", 1)
    ch_2 = __.bcv("Book", 2)
    assert __.next_chapter(ch_1) == ch_2


def test_prev_chapter():
    __ = Manager([LIBRARY], ENGLISH)
    ch_2 = __.bcv("Book", 2)
    ch_1 = __.bcv("Book", 1)
    assert __.prev_chapter(ch_2) == ch_1


def test_bcv():
    bk = __.bcv("Book")
    assert __.name(bk) == "Book"
    bk_2 = __.bcv("Book", 2)
    assert __.name(bk_2) == "Book 2"
    bk_2_1 = __.bcv("Book", 2, 1)
    assert __.name(bk_2_1) == "Book 2:1"


def test_bcr():
    bk_2_135 = __.bcr("Book", 2, [1, 3, 5])
    assert __.name(bk_2_135) == "Book 2:1,3,5"
    bk_2_1357 = __.bcr("Book", 2, [(1, 3), (5, 7)])
    assert __.name(bk_2_1357) == "Book 2:1–3,5–7"


def test_r():
    ref = __.r("Book 1:1")
    assert ref is not None
    assert __.name(ref) == "Book 1:1"
    ref = __.r("Book 1:1,3")
    assert ref is not None
    assert __.name(ref) == "Book 1:1,3"
    ref = __.r("Book 1:1-3")
    assert ref is not None
    assert __.name(ref) == "Book 1:1–3"
    ref = __.r("Book 1:1-3,5-7")
    assert ref is not None
    assert __.name(ref) == "Book 1:1–3,5–7"
    ref = __.r("Book 1:1–2:4")
    assert ref is not None
    assert __.name(ref) == "Book 1:1–2:4"
    ref = __.r("Book 1:1-2:4")
    assert ref is not None
    assert __.name(ref) == "Book 1:1–2:4"


def test_book():
    ref = __.r("Book 1:1")
    assert ref is not None
    book = __.book(ref)
    assert book.name == "Book"


def test_book_reference():
    ref = __.r("Book 1:1")
    assert ref is not None
    book_ref = __.book_reference(ref)
    assert __.name(book_ref) == "Book"


def test_chapter_reference():
    ref = __.r("Book 1:1")
    assert ref is not None
    chapter_ref = __.chapter_reference(ref)
    assert __.name(chapter_ref) == "Book 1"


def test_abbrev():
    ref = __.r("Book 1:1")
    assert ref is not None
    assert __.abbrev(ref) == "Bk 1:1"


def test_code():
    ref = __.r("Book 1:1")
    assert ref is not None
    assert __.code(ref) == "bk+1.1"


def test_name():
    ref = __.r("Book 1:1")
    assert ref is not None
    assert __.name(ref) == "Book 1:1"


def test_numbers():
    ref = __.r("Book 1:1")
    assert ref is not None
    assert __.numbers(ref) == "1:1"
