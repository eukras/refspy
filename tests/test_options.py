from context import *

from refspy import refspy

def test_include_two_letter_aliases():
    __ = refspy()  # <-- include two-letter aliases by default
 
    match, ref = __.first_reference("1Ti 2")
    assert match == "1Ti 2"
    assert ref == __.bcv('1 Tim', 2)
    match, ref = __.first_reference("Ge 1:1")
    assert match == "Ge 1:1"
    assert ref == __.bcv('Gen', 1, 1)
    match, ref = __.first_reference("Jn 1:1")
    assert match == "Jn 1:1"
    assert ref == __.bcv('John', 1, 1)


def test_exclude_two_letter_aliases():
    __ = refspy(include_two_letter_aliases=False)  # <-- but not ambiguous aliases

    match, ref = __.first_reference("1Ti 2")
    assert match == None
    assert ref == None
    match, ref = __.first_reference("Ob 2")
    assert match == None
    assert ref == None
    match, ref = __.first_reference("Am 1:1")
    assert match == None
    assert ref == None
    match, ref = __.first_reference("Is 1:1")
    assert match == None
    assert ref == None


def test_include_ambiguous_aliases():
    __ = refspy(include_ambiguous_aliases=True)

    match, ref = __.first_reference("1Ti 2")
    assert match == "1Ti 2"
    assert ref == __.bcv('1 Tim', 2)
    match, ref = __.first_reference("Ob 2:1")
    assert match == "Ob 2:1"
    assert ref == __.bcv('Obadiah', 2, 1)
    match, ref = __.first_reference("Am 2")
    assert match == "Am 2"
    assert ref == __.bcv('Amos', 2)
    match, ref = __.first_reference("Is 1:1")
    assert match == "Is 1:1"
    assert ref == __.bcv('Isaiah', 1, 1)


def test_not_matching_parts_of_words():
    __ = refspy(include_two_letter_aliases=True, include_ambiguous_aliases=True)

    match, ref = __.first_reference("Test test test. Especially the last part.")
    #                                          ^^  Match Esther?
    assert match == None
    assert ref == None

