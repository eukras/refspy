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
CODE_FORMAT = Format(
    colon=".", comma=",", dash="-", property="code", semicolon="/", space="+"
)
NAME_FORMAT = Format(
    colon=":", comma=",", dash="–", property="name", semicolon="; ", space=" "
)
NUMBER_FORMAT = Format(
    colon=":", comma=",", dash="–", property=None, semicolon="; ", space=" "
)
