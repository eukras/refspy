"""Configure libraries and languages.

Note: TODO: Don't initialise all libraries every time, only on demand.
"""

from refspy.models.language import Language
from refspy.models.library import Library
from refspy.models.syntax import Syntax, syntax_label

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

from refspy.syntax.european import EUROPEAN
from refspy.syntax.international import INTERNATIONAL

LIBRARIES: dict[str, dict[str, list[Library]]] = {
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

LANGUAGE_OPTIONS: list[tuple[str, str, str]] = [
    ("en_US", "English", "intl"),
    ("fr_FR", "French", "euro"),
]
"""
Default language options; could be used in forms and interfaces.
"""

LANGUAGES: dict[str, Language] = {"en": ENGLISH, "fr": FRENCH}
"""A dictionary of available languages in the present version of refspy.

Language names use the first two chars of locale names, e.g. 'en_US' is 'en'.

Example:
    ```
    from refspy.languages.english import ENGLISH

    LANGUAGES = { "en": ENGLISH }
    ```
"""

SYNTAX_OPTIONS: list[tuple[str, str]] = [
    (INTERNATIONAL.abbrev, syntax_label(INTERNATIONAL)),
    (EUROPEAN.abbrev, syntax_label(EUROPEAN)),
]
"""
Default syntax options; could be used in forms and interfaces.
"""

SYNTAX: dict[str, Syntax] = {"euro": EUROPEAN, "intl": INTERNATIONAL}
"""A dictionary of available syntaxes in the present version of refspy.
"""
