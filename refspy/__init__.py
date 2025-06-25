"""A Python package for working with biblical references in ordinary text.

See the [README.md](https://github.com/eukras/refspy) for a more accessible
introduction.
"""

from refspy.init import get_canon, get_language
from refspy.manager import Manager


def refspy(
    canon_name: str = "protestant",
    locale_name: str = "en_US",
    include_two_letter_aliases: bool = True,
) -> Manager:
    """Create a Manager object to access all common package functions.

    See: `refspy.manager.Manager`

    Args:
        canon_name: A valid key for the `refspy.config.LIBRARIES` dict (3)
            - `protestant`
            - `catholic` (adds Deuterocanonicals)
            - `orthodox` (adds Anagignoskomena)
        locale_name: A valid key for the `refspy.config.LANGUAGES` dict (1).
            - `en_US`
        include_two_letter_aliases: e.g. 'Ge', '1 Jn'.

    Note:
        Libraries and languages can be created outside the package, and
        supplied to the Manager object directly. These can be contributed to
        the library, but the point of the library is to read ordinary text
        using ordinary referencing conventions. This will have to be confirmed
        for each proposed library and language.

    To Do:
        Load languages and libraries only on demand when there are more of them.
    """
    return Manager(
        get_canon(canon_name, locale_name),
        get_language(locale_name[:2]),
        include_two_letter_aliases=include_two_letter_aliases,
    )
