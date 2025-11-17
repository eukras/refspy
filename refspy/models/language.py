"""Data object for language options.

Program strings that vary with the selected language.

Attributes:
    verse_markers: The equivalent of 'v.' and vv.' in English.
    ambiguous_aliases: Book names or abbreviations that are also common words.
    number_prefixes: The equivalent of 'I' and 'First' (etc) in English.
    default_link_pattern: see `refspy.manager.Manager.template()`
    demonstration_text: For generating demo HTML and images
    nt_translation: default BibleGateway translations for New Testament
    ot_translation: default BibleGateway translations for Old Testament
    dc_translation: default BibleGateway translations for Deuterocanonicals
"""

from pydantic import BaseModel

from refspy.models.syntax import Syntax


class Language(BaseModel):
    verse_markers: list[str]
    ambiguous_aliases: list[str]
    number_prefixes: dict[str, list[str]]
    syntax: Syntax
    default_link_pattern: str
    demonstration_text: str
    nt_translation: str
    ot_translation: str
    dc_translation: str
    dc_notes: list[str]
