"""Indexing functions for libraries, books, and book aliases."""

from typing import Dict, List, Tuple
from refspy.book import Book
from refspy.library import Library
from refspy.utils import strip_book_number
from refspy.verse import Number

PARAM_CHAR_LIMIT = 20
"""The maximum book name or alias length to convert to URL parameter names."""


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
    libraries: List[Library],
    include_two_letter_aliases: bool = True,
    strict: bool = True
) -> Dict[str, Tuple[Number, Number]]:
    """Create a lookup table for library and book IDs by book aliases.

    Args:
        libraries: A list of `refspy.library.Library` objects to be indexed.
        include_two_letter_aliases: Allow book aliases of only two letters,
            i.e. 'Jn' and '1 Ti'.
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
            aliases = [book.name]
            if book.name != book.abbrev:
                aliases.append(book.abbrev)
            for alias in book.aliases:
                len_alias = len(strip_book_number(alias))
                if (
                    (len_alias > 2 and len_alias < PARAM_CHAR_LIMIT) or
                    (include_two_letter_aliases and len_alias == 2)
                ):
                    aliases.append(alias)
            for alias in aliases:
                add_unique_book_alias(index, alias, library.id, book.id, strict)
    return index
