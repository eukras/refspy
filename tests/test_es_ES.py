from context import *

from refspy import refspy
from refspy.libraries.en_US import NT
from refspy.reference import verse_reference

__ = refspy('catholic', 'es_ES')

def test_numbered_books():
    """
    Simple sanity checks for the books in the en_US libraries.
    """
    assert __.r('1 Cor 1:4') == verse_reference(NT.id, 7, 1, 4)
    assert __.r('2 Cor 1:4') == verse_reference(NT.id, 8, 1, 4)
    assert __.r('1 Co 1:4') == verse_reference(NT.id, 7, 1, 4)
    assert __.r('2 Co 1:4') == verse_reference(NT.id, 8, 1, 4)
    assert __.r('1 Corintios 1:4') == verse_reference(NT.id, 7, 1, 4)
    assert __.r('2 Corintios 1:4') == verse_reference(NT.id, 8, 1, 4)

    assert __.r('Primero Cor 1:4') == verse_reference(NT.id, 7, 1, 4)
    assert __.r('Primero Corintios 1:4') == verse_reference(NT.id, 7, 1, 4)
    assert __.r('Segundo Cor 1:4') == verse_reference(NT.id, 8, 1, 4)
    assert __.r('Segundo Corintios 1:4') == verse_reference(NT.id, 8, 1, 4)

    assert __.r('1ro Cor 1:4') == verse_reference(NT.id, 7, 1, 4)
    assert __.r('1ro Corintios 1:4') == verse_reference(NT.id, 7, 1, 4)
    assert __.r('2do Cor 1:4') == verse_reference(NT.id, 8, 1, 4)
    assert __.r('2do Corintios 1:4') == verse_reference(NT.id, 8, 1, 4)

    assert __.r('I Cor 1:4') == verse_reference(NT.id, 7, 1, 4)
    assert __.r('I Corintios 1:4') == verse_reference(NT.id, 7, 1, 4)
    assert __.r('i Cor 1:4') == verse_reference(NT.id, 7, 1, 4)
    assert __.r('i Corintios 1:4') == verse_reference(NT.id, 7, 1, 4)

    assert __.r('II Cor 1:4') == verse_reference(NT.id, 8, 1, 4)
    assert __.r('II Corintios 1:4') == verse_reference(NT.id, 8, 1, 4)
    assert __.r('ii Cor 1:4') == verse_reference(NT.id, 8, 1, 4)
    assert __.r('ii Corintios 1:4') == verse_reference(NT.id, 8, 1, 4)
