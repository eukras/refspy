"""A Python package for working with biblical references in ordinary text.

See the [README.md](https://github.com/eukras/refspy) for a more accessible
introduction.
"""

from refspy.init import get_canon, get_language, get_formats
from refspy.manager import Manager


def refspy(
        canon_name: str = "protestant", 
        locale_name: str = "en_US",
        include_two_letter_aliases: bool = True,
    ) -> Manager:
    """Create a Manager object to access all common package functions.

    See: `refspy.manager.Manager`

    Args:
        canon_name: A valid key for `refspy.init.get_canon()`
            - `protestant`
            - `catholic` (adds Deuterocanonicals)
            - `orthodox` (adds Anagignoskomena)
        locale_name: An available locale (see the 'librairies' directory)
            (eg. `en_US`, `fr_FR`)
        include_two_letter_aliases: e.g. 'Ge', '1 Jn'.

    Note:
        Libraries and languages can be created outside the package, and
        supplied to the Manager object directly. These can be contributed to
        the library, but the point of the library is to read ordinary text
        using ordinary referencing conventions. This will have to be confirmed
        for each proposed library and language.
    """
    return Manager(
        get_canon(canon_name, locale_name),
        get_language(locale_name[:2]),
        get_formats(locale_name),
        include_two_letter_aliases=include_two_letter_aliases,
    )
