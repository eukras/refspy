from context import *

from refspy.languages.english import ENGLISH
from refspy.libraries.en_US import OT, NT
from refspy.manager import Manager
from refspy.range import range, verse_range
from refspy.reference import reference, verse_reference
from refspy.verse import verse

__ = Manager(libraries=[OT, NT], language=ENGLISH)


def test_number_ranges():
    tuples = __.find_references("Romans 1:1–4, 6, 7-9")
    assert tuples[0][1] == reference(
        verse_range(NT.id, 6, 1, 1, 4),
        verse_range(NT.id, 6, 1, 6),
        verse_range(NT.id, 6, 1, 7, 9),
    )


def test_multi_chapter_ranges():
    _, ref = __.first_reference("Rom 1:1-2:4")
    assert ref == reference(range(verse(NT.id, 6, 1, 1), verse(NT.id, 6, 2, 4)))


def test_one_chapter_books():
    refs = __.find_references("Philemon 3-6, v.15")
    assert refs[0][1] == reference(verse_range(NT.id, 18, 1, 3, 6))
    assert refs[1][1] == reference(verse_range(NT.id, 18, 1, 15))


def test_verse_markers():
    refs = __.find_references("Romans 1:1, v.9, vv.11-12")
    assert refs[0][1] == verse_reference(NT.id, 6, 1, 1)
    assert refs[1][1] == verse_reference(NT.id, 6, 1, 9)
    assert refs[2][1] == verse_reference(NT.id, 6, 1, 11, 12)


def test_books_with_number_prefixes():
    refs = __.find_references("Romans 1:1, 2, 3 John 3")
    #             MATCH THIS:  ^^^^^^^^^^^^^  ^^^^^^^^
    #               NOT THIS:  ^^^^^^^^^^^^^^^^ ^^^^^^
    assert refs[0][1] == reference(
        verse_range(NT.id, 6, 1, 1), verse_range(NT.id, 6, 1, 2)
    )
    assert refs[1][1] == verse_reference(NT.id, 25, 1, 3)


def test_substitute_number_prefixes():
    refs = __.find_references("I Cor 2:3; First Cor 2:3; 1st Cor 2:3")
    assert refs[0][1] == refs[1][1] == refs[2][1]
    refs = __.find_references("II Thess 2:3, Second Thess 2:3, 2nd Thess 2:3")
    assert refs[0][1] == refs[1][1] == refs[2][1]
    refs = __.find_references("III John 2; Third John 2; 3rd John 2")
    assert refs[0][1] == refs[1][1] == refs[2][1]


def test_backward_ranges_and_abbreviations():
    tuples = __.find_references("Romans 1:4–1, Rom 1:776-77, Rom 1:13-4")
    # No match for first reference
    assert len(tuples) == 2
    assert tuples[0][1] == verse_reference(NT.id, 6, 1, 776, 777)
    assert tuples[1][1] == verse_reference(NT.id, 6, 1, 13, 14)


def test_partial_verses():
    _, ref = __.first_reference("Rom 1:1a-2:4b")
    #                                   ^    ^  <-- Ignore letters
    assert ref == reference(range(verse(NT.id, 6, 1, 1), verse(NT.id, 6, 2, 4)))


def test_brackets():
    tuples = __.find_references("Romans (John 1:1–4 (1 Cor 5:24 ()) 3:16) 1:16-17")
    #                    MATCH:  xxxxxx  ^^^^^^^^^^  ^^^^^^^^^^     ^^^^  ^^^^^^^
    #                            ^ Don't match it, but use context later: ^^^^^^^
    assert len(tuples) == 4
    assert tuples[0][1] == verse_reference(NT.id, 4, 1, 1, 4)
    assert tuples[1][1] == verse_reference(NT.id, 7, 5, 24)
    assert tuples[2][1] == verse_reference(NT.id, 4, 3, 16)
    assert tuples[3][1] == verse_reference(NT.id, 6, 1, 16, 17)


def test_malformed_brackets():
    tuples = __.find_references("Romans )John 1:1–4 (1 Cor 5:24 (() 3:16) 1:16-17")
    #                            ^^^ Ignore          ^^^ 1 Corinthians
    print(tuples)
    assert tuples[0][1] == verse_reference(NT.id, 4, 1, 1, 4)
    assert tuples[1][1] == verse_reference(NT.id, 7, 5, 24)
    assert tuples[2][1] == verse_reference(NT.id, 7, 3, 16)
    assert tuples[3][1] == verse_reference(NT.id, 7, 1, 16, 17)
