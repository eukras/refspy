"""
European reference number formatting:

Example:
    ```
    1,2.4-5;
    ```
"""

from refspy.constants import NON_BREAKING_SPACE, SPACE
from refspy.models.syntax import Syntax

EUROPEAN = Syntax(
    name="European",
    abbrev="euro",
    colon=",",
    format_colon="," + NON_BREAKING_SPACE,
    match_colons=":,",
    comma=".",
    format_comma="." + SPACE,
    match_commas=".",
    dash="-",
    format_dash="–",
    match_dashes="–-",
    semicolon=";",
    format_semicolon=NON_BREAKING_SPACE + ";" + SPACE,
    match_semicolons=";",
)
