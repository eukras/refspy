from typing import Dict, List, Tuple
from refspy.library import Library
from refspy.verse import Number


def index_libraries(libraries: List[Library]):
    index = dict()
    for library in libraries:
        index[library.id] = library
    return index


def index_books(libraries: List[Library]):
    index = dict()
    for library in libraries:
        for book in library.books:
            index[library.id, book.id] = book
    return index


def add_unique_library_alias(
    index: Dict[str, Number], alias: str, library_id: Number, strict=True
):
    if alias in index and strict:
        raise ValueError(f"Library alias '{alias}' is not unique.")
    else:
        index[alias] = library_id


def add_unique_book_alias(
    index: Dict[str, Tuple[Number, Number]],
    alias: str,
    library_id: Number,
    book_id: Number,
    strict: bool = True,
):
    if alias in index and strict:
        raise ValueError(f"Book alias '{alias}' is not unique.")
    if alias == "":
        raise ValueError(f"Book alias is '' for ({library_id},{book_id})")
    else:
        index[alias] = (library_id, book_id)


def index_library_aliases(libraries: List[Library]):
    index = dict()
    for library in libraries:
        add_unique_library_alias(index, library.name, library.id)
        add_unique_library_alias(index, library.abbrev, library.id, strict=False)
        add_unique_library_alias(index, library.code, library.id)
    return index


def index_book_aliases(libraries: List[Library]):
    index = dict()
    for library in libraries:
        for book in library.books:
            add_unique_book_alias(index, book.name, library.id, book.id)
            add_unique_book_alias(index, book.abbrev, library.id, book.id, strict=False)
            # add_unique_book_alias(index, book.code, library.id, book.id)
            for alias in book.aliases:
                add_unique_book_alias(index, alias, library.id, book.id)
    return index
