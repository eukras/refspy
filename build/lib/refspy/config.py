"""Configure libraries and languages."""

from typing import Dict, List

from refspy.language import Language
from refspy.languages.english import ENGLISH
from refspy.libraries.en_US import DC, DC_ORTHODOX, NT, OT
from refspy.library import Library

LIBRARIES: Dict[str, Dict[str, List[Library]]] = {
    "protestant": {"en_US": [OT, NT]},
    "catholic": {"en_US": [OT, DC, NT]},
    "orthodox": {"en_US": [OT, DC, DC_ORTHODOX, NT]},
}
"""A dictionary of available locales for available libraries, used for
shorthand library invocation.

Example:
    ```
    from refspy.libraries.en_US import NT, OT

    LIBRARIES = { "protestant": {"en_US": [OT, NT] } }
    ```
"""

LANGUAGES: Dict[str, Language] = {
    "en": ENGLISH,
}
"""A dictionary of available languages, used for shorthand library invocation.

Language names use the first two chars of locale names, e.g. 'en_US' is 'en'.

Example:
    ```
    from refspy.languages.english import ENGLISH

    LANGUAGES = { "en": ENGLISH }
    ```
"""
