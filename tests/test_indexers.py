import pytest
from context import *

from refspy.indexers import (
    add_unique_book_alias,
    index_book_aliases,
    index_books,
    index_libraries,
)
from refspy.book import Book
from refspy.library import Library

bk_1 = Book(id=1, name="Book", abbrev="Bk", aliases=["vol"], chapters=10)
bk_2 = Book(id=2, name="Book", abbrev="Bk", aliases=[], chapters=10)
bk_3 = Book(id=3, name="3 Book", abbrev="3 Bk", aliases=[], chapters=1)

lib_1 = Library(id=1, name="Library", abbrev="Lib", books=[bk_1])
lib_2 = Library(id=2, name="Library", abbrev="Lib", books=[bk_1, bk_2, bk_3])


def test_book_uniqueness():
    index = dict()
    add_unique_book_alias(index, "Library", 1, 1)
    add_unique_book_alias(index, "Other Library", 1, 2)
    with pytest.raises(ValueError):
        add_unique_book_alias(index, "Library", 1, 3)


def test_index_books():
    index = index_books([lib_2])
    assert len(index) == 3
    assert index[2, 1] == bk_1
    assert index[2, 2] == bk_2


def test_index_book_aliases():
    index = index_book_aliases([lib_1])
    assert len(index) == 3
    assert index["Book"] == (1, 1)
    assert index["Bk"] == (1, 1)


def test_non_strict_index_book_aliases_with_params():
    index = index_book_aliases([lib_2], url_param_names=True, strict=False)
    assert len(index) == 5
    assert index["book"] == (2, 2)
    assert index["bk"] == (2, 2)
    assert index["3+book"] == (2, 3)
    assert index["3+bk"] == (2, 3)


def test_index_libraries():
    index = index_libraries([lib_1])
    assert len(index) == 1
    assert index[1] == lib_1
