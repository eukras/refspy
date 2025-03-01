"""Configure libraries and languages."""

from typing import Dict, List

from refspy.language import Language
from refspy.languages.english import ENGLISH
from refspy.languages.spanish import SPANISH
from refspy.libraries.en_US import DC as DC_en_US, DC_ORTHODOX as DC_ORTHODOX_en_US, NT as NT_en_US, OT as OT_en_US
from refspy.libraries.es_ES import DC as DC_es_ES, DC_ORTHODOX as DC_ORTHODOX_es_ES, NT as NT_es_ES, OT as OT_es_ES
from refspy.library import Library

LIBRARIES: Dict[str, Dict[str, List[Library]]] = {
    "protestant": {
        "en_US": [OT_en_US, NT_en_US],
        "es_ES": [OT_es_ES, NT_es_ES]
    },
    "catholic": {
        "en_US": [OT_en_US, DC_en_US, NT_en_US],
        "es_ES": [OT_es_ES, DC_es_ES, NT_es_ES]
    },
    "orthodox": {
        "en_US": [OT_en_US, DC_en_US, DC_ORTHODOX_en_US, NT_en_US],
        "es_ES": [OT_es_ES, DC_es_ES, DC_ORTHODOX_es_ES, NT_es_ES]
    },
}
"""A dictionary of available locales for available libraries, used for
shorthand library invocation.

TODO: Allow a single library to be loaded without processing all of them in LIBRARIES. 

Example:
    ```
    from refspy.libraries.en_US import NT, OT

    LIBRARIES = { "protestant": {"en_US": [OT, NT] } }
    ```
"""

LANGUAGES: Dict[str, Language] = {
    "en": ENGLISH,
    "es": SPANISH,
}
"""A dictionary of available languages, used for shorthand library invocation.

Language names use the first two chars of locale names, e.g. 'en_US' is 'en'.

Example:
    ```
    from refspy.languages.english import ENGLISH

    LANGUAGES = { "en": ENGLISH }
    ```
"""
