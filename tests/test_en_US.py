from context import *

from refspy import refspy
from refspy.libraries.en_US import NT
from refspy.reference import verse_reference

__ = refspy()


def test_numbered_books():
    """
    Simple sanity checks for the books in the en_US libraries.
    """
    assert __.r("1 Cor 1:4") == verse_reference(NT.id, 7, 1, 4)
    assert __.r("2 Cor 1:4") == verse_reference(NT.id, 8, 1, 4)
    assert __.r("1 Corinthians 1:4") == verse_reference(NT.id, 7, 1, 4)
    assert __.r("2 Corinthians 1:4") == verse_reference(NT.id, 8, 1, 4)

    assert __.r("First Cor 1:4") == verse_reference(NT.id, 7, 1, 4)
    assert __.r("First Corinthians 1:4") == verse_reference(NT.id, 7, 1, 4)
    assert __.r("Second Cor 1:4") == verse_reference(NT.id, 8, 1, 4)
    assert __.r("Second Corinthians 1:4") == verse_reference(NT.id, 8, 1, 4)

    assert __.r("1st Cor 1:4") == verse_reference(NT.id, 7, 1, 4)
    assert __.r("1st Corinthians 1:4") == verse_reference(NT.id, 7, 1, 4)
    assert __.r("2nd Cor 1:4") == verse_reference(NT.id, 8, 1, 4)
    assert __.r("2nd Corinthians 1:4") == verse_reference(NT.id, 8, 1, 4)

    assert __.r("I Cor 1:4") == verse_reference(NT.id, 7, 1, 4)
    assert __.r("I Corinthians 1:4") == verse_reference(NT.id, 7, 1, 4)

    assert __.r("II Cor 1:4") == verse_reference(NT.id, 8, 1, 4)
    assert __.r("II Corinthians 1:4") == verse_reference(NT.id, 8, 1, 4)
