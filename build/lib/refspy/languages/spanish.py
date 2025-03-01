from refspy.language import Language


SPANISH = Language(
    verse_markers=["v.", "vv."],
    ambiguous_aliases=['Es', 'Mi'],
    number_prefixes={
        "1": ["Primero", "1ro", "I", "i"],
        "2": ["Segundo", "2do", "II", "ii"],
        "3": ["Tercero", "3ro", "III", "iii"],
        "4": ["Cuarto", "4to", "IV", "iv"],
    },
)