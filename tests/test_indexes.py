import pytest
from context import *

from refspy.indexes import (
    add_unique_book_alias,
    add_unique_library_alias,
    index_book_aliases,
    index_books,
    index_libraries,
    index_library_aliases,
)
from refspy.types.book import Book
from refspy.types.library import Library

bk_1 = Book(
    id=1, name="Book", abbrev="Bk", code="bk", depth=2, aliases=["vol"], chapters=10
)
bk_2 = Book(id=2, name="Book", abbrev="Bk", code="bk", depth=2, aliases=[], chapters=10)

lib_1 = Library(id=1, name="Library", abbrev="Lib", code="lib", books=[bk_1])
lib_2 = Library(id=2, name="Library", abbrev="Lib", code="lib", books=[bk_1, bk_2])


def test_book_uniqueness():
    index = dict()
    add_unique_book_alias(index, "Library", 1, 1)
    add_unique_book_alias(index, "Other Library", 1, 2)
    with pytest.raises(ValueError):
        add_unique_book_alias(index, "Library", 1, 3)


def test_index_books():
    index = index_books([lib_2])
    assert len(index) == 2
    assert index[2, 1] == bk_1
    assert index[2, 2] == bk_2


def test_index_book_aliases():
    index = index_book_aliases([lib_1])
    assert len(index) == 3
    assert index["Book"] == (1, 1)
    assert index["Bk"] == (1, 1)
    # assert index["bk"] == (1, 1)
    # assert index["vol"] == (1, 1)


def test_library_uniqueness():
    index = dict()
    add_unique_library_alias(index, "Book", 1)
    add_unique_library_alias(index, "Other Book", 2)
    with pytest.raises(ValueError):
        add_unique_library_alias(index, "Book", 3)


def test_index_libraries():
    index = index_libraries([lib_1])
    assert len(index) == 1
    assert index[1] == lib_1


def test_index_library_aliases():
    index = index_library_aliases([lib_1])
    assert index["Library"] == 1
    assert index["Lib"] == 1
    # assert index["lib"] == 1
