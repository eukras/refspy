"""A Python package for working with biblical references in ordinary text.

See the [README.md](https://github.com/eukras/refspy) for a more accessible
introduction.
"""

from refspy.init import get_canon, get_language
from refspy.manager import Manager


def refspy(canon_name: str = "protestant", locale_name: str = "en_US") -> Manager:
    """Create a Manager object to access all common package functions.

    Args:
        canon_name: A valid key for the `refspy.config.LIBRARIES` dict
        locale_name: A valid key for the `refspy.config.LANGUAGES` dict
    """
    return Manager(get_canon(canon_name, locale_name), get_language(locale_name[:2]))
