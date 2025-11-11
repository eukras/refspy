from refspy.models.language import Language
from refspy.syntax.european import EUROPEAN


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
    syntax=EUROPEAN,
    default_link_pattern='<a href="https://www.biblegateway.com/passage/?search={LINK}&version=SG21" target="_blank">{ABBREV_NAME}</a>',
    demonstration_text="""
Lorsque quelqu'un écrit une référence biblique, on peut lire Rm 12:1.6-17, 2
Co. 1, 2–3,4, ou bien Philémon 2-3. Elles sont coupées entre deux lignes, elles
utilisent les espaces de façon décousue, deux-points et virgule indifféremment,
les abréviations sont marquées d'un point (ou non), et les virgules sont
utilisées à la fois entre et dans les références. Elles sont parfois
malformées, par exemple Mt 1, 10000 ou 1,3-2, et font parfois l'utilisation de
numéros abrégés : Ps 119, 122-24. Il peut s'agir de références à des livres
deutérocanoniques (DC), comme Sg 7:21-30 ou 2 M 7, ou à des livres
anagignoskomena (DCO), comme 1 Esdras 4:35-40. Le titre d'un livre, par exemple
la Seconde lettre aux Corinthiens, sert de contexte aux références suivantes :
5, 21 ou vv. 25, 37-38. Nous souhaitons correspondre à l'Évangile de Jean, mais
pas à celui de Jean Smith dans ces cas-là. Si la Lettre aux Romains est citée
(puis que l'on ajoute entre parenthèses une référence à 2Co 3, 5-8), la
référence suivante, 12, 16, renverra encore à l'Épître aux Romains.
L'utilisation des lettres pour désigner des fragments de versets, comme dans II
Co 5, 30a-40d, n'est pas systématique, elles sont donc ignorées. Les
abréviations de livre qui sont aussi des noms communs seront ignorés, sauf dans
une référence, par exemple Os 3, 2, mais pas Os.
    """.strip(),
    nt_translation="SG21;SBLGNT",
    ot_translation="SG21;WLC",
    dc_translation="SG21;VULGATE",
)
