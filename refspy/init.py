"""Initialisation helpers for Refspy package."""

from typing import List
from refspy.config import LANGUAGES, LIBRARIES
from refspy.language import Language
from refspy.library import Library


def get_language(language_name: str) -> Language:
    """Lookup key in `refspy.config.LANGUAGES` dict."""
    if language_name in LANGUAGES:
        return LANGUAGES[language_name]
    else:
        raise ValueError(f"Language '{language_name}' not found.")


def get_canon(canon_name: str, locale_name: str) -> List[Library]:
    """Lookup keys in `refspy.config.LIBRARIES` dict."""
    if canon_name in LIBRARIES:
        if locale_name in LIBRARIES[canon_name]:
            return LIBRARIES[canon_name][locale_name]
    raise ValueError(f"Canon '{canon_name}' not found for locale '{locale_name}'.")
