import re

import pytest
from context import *

from refspy.indexers import index_book_aliases, index_books
from refspy.languages.english import ENGLISH
from refspy.matcher import (
    CHAPTER_RANGE_CAPTURE,
    CHAPTER_VERSES_CAPTURE,
    COLON,
    DASH,
    LIST,
    NUMBER,
    RANGE,
    RANGE_OR_NUMBER_COMPILED,
    SPACE,
    Matcher,
    infer_abbreviation,
    make_chapter_range,
    make_chapter_verses,
    make_number_ranges,
    match_chapter_range,
    match_chapter_verses,
    match_number_ranges,
)
from refspy.range import range, verse_range
from refspy.reference import (
    book_reference,
    chapter_reference,
    reference,
    verse_reference,
)
from refspy.verse import verse
from tests.data import TEST_LIBRARY

books = index_books([TEST_LIBRARY])
book_aliases = index_book_aliases([TEST_LIBRARY])
matcher = Matcher(books, book_aliases, ENGLISH)


def test_regexp_building_blocks():
    assert re.findall(COLON, ":") == [":"]

    assert re.findall(DASH, "-") == ["-"]
    assert re.findall(DASH, "–") == ["–"]

    assert re.findall(NUMBER, "0") == ["0"]
    assert re.findall(NUMBER, "1") == ["1"]
    assert re.findall(NUMBER, "1000") == ["1000"]  # <-- numbers of any length

    assert re.findall(SPACE, " ") == [" ", ""]
    assert re.findall(SPACE, "\n") == ["\n", ""]
    assert re.findall(SPACE, "\r") == ["\r", ""]
    assert re.findall(SPACE, "\t") == ["\t", ""]

    assert re.findall(RANGE, "1-2") == ["1-2"]
    assert re.findall(RANGE, "0-999") == ["0-999"]
    assert re.findall(RANGE, "1-1000") == ["1-1000"]
    assert re.findall(RANGE, "1-999") == ["1-999"]


def test_number_list_regexp():
    match = re.findall(LIST, "1-3,4:5,7-9")
    assert match == ["1-3,4", "5,7-9"]
    match = re.findall(LIST, "1-3,4,5, 7-9")
    assert match == ["1-3,4,5, 7-9"]
    match = re.findall(LIST, "11-13,14,15, 17-19")
    assert match == ["11-13,14,15, 17-19"]
    match = re.findall(LIST, "111-113,114,115, 117-119")
    assert match == ["111-113,114,115, 117-119"]


def test_number_list_generated_regexp():
    number_list = matcher.build_number_list_regexp()
    match = re.findall(number_list, "Big Book 1:1, 1, 1 Book 2, 3, 4:5")
    assert match == ["1", "1, 1", "1", "2, 3", "4", "5"]
    match = re.findall(number_list, "Big Book 11:11, 12, 1 Book 12, 13, 14:15")
    assert match == ["11", "11, 12", "1", "12, 13", "14", "15"]


def test_range_or_number_regexp():
    match = RANGE_OR_NUMBER_COMPILED.findall("1,2-3, 4,   5-6")
    assert match == ["1", "2-3", "4", "5-6"]
    match = RANGE_OR_NUMBER_COMPILED.findall("11,12-13, 14,   15-16")
    assert match == ["11", "12-13", "14", "15-16"]


def test_chapter_range_regexp():
    match = CHAPTER_RANGE_CAPTURE.search(" 1:2-3:4")
    assert match is not None
    assert match.group(1) == "1"
    assert match.group(2) == "2"
    assert match.group(3) == "3"
    assert match.group(4) == "4"


def test_chapter_verses_regexp():
    match = CHAPTER_VERSES_CAPTURE.search(" 1:2,3-4")
    assert match is not None
    assert match.group(1) == "1"
    assert match.group(2) == "2,3-4"


def test_name_regexp():
    regexp = matcher.build_reference_regexp()
    assert re.escape("Big") + "\\s+" + re.escape("Book") in regexp
    assert re.escape("Small") + "\\s+" + re.escape("Book") in regexp


