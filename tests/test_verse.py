from pydantic import ValidationError
import pytest

from refspy.verse import verse, Verse


def test_shorthand():
    _ = verse(1, 2, 3, 4)
    assert _.library == 1
    assert _.book == 2
    assert _.chapter == 3
    assert _.verse == 4


def test_from_index():
    _ = Verse.from_index(1002003004)
    assert _.library == 1
    assert _.book == 2
    assert _.chapter == 3
    assert _.verse == 4


def test_keyword_args():
    _ = Verse(library=1, book=2, chapter=3, verse=4)
    assert _.library == 1
    assert _.book == 2
    assert _.chapter == 3
    assert _.verse == 4


def test_args_out_of_number_range():
    with pytest.raises(ValidationError):
        _ = verse(0, 2, 3, 4)
    with pytest.raises(ValidationError):
        _ = verse(1000, 2, 3, 4)
    with pytest.raises(ValidationError):
        _ = verse(1, 0, 3, 4)
    with pytest.raises(ValidationError):
        _ = verse(1, 1000, 3, 4)
    with pytest.raises(ValidationError):
        _ = verse(1, 2, 0, 4)
    with pytest.raises(ValidationError):
        _ = verse(1, 2, 1000, 4)
    with pytest.raises(ValidationError):
        _ = verse(1, 2, 3, 0)
    with pytest.raises(ValidationError):
        _ = verse(1, 2, 3, 1000)


def test_tuples():
    _ = verse(1, 2, 3, 4)
    assert _.tuple() == (1, 2, 3, 4)


def test_index_numbers():
    _ = verse(1, 2, 3, 4)
    assert _.index() == 1002003004
