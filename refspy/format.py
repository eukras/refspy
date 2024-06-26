from refspy.types.format import Format


ABBREV_FORMAT = Format(
    colon=":", comma=",", dash="–", property="abbrev", semicolon="; ", space=" "
)
CODE_FORMAT = Format(
    colon=".", comma=",", dash="-", property="code", semicolon="/", space="+"
)
NAME_FORMAT = Format(
    colon=":", comma=",", dash="–", property="name", semicolon="; ", space=" "
)
NUMBER_FORMAT = Format(
    colon=":", comma=",", dash="–", property=None, semicolon="; ", space=" "
)
