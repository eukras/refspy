from typing import List
from refspy.library import get_library
from refspy.types.library import Library

CORPUSES = {
    "protestant": ["OT", "NT"],
    "catholic": ["OT", "DC", "NT"],
    "orthodox": ["OT", "DC", "DC_ORTHODOX", "NT"],
}


def get_corpus(name: str, locale: str) -> List[Library]:
    if name in CORPUSES:
        return get_library(name, locale)
    else:
        raise ValueError(f"Corpus '{name}' not found.")
