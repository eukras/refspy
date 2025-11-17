from refspy.models.language import Language
from refspy.syntax.international import INTERNATIONAL


ENGLISH = Language(
    verse_markers=["v.", "vv."],
    ambiguous_aliases=["Am", "Ho", "Is", "So"],
    number_prefixes={
        "1": ["First Letter to the", "First", "1st", "I"],
        "2": ["Second Letter to the", "Second", "2nd", "II"],
        "3": ["Third Letter to the", "Third", "3rd", "III"],
        "4": ["Fourth Letter to the", "Fourth", "4th", "IV"],
    },
    syntax=INTERNATIONAL,
    default_link_pattern='<a href="https://www.biblegateway.com/passage/?search={LINK}&version=NRSVA" target="_blank">{ABBREV_NAME}</a>',
    demonstration_text="""
Human-written Bible references look like Rom 12.1-2, 9-12, 2 Cor. 4:16-5:5,
or Philemon 4-7. They wrap lines, use spaces inconsistently, use colons and
periods interchangeably, indicate abbreviations with periods (or not), and
have commas both between and within references. They are sometimes
malformed, like Mt 1.10000 or 1:3-2, but might also use number
abbreviations like Ps 119:122-24. They might refer to Deuterocanonical
books (DC), like Wis 7:21-30 or 2 Macc 7, or Anagignoskomena (DCO), like 1
Esdras 4:35-40. A book name, like Second Corinthians, may provide context
for references that follow, such as 5:11-15 or vv.16-21. We want to match,
say, 'John' but not match 'John Smith' in these cases. If we cite Romans
(but then add a reference to 2ndCo 5:11-21 in parentheses), a subsequent
reference like 12:9-21 should still be to Romans. Using letters for partial
verses, as in II Cor 5:10a-15d, has no consistent meaning, so the letters
are ignored. Book aliases that are common words will be ignored except in
references, e.g. Am 4:1, but not Am.
    """.strip(),
    nt_translation="NRSVUE;SBLGNT",
    ot_translation="NRSVUE;WLC",
    dc_translation="NRSVUE;VULGATE",
    dc_notes=[],
)
