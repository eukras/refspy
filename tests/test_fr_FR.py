from context import *

from refspy import refspy
from refspy.languages.french import FRENCH
from refspy.libraries.fr_FR import NT

from refspy.models.range import verse_range
from refspy.models.reference import reference, verse_reference

fr_euro = refspy("catholic", "fr_FR", "euro")
fr_intl = refspy("catholic", "fr_FR", "intl")


def test_numbered_books():
    """
    Simple sanity checks for the books in the fr_FR libraries.
    """
    I_COR_1_4 = verse_reference(NT.id, 7, 1, 4)
    II_COR_1_4 = verse_reference(NT.id, 8, 1, 4)
    II_COR_1_4_6 = reference(
        verse_range(NT.id, 8, 1, 4),
        verse_range(NT.id, 8, 1, 6),
    )
    II_COR_1_4_67 = reference(
        verse_range(NT.id, 8, 1, 4),
        verse_range(NT.id, 8, 1, 6, 7),
    )

    assert fr_euro.r("1 Co 1, 4") == I_COR_1_4
    assert fr_euro.r("2 Co 1, 4") == II_COR_1_4
    assert fr_euro.r("2 Co 1, 4.6") == II_COR_1_4_6

    assert fr_euro.r("1 Corinthiens 1, 4") == I_COR_1_4
    assert fr_euro.r("2 Corinthiens 1, 4") == II_COR_1_4

    assert fr_euro.r("Première Lettre à Co 1, 4") == I_COR_1_4
    assert fr_euro.r("Première Lettre à Corinthiens 1, 4") == I_COR_1_4
    assert fr_euro.r("Seconde Lettre à Co 1, 4") == II_COR_1_4
    assert fr_euro.r("Seconde Lettre à Corinthiens 1, 4") == II_COR_1_4

    assert fr_euro.r("1ere Co 1, 4") == I_COR_1_4
    assert fr_euro.r("1ere Corinthiens 1, 4") == I_COR_1_4
    assert fr_euro.r("2nd Co 1, 4") == II_COR_1_4
    assert fr_euro.r("2nd Corinthiens 1, 4") == II_COR_1_4

    assert fr_euro.r("I Co 1, 4") == I_COR_1_4
    assert fr_euro.r("I Corinthiens 1, 4") == I_COR_1_4
    assert fr_euro.r("II Co 1, 4") == II_COR_1_4
    assert fr_euro.r("II Corinthiens 1, 4") == II_COR_1_4

    assert fr_intl.r("2 Co 1:4,6") == II_COR_1_4_6
    assert fr_euro.r("2 Co 1,4.6") == II_COR_1_4_6

    assert fr_intl.r("2 Co 1:4,6-7") == II_COR_1_4_67
    assert fr_euro.r("2 Co 1,4.6-7") == II_COR_1_4_67


def test_multiple_references():
    refs = fr_euro.find_references("Rm 12,1.6-17, 2 Co. 1, 2–3,4, ou bien Philémon 2-3")
    assert len(refs) == 3
    assert refs[0][1] == fr_euro.r("Rm 12,1.6-17")
    assert refs[1][1] == fr_euro.r("2 Co. 1, 2–3,4")
    assert refs[2][1] == fr_euro.r("Philémon 2-3")
