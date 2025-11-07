from refspy.constants import SPACE
from refspy.language import Language


ENGLISH = Language(
    verse_markers=["v.", "vv."],
    ambiguous_aliases=["Am", "Ho", "Is", "So"],
    number_prefixes={
        "1": ["First Letter to the", "First", "1st", "I"],
        "2": ["Second Letter to the", "Second", "2nd", "II"],
        "3": ["Third Letter to the", "Third", "3rd", "III"],
        "4": ["Fourth Letter to the", "Fourth", "4th", "IV"],
    },
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
    default_link_pattern='<a href="https://www.biblegateway.com/passage/?search={LINK}&version=NRSVA" target="_blank">{ABBREV_NAME}</a>',
)
