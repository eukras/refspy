from pydantic import BaseModel


class Format(BaseModel):
    colon: str
    comma: str
    dash: str
    property: str | None
    semicolon: str
    space: str
