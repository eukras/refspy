from refspy.constants import NON_BREAKING_SPACE, SPACE
from refspy.language import Language


FRENCH = Language(
    verse_markers=["v.", "vv."],
    ambiguous_aliases=["Est", "Ex", "Ne", "Os", "Si"],
    number_prefixes={
        "1": [
            "Première Lettre à",
            "Première lettre aux",
            "Première Épître de",
            "Premier livre des",
            "1ere",
            "I",
        ],
        "2": [
            "Seconde Lettre à",
            "Seconde lettre aux",
            "Seconde Épître de",
            "Deuxième livre des",
            "2nd",
            "II",
        ],
        "3": ["Troisième Lettre à", "Troisième Épître de", "3e", "III"],
        "4": ["Quatrième", "4e", "IV"],
    },
    colon=",",
    format_colon="," + NON_BREAKING_SPACE,
    match_colons=":,",
    comma=".",
    format_comma="." + SPACE,
    match_commas=".",
    dash="–",
    format_dash="–",
    match_dashes="–-",
    semicolon=";",
    format_semicolon=NON_BREAKING_SPACE + ";" + SPACE,
    match_semicolons=";",
    default_link_pattern='<a href="https://www.biblegateway.com/passage/?search={LINK}&version=SG21" target="_blank">{ABBREV_NAME}</a>',
)
