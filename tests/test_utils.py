from context import *

import pytest

from refspy import refspy
from refspy.languages.english import ENGLISH
from refspy.utils import (
    add_space_after_book_number,
    get_unnumbered_book_aliases,
    normalize_spacing,
    parse_number,
    sequential_replace,
    sequential_replace_tuples,
    strip_book_number,
    strip_space_after_book_number,
    url_param,
    url_escape,
)


__ = refspy()

def test_parse_number():
    text = "USD $50"
    assert parse_number(text) == 50


def test_parse_number_raises_value_error():
    text = "My offer is this: nothing."
    with pytest.raises(ValueError):
        assert parse_number(text) == 50


def test_url_param():
    assert url_param("1 Cor 3:4–5") == "1+cor+3.4-5"

def test_url_escape():
    assert url_escape("1 Cor 3:4–5") == "1%20Cor%203%3A4-5"


def test_strip_book_number():
    assert strip_book_number('2 Tim') == 'Tim'
    assert strip_book_number('2Tim') == '2Tim'
    assert strip_book_number('1st') == '1st'


def test_strip_space_after_book_number():
    assert strip_space_after_book_number('2 Tim') == '2Tim'
    assert strip_space_after_book_number('2  Tim') == '2 Tim'
    assert strip_space_after_book_number('2Tim') == '2Tim'
    assert strip_space_after_book_number('1st') == '1st'


def test_add_space_after_book_number():
    """ Remove space between any leading digit and all subsequent text.

    e.g. '2Tim' becomes '2 Tim'.
    """
    unnumbered_book_aliases = get_unnumbered_book_aliases(__.book_aliases)

    assert add_space_after_book_number('2Tim', unnumbered_book_aliases, ENGLISH.number_prefixes) == '2 Tim'
    assert add_space_after_book_number('IITim', unnumbered_book_aliases, ENGLISH.number_prefixes) == '2 Tim'
    assert add_space_after_book_number('2ndTim', unnumbered_book_aliases, ENGLISH.number_prefixes) == '2 Tim'
    assert add_space_after_book_number('SecondTim', unnumbered_book_aliases, ENGLISH.number_prefixes) == '2 Tim'
    assert add_space_after_book_number('2 Tim', unnumbered_book_aliases, ENGLISH.number_prefixes) == '2 Tim'
    assert add_space_after_book_number('II Tim', unnumbered_book_aliases, ENGLISH.number_prefixes) == 'II Tim'
    assert add_space_after_book_number('2nd Tim', unnumbered_book_aliases, ENGLISH.number_prefixes) == '2nd Tim'
    assert add_space_after_book_number('Second Tim', unnumbered_book_aliases, ENGLISH.number_prefixes) == 'Second Tim'


def test_normalize_spacing():
    text = "  a  \t\t b    c  \n\r  d   e   "
    assert normalize_spacing(text) == " a b c d e "


def test_sequential_replace_tuples():
    text = "1 Cor 1; 1 Cor 1:1; 1 Cor 1:1-4"
    tuples = [
        ("1 Cor 1", "XXXXXXX"),
        ("1 Cor 1:1", "YYYYYYYYY"),
        ("1 Cor 1:1-4", "ZZZZZZZZZZZ"),
    ]
    result = sequential_replace_tuples(text, tuples)
    assert result == "XXXXXXX; YYYYYYYYY; ZZZZZZZZZZZ"


def test_sequential_replace():
    text = "1 Cor 1; 1 Cor 1:1; 1 Cor 1:1-4"
    strs = ["1 Cor 1", "1 Cor 1:1", "1 Cor 1:1-4"]
    tags = ["XXXXXXX", "YYYYYYYYY", "ZZZZZZZZZZZ"]
    result = sequential_replace(text, strs, tags)
    assert result == "XXXXXXX; YYYYYYYYY; ZZZZZZZZZZZ"
