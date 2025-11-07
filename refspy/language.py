"""Data object for language options.

Program strings that vary with the selected language.

Attributes:
    verse_markers: The equivalent of 'v.' and vv.' in English.
    ambiguous_aliases: Book names or abbreviations that are also common words.
    number_prefixes: The equivalent of 'I' and 'First' (etc) in English.
    colon: ':' in English
    comma: ',' in English
    dash: '-' in English
    semicolon: ';' in English
    format_colon: ':' in English
    format_comma: "," in English
    format_dash: "–" in English (EN_DASH)
    format_semicolon: ";" in English
    match_colons: ":." in English
    match_commas: "," in English
    match_dashes: "–-" in ENglish (incl. EN_DASH)
    match_semicolons: ";" in English
    default_link_pattern: see `refspy.manager.Manager.template()`
"""

from pydantic import BaseModel


class Language(BaseModel):
    verse_markers: list[str]
    ambiguous_aliases: list[str]
    number_prefixes: dict[str, list[str]]
    colon: str
    comma: str
    dash: str
    semicolon: str
    format_colon: str
    format_comma: str
    format_dash: str
    format_semicolon: str
    match_colons: str
    match_commas: str
    match_dashes: str
    match_semicolons: str
    default_link_pattern: str
