"""Data type for Numbers

Library, book, chapter, and verse numbers are integers in the range 1 to 999.
"""

from typing import Annotated
from annotated_types import Ge, Le  # >=, <=

Number = Annotated[int, Ge(1), Le(999)]
