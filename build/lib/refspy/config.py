"""Configure libraries and languages."""

from typing import Dict, List

from refspy.language import Language
from refspy.languages.english import ENGLISH
from refspy.languages.spanish import SPANISH
from refspy.libraries.en_US import DC, DC_ORTHODOX, NT, OT
from refspy.libraries.es_ES import DC_es, DC_ORTHODOX_es, NT_es, OT_es
from refspy.library import Library

LIBRARIES: Dict[str, Dict[str, List[Library]]] = {
    "protestant": {"en_US": [OT, NT], "es_ES": [OT_es, NT_es]},
    "catholic": {"en_US": [OT, DC, NT], "es_ES": [OT_es, DC_es, NT_es]},
    "orthodox": {"en_US": [OT, DC, DC_ORTHODOX, NT], "es_ES": [OT_es, DC_es, DC_ORTHODOX_es, NT_es]},
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
