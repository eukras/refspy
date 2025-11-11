"""
Data object for reference formatting options.

The Format objects are used by the `refspy.formatter.Formatter` to turn
references into different kinds of strings. Properties are named by their
characters in normal English formatting. Attributes should contain any
necessary spacing to be added before or after characters.

Attributes:
    colon: ':' in English
    comma: ',' in English
    dash: '-' in English
    semicolon: ';' in English
    book_only: e.g. 'Romans'
    number_only: e.g. '12:16'
    property: 'name' (or None)

Note:
    If book_only is true, number_only is ignored.
"""

from pydantic import BaseModel


class Format(BaseModel):
    colon: str
    comma: str
    dash: str
    semicolon: str
    book_only: bool
    number_only: bool
    property: str | None
