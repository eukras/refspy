from refspy.types.language import Language

ENGLISH = Language(
    verse_markers=["v.", "vv."],
    number_prefixes={
        "1": ["I", "First"],
        "2": ["II", "Second"],
        "3": ["III", "Third"],
        "4": ["IV", "Fourth"],
    },
)
