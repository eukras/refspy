"""
English and international reference number formatting:

Example:
    ```
    1:2,4-5;
    ```
"""

from refspy.constants import SPACE
from refspy.models.symbols import Symbols

INTERNATIONAL = Symbols(
    colon=":",
    format_colon=":",
    match_colons=":.",
    comma=",",
    format_comma="," + SPACE,
    match_commas=",",
    dash="–",
    format_dash="–",
    match_dashes="–-",
    semicolon=";",
    format_semicolon=";" + SPACE,
    match_semicolons=";",
)
