from refspy.indexes import index_book_aliases, index_books
from refspy.libraries.en_US import NT
from refspy.navigator import Navigator
from refspy.reference import chapter_reference as ch

books = index_books([NT])
book_aliases = index_book_aliases([NT])
__ = Navigator(books, book_aliases)


def test_prev_chapter():
    assert __.prev_chapter(ch(400, 6, 7)) == ch(400, 6, 6)  # Rom 7 -> Rom 6
    assert __.prev_chapter(ch(400, 6, 1)) == ch(400, 5, 28)  # Rom 1 -> Acts 28
    assert __.prev_chapter(ch(400, 1, 1)) is None  # Matt 1 -> None


def test_next_chapter():
    assert __.next_chapter(ch(400, 6, 7)) == ch(400, 6, 8)  # Rom 7 -> Rom 8
    assert __.next_chapter(ch(400, 6, 16)) == ch(400, 7, 1)  # Rom 16 -> 1 Cor 1
    assert __.next_chapter(ch(400, 27, 22)) is None  # Rev 22 -> None