def test_match_brackets():
    text = "Big Book 1:2-5 (and 34:6 (and 7)) are more interesting than Small Book 3-6."
    matches = matcher.brackets_regexp.findall(text)
    assert len(matches) == 4
    assert matches[0] == "("
    assert matches[1] == "("
    assert matches[2] == ")"
    assert matches[3] == ")"


def test_match_names():
    assert matcher.reference_regexp.findall("Big Book") == [
        ("Big Book", "Big Book", "", "")
    ]
    assert matcher.reference_regexp.findall("Big") == [("Big", "Big", "", "")]
    assert matcher.reference_regexp.findall("Small Book") == [
        ("Small Book", "Small Book", "", "")
    ]
    assert matcher.reference_regexp.findall("Small") == [("Small", "Small", "", "")]


def test_match_names_and_numbers():
    assert matcher.reference_regexp.findall("Big Book 1") == [
        ("Big Book 1", "Big Book", " 1", "")
    ]
    assert matcher.reference_regexp.findall("Big Book 1-2") == [
        ("Big Book 1-2", "Big Book", " 1-2", "")
    ]
    assert matcher.reference_regexp.findall("Big Book 1-2,4,6") == [
        ("Big Book 1-2,4,6", "Big Book", " 1-2,4,6", "")
    ]
    assert matcher.reference_regexp.findall("Big Book 1-2,4,6") == [
        ("Big Book 1-2,4,6", "Big Book", " 1-2,4,6", "")
    ]


def test_verse_lists_with_abbreviations():
    assert matcher.reference_regexp.findall("Big 1:1") == [
        ("Big 1:1", "Big", " 1:1", "")
    ]
    assert matcher.reference_regexp.findall("Big 1:1, 2") == [
        ("Big 1:1, 2", "Big", " 1:1, 2", "")
    ]
    assert matcher.reference_regexp.findall("Bg 1:1, 2") == [
        ("Bg 1:1, 2", "Bg", " 1:1, 2", "")
    ]


def test_malformed_refs():
    matches = match_number_ranges("1-2,4-3")
    assert matches[0] == "1-2"
    assert matches[1] == "4-3"


def test_comma_separation():
    assert matcher.reference_regexp.findall("Big Book 1:55, 66, 77") == [
        ("Big Book 1:55, 66, 77", "Big Book", " 1:55, 66, 77", "")
    ]


def test_negative_lookaheads():
    matches = matcher.reference_regexp.findall("Big Book 1:1, 2, 1 Book 4")
    #                                                    ^^^^ Negative lookaheads
    assert len(matches) == 2
    assert matches[0] == ("Big Book 1:1, 2", "Big Book", " 1:1, 2", "")
    assert matches[1] == ("1 Book 4", "1 Book", " 4", "")


def test_match_names_in_context():
    text = "Big Book 1:2-5 and 34:6,7 are more interesting than Small Book 3-6."
    matches = matcher.reference_regexp.findall(text)
    assert len(matches) == 3
    assert matches[0] == ("Big Book 1:2-5", "Big Book", " 1:2-5", "")
    assert matches[1] == ("", "", "", "34:6,7")
    assert matches[2] == ("Small Book 3-6", "Small Book", " 3-6", "")


def test_match_number_ranges_numeric():
    last_range = verse_range(1, 1, 1, 1)
    matches = match_number_ranges("1,4-5,7–8, 9")
    reference = make_number_ranges(last_range, matches)
    assert reference is not None
    assert reference.ranges[0] == range(verse(1, 1, 1, 1), verse(1, 1, 1, 1))
    assert reference.ranges[1] == range(verse(1, 1, 1, 4), verse(1, 1, 1, 5))
    assert reference.ranges[2] == range(verse(1, 1, 1, 7), verse(1, 1, 1, 8))
    assert reference.ranges[3] == range(verse(1, 1, 1, 9), verse(1, 1, 1, 9))


def test_match_number_ranges_prefixed_v():
    last_range = verse_range(1, 1, 1, 1)
    matches = match_number_ranges("v.1,4-5")
    assert matches is not None
    reference = make_number_ranges(last_range, matches)
    assert reference is not None
    assert reference.ranges[0] == range(verse(1, 1, 1, 1), verse(1, 1, 1, 1))
    assert reference.ranges[1] == range(verse(1, 1, 1, 4), verse(1, 1, 1, 5))


