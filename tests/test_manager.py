import pytest
from context import *

from refspy import refspy
from refspy.book import Book
from refspy.languages.english import ENGLISH
from refspy.libraries.en_US import NT
from refspy.library import Library
from refspy.manager import Manager
from refspy.range import range
from refspy.reference import reference, verse_reference
from refspy.verse import verse

BOOK = Book(id=2, name="Book", abbrev="Bk", aliases=["vol"], chapters=3)

LIBRARY = Library(id=1, name="Library", abbrev="Lib", books=[BOOK])

REFERENCES = [
    # 'Book 1:1–2' in Library
    reference(range(verse(LIBRARY.id, BOOK.id, 1, 1), verse(LIBRARY.id, BOOK.id, 1, 2)))
]

__ = Manager([LIBRARY], ENGLISH)
REFSPY = refspy()


def test_init():
    assert __.libraries[LIBRARY.id] == LIBRARY
    assert __.book_aliases["Book"] == (LIBRARY.id, BOOK.id)

def test_make_index_references():
    tuples = __.find_references("Book 1:2, 2:1, 3:4, 1:4-5, 7, 3:6")
    refs = __.make_index_references([ref for _, ref in tuples if ref])
    assert ','.join([__.template(ref) for ref in refs if ref is not None]) == "Bk 1:2, 4–5, 7; 2:1; 3:4, 6"

def test_make_index():
    tuples = __.find_references("Book 1:2, 2:1, 3:4, 1:4-5, 7, 3:6")
    text = __.make_index([ref for _, ref in tuples if ref])
    assert text == "Bk 1:2, 4–5, 7; 2:1; 3:4, 6"


# MEMO: Should return [(chapter_reference, total), ...] for hotspots.
def test_make_hotspots():
    tuples = __.find_references("Book 1:2, 2:1, 3:4, 1:4-5, 7, 3:6")
    out = __.make_hotspots(
        [ref for _, ref in tuples if ref], max_chapters=2, min_references=2
    )
    assert out == 'Bk 1, Bk 3'


def test_make_hotspots_lots():
    tuples = __.find_references("Book 1:2, 2:1, 3:4, 1:4-5, 7, 3:6, " * 100)
    out = __.make_hotspots(
        [ref for _, ref in tuples if ref], max_chapters=2, min_references=2
    )
    assert out == 'Bk 1, Bk 3'


def test_make_hotspots_empty():
    text = __.make_hotspots([], max_chapters=2, min_references=2)
    assert text is None


def test_non_unique():
    """
    Repeating any name/alias values raise an error.
    """
    with pytest.raises(ValueError):
        _ = Manager([LIBRARY, LIBRARY], ENGLISH)


def test_sort_references():
    ref_1 = verse_reference(NT.id, 1, 2, 3)
    ref_2 = verse_reference(NT.id, 1, 2, 4)
    ref_3 = verse_reference(NT.id, 1, 2, 5)
    sorted_ref = __.sort_references([ref_3, ref_2, ref_1])
    assert sorted_ref.ranges == [ref_1.ranges[0], ref_2.ranges[0], ref_3.ranges[0]]


def test_merge_references():
    ref_1 = verse_reference(NT.id, 1, 2, 3)
    ref_2 = verse_reference(NT.id, 1, 2, 3, 4)
    ref_3 = verse_reference(NT.id, 1, 2, 4, 5)
    merged = __.merge_references([ref_3, ref_2, ref_1])
    assert len(merged.ranges) == 1
    assert merged == verse_reference(NT.id, 1, 2, 3, 5)


def test_combine_references():
    ref_1 = verse_reference(NT.id, 1, 2, 3)
    ref_2 = verse_reference(NT.id, 1, 2, 4)
    ref_3 = verse_reference(NT.id, 1, 2, 5, 6)
    combined = __.combine_references([ref_3, ref_2, ref_1])
    assert len(combined.ranges) == 1
    assert combined == verse_reference(NT.id, 1, 2, 3, 6)


