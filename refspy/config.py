"""Configure libraries and languages.

Note: TODO: Don't initialise all libraries every time, only on demand.
"""

from typing import Dict, List

from refspy.language import Language
from refspy.languages.english import ENGLISH
from refspy.languages.french import FRENCH
from refspy.libraries.en_US import (
    DC as EN_DC,
    DC_ORTHODOX as EN_DC_ORTHODOX,
    NT as EN_NT,
    OT as EN_OT,
)
from refspy.libraries.fr_FR import (
    DC as FR_DC,
    DC_ORTHODOX as FR_DC_ORTHODOX,
    NT as FR_NT,
    OT as FR_OT,
)
from refspy.library import Library

LIBRARIES: Dict[str, Dict[str, List[Library]]] = {
    "protestant": {
        "en_US": [EN_OT, EN_NT],
        "fr_FR": [FR_OT, FR_NT],
    },
    "catholic": {
        "en_US": [EN_OT, EN_DC, EN_NT],
        "fr_FR": [FR_OT, FR_DC, FR_NT],
    },
    "orthodox": {
        "en_US": [EN_OT, EN_DC, EN_DC_ORTHODOX, EN_NT],
        "fr_FR": [FR_OT, FR_DC, FR_DC_ORTHODOX, FR_NT],
    },
}
"""A dictionary of available locales for available libraries, used for
shorthand library invocation.

Example:
    ```
    from refspy.libraries.en_US import NT, OT

    LIBRARIES = { "protestant": {"en_US": [OT, NT] } }
    ```
"""

LANGUAGES: Dict[str, Language] = {"en": ENGLISH, "fr": FRENCH}
"""A dictionary of available languages, used for shorthand library invocation.

Language names use the first two chars of locale names, e.g. 'en_US' is 'en'.

Example:
    ```
    from refspy.languages.english import ENGLISH

    LANGUAGES = { "en": ENGLISH }
    ```
"""
