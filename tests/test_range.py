from context import *

from pydantic import ValidationError
import pytest

from refspy.range import book, chapter, Range, range
from refspy.verse import verse


def test_shorthand():
    v1 = verse(1, 2, 3, 4)
    v2 = verse(1, 2, 3, 5)
    _ = range(v1, v2)
    assert _.start == v1
    assert _.end == v2


def test_construction():
    v1 = verse(1, 2, 3, 4)
    v2 = verse(1, 2, 3, 5)
    _ = Range(start=v1, end=v2)
    assert _.start == v1
    assert _.end == v2


def test_wrong_number_of_args():
    with pytest.raises(TypeError):
        _ = range(verse(1, 2, 3, 4))
    with pytest.raises(TypeError):
        _ = range(verse(1, 2, 3, 4), verse(1, 2, 3, 4), verse(1, 2, 3, 4))


def test_wrong_verse_order():
    with pytest.raises(ValidationError):
        v1 = verse(1, 2, 3, 4)
        v2 = verse(1, 2, 3, 5)
        _ = Range(start=v2, end=v1)


def test_overlaps():
    r1 = range(verse(1, 2, 3, 4), verse(1, 2, 3, 8))
    r2 = range(verse(1, 2, 3, 6), verse(1, 2, 3, 8))
    r3 = range(verse(1, 2, 3, 9), verse(1, 2, 3, 12))
    assert r1.overlaps(r2)
    assert not r1.overlaps(r3)
    assert not r2.overlaps(r3)


def test_contains():
    r1 = range(verse(1, 2, 3, 4), verse(1, 2, 3, 8))
    r2 = range(verse(1, 2, 3, 6), verse(1, 2, 3, 8))
    r3 = range(verse(1, 2, 3, 9), verse(1, 2, 3, 12))
    assert r1.contains(r2)
    assert not r2.contains(r1)
    assert not r3.contains(r1)


def test_adjoins():
    vr1 = range(verse(1, 2, 3, 3), verse(1, 2, 3, 4))
    vr2 = range(verse(1, 2, 3, 5), verse(1, 2, 3, 6))
    cr1 = range(verse(1, 2, 3, 1), verse(1, 2, 4, 999))
    cr2 = range(verse(1, 2, 5, 1), verse(1, 2, 6, 999))
    assert vr1.adjoins(vr2)
    assert vr2.adjoins(vr1)
    assert cr1.adjoins(cr2)
    assert cr2.adjoins(cr1)
    assert not cr1.adjoins(vr1)
    assert not cr2.adjoins(vr2)


def test_is_book_range():
    assert range(verse(1, 1, 1, 1), verse(1, 2, 999, 999)).is_book_range()


def test_is_inter_book_range():
    assert range(verse(1, 1, 1, 1), verse(1, 2, 1, 1)).is_inter_book_range()


def test_is_book():
    assert range(verse(1, 1, 1, 1), verse(1, 1, 999, 999)).is_book()
    assert book(1, 1).is_book()


def test_is_chapter_range():
    assert range(verse(1, 1, 1, 1), verse(1, 1, 2, 999)).is_chapter_range()


def test_is_inter_chapter_range():
    assert range(verse(1, 1, 1, 2), verse(1, 1, 3, 4)).is_inter_chapter_range()


def test_is_chapter():
    assert range(verse(1, 1, 1, 1), verse(1, 1, 1, 999)).is_chapter()
    assert chapter(1, 1, 1).is_chapter()


def test_is_verse_range():
    assert range(verse(1, 1, 1, 1), verse(1, 1, 1, 2)).is_verse_range()


def test_is_verse():
    assert range(verse(1, 1, 1, 1), verse(1, 1, 1, 1)).is_verse()


def test_chapter_range():
    _ = chapter(1, 2, 3)
    assert _.start == verse(1, 2, 3, 1)
    assert _.end == verse(1, 2, 3, 999)


def test_book_range():
    _ = book(1, 2)
    assert _.start == verse(1, 2, 1, 1)
    assert _.end == verse(1, 2, 999, 999)
