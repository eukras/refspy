"""Data object for language options.

Program strings that vary with the selected language.

Attributes:
    verse_markers: The equivalent of 'v.' and vv.' in English.
    number_prefixes: The equivalent of 'I' and 'First' (etc) in English.
"""

from typing import Dict, List

from pydantic import BaseModel


class Language(BaseModel):
    verse_markers: List[str]
    ambiguous_aliases: List[str]
    number_prefixes: Dict[str, List[str]]