def test_match_number_ranges_prefixed_vv():
    last_range = verse_range(1, 1, 1, 1)
    matches = match_number_ranges("vv.1,4-5")
    assert matches is not None
    reference = make_number_ranges(last_range, matches)
    assert reference is not None
    assert reference.ranges[0] == range(verse(1, 1, 1, 1), verse(1, 1, 1, 1))
    assert reference.ranges[1] == range(verse(1, 1, 1, 4), verse(1, 1, 1, 5))


def test_match_chapter_range():
    last_range = verse_range(1, 1, 1, 1)
    matches = match_chapter_range("1:4-2:3")
    assert matches is not None
    reference = make_chapter_range(last_range, matches)
    assert reference is not None
    assert reference.ranges == [range(verse(1, 1, 1, 4), verse(1, 1, 2, 3))]
    matches = match_chapter_range("1:4–2:3")
    assert matches is not None
    reference = make_chapter_range(last_range, matches)
    assert reference is not None
    assert reference.ranges == [range(verse(1, 1, 1, 4), verse(1, 1, 2, 3))]


def test_match_chapter_verses():
    last_range = verse_range(1, 1, 1, 1)
    matches = match_chapter_verses("1:4,8-9")
    assert matches is not None
    reference = make_chapter_verses(last_range, matches)
    assert reference is not None
    assert reference.ranges == [
        range(verse(1, 1, 1, 4), verse(1, 1, 1, 4)),
        range(verse(1, 1, 1, 8), verse(1, 1, 1, 9)),
    ]


def test_find_references():
    sample_text = "Big Book 1:2-5 and 34:6,7 are more interesting than Small Book 3-6."
    __ = matcher.generate_references(sample_text)
    text, ref = next(__)
    assert text == "Big Book 1:2-5"
    assert ref == reference(range(verse(1, 2, 1, 2), verse(1, 2, 1, 5)))
    text, ref = next(__)
    assert text == "34:6,7"
    assert ref == reference(
        range(verse(1, 2, 34, 6), verse(1, 2, 34, 6)),
        range(verse(1, 2, 34, 7), verse(1, 2, 34, 7)),
    )
    text, ref = next(__)
    assert text == "Small Book 3-6"
    assert ref == reference(range(verse(1, 3, 1, 3), verse(1, 3, 1, 6)))
    with pytest.raises(StopIteration):
        assert next(__) is None


def test_vv_references():
    sample_text = "Big Book 5 is useful, esp. vv.3-4 and v.8."
    __ = matcher.generate_references(sample_text)
    text, ref = next(__)
    assert text == "Big Book 5"
    assert ref == reference(range(verse(1, 2, 5, 1), verse(1, 2, 5, 999)))
    text, ref = next(__)
    assert text == "vv.3-4"
    assert ref == reference(range(verse(1, 2, 5, 3), verse(1, 2, 5, 4)))
    text, ref = next(__)
    assert text == "v.8"
    assert ref == reference(range(verse(1, 2, 5, 8), verse(1, 2, 5, 8)))
    with pytest.raises(StopIteration):
        assert next(__) is None


def test_include_books():
    sample_text = "Big Book or Small Book?"
    __ = matcher.generate_references(sample_text, include_books=True)
    text, ref = next(__)
    assert text == "Big Book"
    assert ref == book_reference(1, 2)
    text, ref = next(__)
    assert text == "Small Book"
    assert ref == book_reference(1, 3)
    # ^^ The final reference should still be to Big Book.
    with pytest.raises(StopIteration):
        assert next(__) is None


def test_single_parentheses():
    sample_text = "Big Book 1:2-5 (cf. Small Book 34) is more interesting than vv.3-6."
    # ^^ The final reference should still be to Big Book (book ID 2).
    __ = matcher.generate_references(sample_text)
    text, ref = next(__)
    assert text == "Big Book 1:2-5"
    assert ref == reference(range(verse(1, 2, 1, 2), verse(1, 2, 1, 5)))
    text, ref = next(__)
    assert text == "Small Book 34"
    assert ref == reference(range(verse(1, 3, 1, 34), verse(1, 3, 1, 34)))
    text, ref = next(__)
    assert text == "vv.3-6"
    assert ref == reference(range(verse(1, 2, 1, 3), verse(1, 2, 1, 6)))
    with pytest.raises(StopIteration):
        assert next(__) is None


