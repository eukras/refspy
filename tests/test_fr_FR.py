from context import *

from refspy import refspy
from refspy.libraries.fr_FR import NT
from refspy.reference import verse_reference

__ = refspy('catholic', 'fr_FR')

def test_numbered_books():
    """
    Simple sanity checks for the books in the fr_FR libraries.
    """
    I_COR_1_4 = verse_reference(NT.id, 7, 1, 4)
    II_COR_1_4 = verse_reference(NT.id, 8, 1, 4)

    assert __.r('1 Co 1, 4') == I_COR_1_4
    assert __.r('2 Co 1, 4') == II_COR_1_4
    assert __.r('1 Corinthiens 1, 4') == I_COR_1_4
    assert __.r('2 Corinthiens 1, 4') == II_COR_1_4

    assert __.r('Première Lettre à Co 1, 4') == I_COR_1_4
    assert __.r('Première Lettre à Corinthiens 1, 4') == I_COR_1_4
    assert __.r('Seconde Lettre à Co 1, 4') == II_COR_1_4
    assert __.r('Seconde Lettre à Corinthiens 1, 4') == II_COR_1_4

    assert __.r('1ere Co 1, 4') == I_COR_1_4
    assert __.r('1ere Corinthiens 1, 4') == I_COR_1_4
    assert __.r('2nd Co 1, 4') == II_COR_1_4
    assert __.r('2nd Corinthiens 1, 4') == II_COR_1_4

    assert __.r('I Co 1, 4') == I_COR_1_4
    assert __.r('I Corinthiens 1, 4') == I_COR_1_4
    assert __.r('II Co 1, 4') == II_COR_1_4
    assert __.r('II Corinthiens 1, 4') == II_COR_1_4
