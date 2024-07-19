"""
Provide general utility functions for the Refspy package.
"""

import re
from typing import Any, List, Tuple

from refspy.number import Number


def parse_number(number_str: str) -> Number:
    """Remove non-digits and return an integer IF it falls between 1 and 999
    inclusive.

    Args:
        number_str: A string expected to contain an integer, among other
            characters.

    Raises:
        ValueError: if no digits in 1..999 range.

    Return:
        None if no digits appear in `number_str` or not in range.
    """
    digits = re.sub(r"\D", "", number_str)
    if digits != "":
        number = int(digits)
        if 1 <= number <= 999:
            return number
    raise ValueError(f"Invalid number string for parse_number: '{number_str}'")


def url_escape(name: str) -> str:
    """Turn a library or book name into a URL escaped string

    Simple URL encode for significant characters:

        * '1 Cor 3:4–5 -> '1%20Cor%203%3A4-5'
    """
    return name.replace(" ", "%20").replace(":", "%3A").replace("–", "-")


def url_param(name: str) -> str:
    """Turn a library or book name into a URL-friendly string.

    Lowercase and no spaces: '1 Cor 3:4-5' -> '1+cor+3.4-5'
    """
    return name.lower().replace(" ", "+").replace(":", ".").replace("–", "-")


def normalize_spacing(text: str) -> str:
    """Replace multiple spaces with single spaces.

    Args:
        text: A string expected to have irregular spacing.
    """
    return re.sub("\\s+", " ", text)


def pluralize(number: int, singular: str, plural: str = "") -> str:
    """
    Super simple pluralization.
    """
    if number == 1:
        return "%d %s" % (number, singular)
    else:
        if plural != "":
            return "%d %s" % (number, plural)
        else:
            return "%d %ss" % (number, singular)


def sequential_replace_tuples(text: str, tuples: List[Tuple[str, str]]):
    """Replace values, searching from the end of each previous replacement.

    This is for replacing matches, and ensures they are replaced in the
    same order they are matched.

    This function takes find-replace strings as a list of tuples. See
    `refspy.utils.sequential_replace`.

    Args:
        text: A string in which matches should be replaces
        tuples: A list of find-replace tuples, in order of appearance.
    """
    new_text = ""
    cursor = 0
    for find, replace in tuples:
        if find and replace:
            next_match = text.find(find, cursor)
            if next_match != -1:
                new_text += text[cursor:next_match]
                new_text += replace
                cursor = next_match + len(find)
    new_text += text[cursor:]
    return new_text


def sequential_replace(text: str, find: List[str], replace: List[str]) -> str:
    """Replace values, searching from the end of each previous replacement.

    This function takes find-replace strings as two separate lists. Unmatched
    entries will be ignored by zip(). See
    `refspy.utils.sequential_replace_tuples`.

    Args:
        text: A string in which matches should be replaces
        find: A list of values to be found, in order of appearance.
        replace: A list of replacement values.
    """
    return sequential_replace_tuples(text, list(zip(find, replace)))


def string_together(*args: Any) -> str:
    """Convert objects to strings and concatenate.

    Args:
        *args: A list of string-convertable values.
    """
    return "".join([str(arg) for arg in args])
