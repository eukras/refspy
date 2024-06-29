from typing import List

from refspy.language import Language
from refspy.languages.english import ENGLISH
from refspy.libraries.en_US import DC, DC_ORTHODOX, NT, OT
from refspy.library import Library


LIBRARIES = {
    "protestant": {"en_US": [OT, NT]},
    "catholic": {"en_US": [OT, DC, NT]},
    "orthodox": {"en_US": [OT, DC, DC_ORTHODOX, NT]},
}


def get_libraries(name: str, locale: str) -> List[Library]:
    if name in LIBRARIES:
        return get_library(name, locale)
    else:
        raise ValueError(f"Corpus '{name}' not found.")


def get_library(name: str, locale: str) -> List[Library]:
    if name in LIBRARIES:
        if locale in LIBRARIES[name]:
            return LIBRARIES[name][locale]
    raise ValueError(f"Library '{name}' not found for locale '{locale}'.")


# Use the first two chars of locale strings for languages:
LANGUAGES = {
    "en": ENGLISH,
}


def get_language(name: str) -> Language:
    if name in LANGUAGES:
        return LANGUAGES[name]
    else:
        raise ValueError(f"Language '{name}' not found.")
