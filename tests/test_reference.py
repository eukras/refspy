from context import *

from pydantic import ValidationError
import pytest

from refspy.reference import (
    chapter_reference,
    reference,
    verse_reference,
)
from refspy.range import range
from refspy.verse import verse


def test_empty_reference_raises_value_error():
    """
    Check empty range lists
    """
    with pytest.raises(ValidationError):
        _ = reference()


def test_reference_comparison():
    reference_1 = reference(range(verse(1, 2, 3, 4), verse(1, 2, 3, 6)))
    reference_2 = reference(range(verse(1, 2, 3, 7), verse(1, 2, 3, 8)))
    assert reference_1 < reference_2
    assert min([reference_1, reference_2]) == reference_1
    assert max([reference_1, reference_2]) == reference_2


def test_reference_addition():
    """
    Check that references add correctly
    """
    range_1 = range(verse(1, 2, 3, 4), verse(1, 2, 3, 6))
    range_2 = range(verse(1, 2, 3, 7), verse(1, 2, 3, 8))
    ref_1 = reference(range_1)
    ref_2 = reference(range_2)
    ref_3 = reference(range_1, range_2)

    assert ref_1 + ref_2 == ref_3


def test_contains():
    ch3 = chapter_reference(1, 2, 3)
    ch3v45 = verse_reference(1, 2, 3, 4, 5)
    assert ch3.contains(ch3)
    assert ch3v45.contains(ch3v45)
    assert ch3.contains(ch3v45)
    assert not ch3v45.contains(ch3)


def test_overlaps():
    ch3 = chapter_reference(1, 2, 3)
    ch3v45 = verse_reference(1, 2, 3, 4, 5)
    assert ch3.overlaps(ch3)
    assert ch3v45.overlaps(ch3v45)
    assert ch3.overlaps(ch3v45)
    assert ch3v45.overlaps(ch3)


def test_adjoins():
    ch3v45 = verse_reference(1, 2, 3, 4, 5)
    ch3v67 = verse_reference(1, 2, 3, 6, 7)
    assert ch3v45.adjoins(ch3v67)
    assert ch3v67.adjoins(ch3v45)
