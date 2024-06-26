from typing import List
from pydantic import BaseModel

from refspy.types.book import Book


class Library(BaseModel):
    id: int
    name: str
    abbrev: str
    code: str
    books: List[Book]
