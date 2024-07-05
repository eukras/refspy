"""Indexing functions for libraries, books, and book aliases."""

from typing import Dict, List, Tuple
from refspy.book import Book
from refspy.library import Library
from refspy.verse import Number


def index_libraries(libraries: List[Library]) -> Dict[Number, Library]:
    """Create a lookup dict for libraries by library.id"""
    index = dict()
    for library in libraries:
        index[library.id] = library
    return index


def index_books(libraries: List[Library]) -> Dict[Tuple[Number, Number], Book]:
    """Create a lookup dict for books by (library.id, book.id)"""
    index = dict()
    for library in libraries:
        for book in library.books:
            index[library.id, book.id] = book
    return index


def add_unique_book_alias(
    index: Dict[str, Tuple[Number, Number]],
    alias: str,
    library_id: Number,
    book_id: Number,
    strict: bool = True,
):
    """Add an index entry for a library and book if none exists

    Modifies the passed index dict.

    Args:
        strict: raise an error in the case of a collision between
            alias values.
    """
    if alias in index and strict:
        raise ValueError(f"Book alias '{alias}' is not unique.")
    if alias == "":
        raise ValueError(f"Book alias is '' for ({library_id},{book_id})")
    else:
        index[alias] = (library_id, book_id)


def index_book_aliases(
    libraries: List[Library], code_only: bool = False, strict: bool = True
) -> Dict[str, Tuple[Number, Number]]:
    """Create a lookup table for library and book IDs by book aliases.

    Args:
        libraries: A list of `refspy.library.Library` objects to be indexed.
        code_only: Index for the purpose of reading URL params (use book.code
            only, not book name, abbrev, or aliases).
        strict: Throw a ValueError if any two aliases are the same, or any
            alias is an empty string.

    Note:
        Because books like Ruth or Mark have book.abbrev == book.name, we only
        index the abbrev if it differs from the name. These books will not raise
        a ValueError when strict=True.
    """
    index = dict()
    for library in libraries:
        for book in library.books:
            if code_only:
                add_unique_book_alias(index, book.code, library.id, book.id, strict)
            else:
                add_unique_book_alias(index, book.name, library.id, book.id, strict)
                if book.name != book.abbrev:
                    add_unique_book_alias(
                        index, book.abbrev, library.id, book.id, strict
                    )
                for alias in book.aliases:
                    add_unique_book_alias(index, alias, library.id, book.id, strict)
    return index
