from refspy.language import Language


FRENCH = Language(
    verse_markers=["v.", "vv."],
    ambiguous_aliases=[],
    number_prefixes={
        "1": ["Première Lettre à", "Première lettre aux", "Première Épître de", "Premier livre des", "1ere", "I"],
        "2": ["Seconde Lettre à", "Seconde lettre aux", "Seconde Épître de", "Deuxième livre des", "2nd", "II"],
        "3": ["Troisième Lettre à", "Troisième Épître de", "3e", "III"],
        "4": ["Quatrième", "4e", "IV"],
    },
)
