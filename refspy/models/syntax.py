"""
Data object for reference character separators.

The Symbol object is used in instances of `refspy.language.Language`
to store the different symbol conventions used in the EU countries
and internationally. For example, `1:2,4-5 (INTL) == 1,2.4-5 (EURO)`.

It also stores matching characters that should be considered equivalent when
matching.

Attributes:
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
    match_dashes: "–-" in English (incl. EN_DASH)
    match_semicolons: ";" in English
"""

from pydantic import BaseModel


class Syntax(BaseModel):
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
