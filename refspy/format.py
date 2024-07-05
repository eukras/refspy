"""
Data object for reference formatting options.

The Format objects are used by the `refspy.formatter.Formatter` to turn
references into different kinds of strings. Properties are named by their
characters in normal English formatting.

Attributes:
    colon: ':'
    comma: ','
    dash: '-'
    property: 'name'
    semicolon: '; '
    space: ' '

Note:
    This may need to move into the language files.
"""

from pydantic import BaseModel


class Format(BaseModel):
    colon: str
    comma: str
    dash: str
    property: str | None
    semicolon: str
    space: str


ABBREV_FORMAT = Format(
    colon=":", comma=",", dash="–", property="abbrev", semicolon="; ", space=" "
)
PARAM_FORMAT = Format(
    colon=".", comma=",", dash="-", property="abbrev", semicolon="/", space="+"
)
NAME_FORMAT = Format(
    colon=":", comma=",", dash="–", property="name", semicolon="; ", space=" "
)
NUMBER_FORMAT = Format(
    colon=":", comma=",", dash="–", property=None, semicolon="; ", space=" "
)
