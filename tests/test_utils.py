from context import *

import pytest

from refspy import refspy
from refspy.utils import (
    normalize_spacing,
    parse_number,
    sequential_replace,
    sequential_replace_tuples,
    url_param,
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
    assert url_param("1 Cor") == "1+cor"
    assert url_param("Romans") == "romans"
    assert url_param("1 Cor 3:4-5") == "1+cor+3.4-5"


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