def test_collate_by_id():
    collation = __.collate_by_id(REFERENCES)
    for library_id, book_collation in collation.items():
        assert library_id == LIBRARY.id
        for book_id, book_references in book_collation.items():
            assert book_id == BOOK.id
            assert book_references == REFERENCES


def test_collate():
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
    assert __.name(bk_2_135) == "Book 2:1, 3, 5"
    bk_2_1357 = __.bcr("Book", 2, [(1, 3), (5, 7)])
    assert __.name(bk_2_1357) == "Book 2:1–3, 5–7"


def test_r():
    ref = __.r("Book 1:1")
    assert ref is not None
    assert __.name(ref) == "Book 1:1"
    ref = __.r("Book 1:1, 3")
    assert ref is not None
    assert __.name(ref) == "Book 1:1, 3"
    ref = __.r("Book 1:1-3")
    assert ref is not None
    assert __.name(ref) == "Book 1:1–3"
    ref = __.r("Book 1:1-3, 5-7")
    assert ref is not None
    assert __.name(ref) == "Book 1:1–3, 5–7"
    ref = __.r("Book 1:1–2:4")
    assert ref is not None
    assert __.name(ref) == "Book 1:1–2:4"
    ref = __.r("Book 1:1-2:4")
    assert ref is not None
    assert __.name(ref) == "Book 1:1–2:4"


def test_get_book():
    ref = __.r("Book 1:1")
    assert ref is not None
    book = __.get_book(ref)
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


def test_name():
    ref = __.r("Book 1:1")
    assert ref is not None
    assert __.name(ref) == "Book 1:1"


def test_book():
    ref = __.r("Book 1:1")
    assert ref is not None
    assert __.book(ref) == "Book"


def test_numbers():
    ref = __.r("Book 1:1")
    assert ref is not None
    assert __.numbers(ref) == "1:1"


def test_abbrev_name():
    ref = __.r("Book 1:1")
    assert ref is not None
    assert __.abbrev_name(ref) == "Bk 1:1"


def test_abbrev_book():
    ref = __.r("Book 1:1")
    assert ref is not None
    assert __.abbrev_book(ref) == "Bk"


def test_template():
    ref = __.r("1 Cor 2:3-4, 5")
    if ref is not None:
        assert __.template(ref, "x {NAME}") == "x 1 Corinthians 2:3–4, 5"
        assert __.template(ref, "x {BOOK}") == "x 1 Corinthians"
        assert __.template(ref, "x {NUMBERS}") == "x 2:3–4, 5"
        assert __.template(ref, "x {ABBREV_NAME}") == "x 1 Cor 2:3–4, 5"
        assert __.template(ref, "x {ABBREV_BOOK}") == "x 1 Cor"
        assert __.template(ref, "x {ABBREV_NUMBERS}") == "x 2:3–4, 5"
        assert __.template(ref, "x {ESC_NAME}") == "x 1%20Corinthians%202%3A3-4,%205"
        assert __.template(ref, "x {ESC_BOOK}") == "x 1%20Corinthians"
        assert __.template(ref, "x {ESC_NUMBERS}") == "x 2%3A3-4,%205"
        assert __.template(ref, "x {ESC_ABBREV_NAME}") == "x 1%20Cor%202%3A3-4,%205"
        assert __.template(ref, "x {ESC_ABBREV_BOOK}") == "x 1%20Cor"
        assert __.template(ref, "x {ESC_ABBREV_NUMBERS}") == "x 2%3A3-4,%205"
        assert __.template(ref, "x {PARAM_NAME}") == "x 1cor+2:3-4,+5"
        assert __.template(ref, "x {PARAM_BOOK}") == "x 1cor"
        assert __.template(ref, "x {PARAM_NUMBERS}") == "x 2:3-4,+5"
