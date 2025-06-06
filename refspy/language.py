"""Data object for language options.

Program strings that vary with the selected language.

Attributes:
    verse_markers: The equivalent of 'v.' and vv.' in English.
    ambiguous_aliases: Book names or abbreviations that are also common words.
    number_prefixes: The equivalent of 'I' and 'First' (etc) in English.
    name_format: object for formatting book name and number references
    book_format: object for formatting book name references
    number_format: object for formatting number references
    abbrev_name_format: object for formatting abbreviated book name plus number references
    abbrev_book_format: object for formatting abbreviated book name references
    abbrev_number_format: object for formatting abbreviated number references
"""

from typing import Dict, List

from pydantic import BaseModel

from refspy.format import Format


class Language(BaseModel):
    verse_markers: List[str]
    ambiguous_aliases: List[str]
    number_prefixes: Dict[str, List[str]]
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
