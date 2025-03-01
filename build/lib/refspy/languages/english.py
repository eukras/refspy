from refspy.language import Language


ENGLISH = Language(
    verse_markers=["v.", "vv."],
    ambiguous_aliases=['Am', 'Ho', 'Is', 'So'],
    number_prefixes={
        "1": ["First", "1st", "I"],
        "2": ["Second", "2nd", "II"],
        "3": ["Third", "3rd", "III"],
        "4": ["Fourth", "4th", "IV"],
    },
)
