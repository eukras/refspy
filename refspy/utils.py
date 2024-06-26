import re
from typing import List, Tuple


def string_together(*args) -> str:
    """
    Convert objects to strings and concatenate.
    """
    return "".join([str(arg) for arg in args])


def normalize_spacing(text):
    """
    Turn multiple spaces into single spaces.
    """
    return re.sub("\\s+", " ", text)


def sequential_replace_tuples(text: str, tuples: List[Tuple[str, str]]):
    """
    A sequential replace searches from the end of each previous replacement.
    This is for replacing matches, and ensures they are replaced in the
    same order they are matched. This function takes find-replace strings as
    lists of tuples.
    """
    new_text = ""
    cursor = 0
    for find, replace in tuples:
        next_match = text.find(find, cursor)
        new_text += text[cursor:next_match]
        new_text += replace
        cursor = next_match + len(find)
    new_text += text[cursor:]
    return new_text


def sequential_replace(text: str, find: List[str], replace: List[str]) -> str:
    """
    A sequential replace searches from the end of each previous replacement.
    This is for replacing matches, and ensures they are replaced in the
    same order they are matched. This function takes find-replace strings as
    two separate lists. Unmatched entries will be ignored by zip().
    """
    return sequential_replace_tuples(text, list(zip(find, replace)))
