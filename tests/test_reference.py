from pydantic import ValidationError
import pytest

from refspy.reference import reference
from refspy.range import range
from refspy.verse import verse


def test_empty_reference():
    """
    Check empty range lists
    """
    with pytest.raises(ValidationError):
        _ = reference([])


def test_reference_sorting():
    """
    Check that identical range lists are identical references
    """
    range_1 = range(verse(1, 2, 3, 4), verse(1, 2, 3, 6))
    range_2 = range(verse(1, 2, 3, 7), verse(1, 2, 3, 8))
    reference_1 = reference([range_1, range_2])
    reference_2 = reference([range_2, range_1])

    assert reference_1 == reference_2


def test_reference_addition():
    """
    Check that references add correctly
    """
    range_1 = range(verse(1, 2, 3, 4), verse(1, 2, 3, 6))
    range_2 = range(verse(1, 2, 3, 7), verse(1, 2, 3, 8))
    ref_1 = reference([range_1])
    ref_2 = reference([range_2])
    ref_3 = reference([range_1, range_2])

    assert ref_1 + ref_2 == ref_3
