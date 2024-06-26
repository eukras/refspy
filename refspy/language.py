from refspy.languages.english import ENGLISH
from refspy.types.language import Language


# Use the first two chars of locale strings for languages:
LANGUAGES = {
    "en": ENGLISH,
}


def get_language(name: str) -> Language:
    if name in LANGUAGES:
        return LANGUAGES[name]
    else:
        raise ValueError(f"Language '{name}' not found.")
