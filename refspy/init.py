"""Initialisation helpers for Refspy package."""

from typing import List
from refspy.language import Language
from refspy.library import Library
from refspy.format import Formats

def get_language(language_name: str) -> Language:
    """Dynamically loads language specifities.

    Language names use the first two chars of locale names, e.g. 'en_US' is 'en'.
    """
    if language_name == "en":
        from refspy.languages.english import ENGLISH
        return ENGLISH
    elif language_name == "fr":
        from refspy.languages.french import FRENCH
        return FRENCH
    else:
        raise ValueError(f"Language '{language_name}' not found.")

def get_canon(canon_name: str, locale_name: str) -> List[Library]:
    """Dynamically loads canon

    Args:
        canon_name:
            - 'protestant'
            - 'catholic' (adds Deuterocanonicals)
            - 'orthodox' (adds Anagignoskomena)
        locale_name: An available locale (see the 'librairies' directory)
            (eg. 'en_US', 'fr_FR')
    """
    if locale_name == "en_US":
        from refspy.libraries.en_US import DC, DC_ORTHODOX, NT, OT
    elif locale_name == "fr_FR":
        from refspy.libraries.fr_FR import DC, DC_ORTHODOX, NT, OT
    else:
        raise ValueError(f"Locale '{locale_name}' not available.")
    
    if canon_name == "protestant":
        return [OT, NT]
    elif canon_name == "catholic":
        return [OT, DC, NT]
    elif canon_name == "orthodox":
        return [OT, DC, DC_ORTHODOX, NT]
    else:
        raise ValueError(f"Canon '{canon_name}' not found for locale '{locale_name}'.")

def get_formats(locale_name: str) -> Formats:
    """
    """
    if locale_name == "en_US":
        from refspy.formats.en_US import FORMATS
        return FORMATS
    elif locale_name == "fr_FR":
        from refspy.formats.fr_FR import FORMATS
        return FORMATS
    else:
        raise ValueError(f"Format not found for local '{locale_name}'.")