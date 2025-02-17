"""
Data object for reference formatting options.

The Format objects are used by the `refspy.formatter.Formatter` to turn
references into different kinds of strings. Properties are named by their
characters in normal English formatting.

Attributes:
    book_only: False
    colon: ':'
    comma: ','
    dash: '-'
    number_only: False
    property: 'name'
    semicolon: '; '
    space: ' '

Note:
    If book_only is true, number_only is ignored.
"""

from pydantic import BaseModel


class Format(BaseModel):
    book_only: bool
    colon: str
    comma: str
    dash: str
    number_only: bool
    dash: str
    property: str | None
    semicolon: str
    space: str


NAME_FORMAT = Format(
    colon=":",
    comma=", ",
    dash="–",
    book_only=False,
    number_only=False,
    property="name",
    semicolon="; ",
    space=" ",
)
BOOK_FORMAT = Format(
    colon=":",
    comma=", ",
    dash="–",
    book_only=True,
    number_only=False,
    property="name",
    semicolon="; ",
    space=" ",
)
NUMBER_FORMAT = Format(
    colon=":",
    comma=", ",
    dash="–",
    book_only=False,
    number_only=True,
    property=None,
    semicolon="; ",
    space=" ",
)
ABBREV_NAME_FORMAT = Format(
    colon=":",
    comma=", ",
    dash="–",
    book_only=False,
    number_only=False,
    property="abbrev",
    semicolon="; ",
    space=" ",
)
ABBREV_BOOK_FORMAT = Format(
    colon=":",
    comma=", ",
    dash="–",
    book_only=True,
    number_only=False,
    property="abbrev",
    semicolon="; ",
    space=" ",
)
ABBREV_NUMBER_FORMAT = Format(
    colon=":",
    comma=", ",
    dash="–",
    book_only=False,
    number_only=True,
    property="abbrev",
    semicolon="; ",
    space=" ",
)
