from typing import List
from pydantic import BaseModel


class Book(BaseModel):
    id: int
    name: str
    abbrev: str
    code: str
    depth: int
    aliases: List[str]
    chapters: int
