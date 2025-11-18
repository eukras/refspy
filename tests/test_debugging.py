from context import *

from refspy.languages.english import ENGLISH
from refspy.libraries.en_US import OT, NT
from refspy.manager import Manager
from refspy.models.range import range, verse_range
from refspy.models.reference import reference, verse_reference
from refspy.models.verse import verse

__ = Manager(libraries=[OT, NT], language=ENGLISH)


def test_number_ranges():
    refs = __.find_references("Romans 1:1–4, 6, 7-9")
    assert refs[0][1] == reference(
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


def test_ambiguous_verses():
    refs = __.find_references("v.5, v.6-7, 6:5, 8:6-7")
    assert len(refs) == 0


def test_ambiguous_verse_return_none():
    refs = __.find_references("v.5, v.6-7, 6:5, 8:6-7", include_nones=True)
    assert len(refs) == 4


def test_ambiguous_context():
    refs = __.find_references("v.5", include_nones=True)
    assert len(refs) == 1
    refs = __.find_references("8:5", include_nones=True)
    assert len(refs) == 1
    refs = __.find_references("Romans, v.5", include_nones=True)
    assert len(refs) == 1


def test_ambiguous_context_returns_none():
    refs = __.find_references("Romans, v.5", include_nones=True)
    assert len(refs) == 1
    assert refs[0][1] == None


def test_books_with_number_prefixes():
    refs = __.find_references("Romans 1:1, 2, 3 John 3")
    #             MATCH THIS:  ^^^^^^^^^^^^^  ^^^^^^^^
    #               NOT THIS:  ^^^^^^^^^^^^^^^^ ^^^^^^
    assert refs[0][1] == reference(
        verse_range(NT.id, 6, 1, 1), verse_range(NT.id, 6, 1, 2)
    )
    assert refs[1][1] == verse_reference(NT.id, 25, 1, 3)


def test_backward_ranges_and_abbreviations():
    refs = __.find_references("Romans 1:4–1, Rom 1:776-77, Rom 1:13-4")
    # No match for first reference
    assert len(refs) == 2
    assert refs[0][1] == verse_reference(NT.id, 6, 1, 776, 777)
    assert refs[1][1] == verse_reference(NT.id, 6, 1, 13, 14)


def test_partial_verses():
    _, ref = __.first_reference("Rom 1:1a-2:4b")
    #                                   ^    ^  <-- Ignore letters
    assert ref == reference(range(verse(NT.id, 6, 1, 1), verse(NT.id, 6, 2, 4)))


def test_brackets():
    refs = __.find_references("Romans (John 1:1–4 (1 Cor 5:24 ()) 3:16) 1:16-17")
    #                  MATCH:  xxxxxx  ^^^^^^^^^^  ^^^^^^^^^^     ^^^^  ^^^^^^^
    #                          ^ Don't match this, but use for context: ^^^^^^^
    assert len(refs) == 4
    assert refs[0][1] == verse_reference(NT.id, 4, 1, 1, 4)
    assert refs[1][1] == verse_reference(NT.id, 7, 5, 24)
    assert refs[2][1] == verse_reference(NT.id, 4, 3, 16)
    assert refs[3][1] == verse_reference(NT.id, 6, 1, 16, 17)


def test_malformed_brackets():
    refs = __.find_references("Romans )John 1:1–4 (1 Cor 5:24 (() 3:16) 1:16-17")
    #                            ^^^ Ignore          ^^^ 1 Corinthians
    assert refs[0][1] == verse_reference(NT.id, 4, 1, 1, 4)
    assert refs[1][1] == verse_reference(NT.id, 7, 5, 24)
    assert refs[2][1] == verse_reference(NT.id, 7, 3, 16)
    assert refs[3][1] == verse_reference(NT.id, 7, 1, 16, 17)


def test_start_of_words():
    refs = __.find_references(
        "Esxxx Gexxx Rexxx Laxxx!",
        include_books=True,
        include_nones=True,
        # ^Esth ^Gen  ^Rev  ^Lam
    )
    assert len(refs) == 0


def test_merge_long_reference_lists():
    """
    Observed wrong merging in Deut when testing on Westminster confession.
    """
    input = (
        "Deut 2:30; 4:15–16; 4:15–20; 5:32; 6:4; 6:6–7; 6:13 (2); "
        + "7:3–4; 10:4; 10:20; 12:32; 13:6–12; 19:5; 23:21, 23; 24:1–4; "
        + "29:4; 29:19; 29:29; 30:6; 30:19"
    )
    merge_expected = (
        "Deut 2:30; 4:15–20; 5:32; 6:4, 6–7, 13; "
        + "7:3–4; 10:4, 20; 12:32; 13:6–12; 19:5; 23:21, 23; 24:1–4; "
        + "29:4, 19, 29; 30:6, 19"
    )
    references = [ref for _, ref in __.find_references(input) if ref is not None]
    merged = __.merge_references(references)
    output = __.abbrev_name(merged)
    assert output == merge_expected


def test_combine_long_reference_lists():
    """
    Observed wrong merging in Deut when testing on Westminster confession.
    """
    input = (
        "Deut 2:30; 4:15–16; 4:15–20; 5:32; 6:4; 6:6–7; 6:13 (2); "
        + "7:3–4; 10:4; 10:20; 12:32; 13:6–12; 19:5; 23:21, 23; 24:1–4; "
        + "29:4; 29:19; 29:29; 30:6; 30:19"
    )
    merge_expected = (
        "Deut 2:30; 4:15–20; 5:32; 6:4, 6–7, 13; "
        + "7:3–4; 10:4, 20; 12:32; 13:6–12; 19:5; 23:21, 23; 24:1–4; "
        + "29:4, 19, 29; 30:6, 19"
    )
    references = [ref for _, ref in __.find_references(input) if ref is not None]
    merged = __.merge_references(references)
    combined = __.combine_references([merged])
    output = __.abbrev_name(combined)
    assert output == merge_expected


def test_adjoins_cases():
    ref_1 = __.r("Deut 13:6-12")
    ref_2 = __.r("Deut 19:5")
    if ref_1 and ref_2:
        rng_1 = ref_1.ranges[0]
        rng_2 = ref_2.ranges[0]
        # test Deut 13:6-12
        assert not rng_1.is_verse()
        assert rng_1.is_verse_range()
        assert not rng_1.is_inter_chapter_range()
        assert not rng_1.is_chapter()
        assert not rng_1.is_chapter_range()
        assert not rng_1.is_inter_chapter_range()
        assert not rng_1.is_book()
        assert not rng_1.is_book_range()
        # test Deut 19:5
        assert rng_2.is_verse()
        assert not rng_2.is_verse_range()
        assert not rng_2.is_inter_chapter_range()
        assert not rng_2.is_chapter()
        assert not rng_2.is_chapter_range()
        assert not rng_2.is_inter_chapter_range()
        assert not rng_2.is_book()
        assert not rng_2.is_book_range()
        # Test adjoins
        assert rng_1 < rng_2
        assert not rng_1.adjoins(rng_2)
