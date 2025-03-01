"""Data type for index numbers.

An index number can be used to store a verse in a database using an `UNSIGNED
INT(12)` field.

It is created by multiplying each constituent number (library, book, chapter,
verse) by powers of 1000.

Example:
    `verse(1, 2, 3, 4)` becomes `1002003004`
"""

from typing import Annotated
from annotated_types import Ge, Le  # >=, <=

Index = Annotated[int, Ge(1001001001), Le(999999999999)]