def test_number_prefixes_1():
    sample_text = "1 Book 1:1, First Book 1:1, 1st Book 1:1, I Book 1:1"
    first_reference = verse_reference(1, 4, 1, 1)
    __ = matcher.generate_references(sample_text)
    text, ref = next(__)
    assert text == "1 Book 1:1"
    assert ref == first_reference
    text, ref = next(__)
    assert text == "First Book 1:1"
    assert ref == first_reference
    text, ref = next(__)
    assert text == "1st Book 1:1"
    assert ref == first_reference
    text, ref = next(__)
    assert text == "I Book 1:1"
    assert ref == first_reference
    # No more
    with pytest.raises(StopIteration):
        assert next(__) is None


def test_number_prefixes_2():
    sample_text = "2 Book 1:1, Second Book 1:1, 2nd Book 1:1, II Book 1:1"
    first_reference = verse_reference(1, 5, 1, 1)
    __ = matcher.generate_references(sample_text)
    text, ref = next(__)
    assert text == "2 Book 1:1"
    assert ref == first_reference
    text, ref = next(__)
    assert text == "Second Book 1:1"
    assert ref == first_reference
    text, ref = next(__)
    assert text == "2nd Book 1:1"
    assert ref == first_reference
    text, ref = next(__)
    assert text == "II Book 1:1"
    assert ref == first_reference
    # No more
    with pytest.raises(StopIteration):
        assert next(__) is None


def test_number_prefixes_3():
    sample_text = "3 Book 1, Third Book 1, 3rd Book 1, III Book 1"
    first_reference = verse_reference(1, 6, 1, 1)
    __ = matcher.generate_references(sample_text)
    text, ref = next(__)
    assert text == "3 Book 1"
    assert ref == first_reference
    text, ref = next(__)
    assert text == "Third Book 1"
    assert ref == first_reference
    text, ref = next(__)
    assert text == "3rd Book 1"
    assert ref == first_reference
    text, ref = next(__)
    assert text == "III Book 1"
    assert ref == first_reference
    # No more
    with pytest.raises(StopIteration):
        assert next(__) is None


def test_book_number_spacing_is_optional():
    sample_text = "1Book 1:1"
    first_reference = verse_reference(1, 4, 1, 1)
    __ = matcher.generate_references(sample_text)
    text, ref = next(__)
    assert text == "1Book 1:1"
    assert ref == first_reference
    with pytest.raises(StopIteration):
        assert next(__) is None


def test_line_wrapping():
    text = """
        This is a wrapped reference to 1 
        Book 5.
        """
    __ = matcher.generate_references(text)
    text, ref = next(__)
    assert (
        text
        == """1 
        Book 5"""
    )
    assert ref == chapter_reference(1, 4, 5)


def test_nonnumeric_prefixes():
    text = "1stBook 6:6 IBook 6:6"
    __ = matcher.generate_references(text)
    text, ref = next(__)
    assert text == "1stBook 6:6"
    assert ref == verse_reference(1, 4, 6, 6)
    text, ref = next(__)
    assert text == "IBook 6:6"
    assert ref == verse_reference(1, 4, 6, 6)


def test_infer_abbreviation():
    assert infer_abbreviation("124", "24") == "124"
    assert infer_abbreviation("12", "4") == "14"
    assert infer_abbreviation("24", "23") is None
    assert infer_abbreviation("4", "3") is None


def test_periods_on_abbreviations_and_aliases():
    text = "Sm. 1; Bg.1:1"
    __ = matcher.generate_references(text)
    text, ref = next(__)
    assert text == "Sm. 1"
    assert ref == verse_reference(1, 3, 1, 1)
    text, ref = next(__)
    assert text == "Bg.1:1"
    assert ref == verse_reference(1, 2, 1, 1)


def test_aliases_dont_match_the_start_of_words():
    text = "Smash and grab"
    #       ^^ Start of 'Sm' (Small)
    __ = matcher.generate_references(text, include_books=True, include_nones=True)
    with pytest.raises(StopIteration):
        text, ref = next(__)
