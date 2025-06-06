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


def test_skips_ambiguous_aliases_for_context_references():
    """See `refspy.languages` for ambiguous_aliases.
    """
    __ = refspy()
    refs = __.find_references("Am. Am 3:1.")
    #                          ^^  Only match the second reference.
    assert len(refs) == 1
    assert refs[0][0] == 'Am 3:1'
    assert refs[0][1] == __.bcv('Amos', 3, 1)
