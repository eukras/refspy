from typing import Dict, List

from pydantic import BaseModel


class Language(BaseModel):
    verse_markers: List[str]
    number_prefixes: Dict[str, List[str]]
