from refspy.book import Book
from refspy.library import Library

# See README.md for Library ID numbers
# English language libraries follow SBL style guide for books and
# abbreviations.

OT = Library(
    id=200,
    name="Old Testament",
    abbrev="OT",
    books=[
        Book(
            id=1,
            name="Genesis",
            abbrev="Gen",
            aliases=[],
            chapters=50,
        ),
        Book(
            id=2,
            name="Exodus",
            abbrev="Exod",
            aliases=["Ex"],
            chapters=40,
        ),
        Book(
            id=3,
            name="Leviticus",
            abbrev="Lev",
            aliases=[],
            chapters=27,
        ),
        Book(
            id=4,
            name="Numbers",
            abbrev="Num",
            aliases=[],
            chapters=36,
        ),
        Book(
            id=5,
            name="Deuteronomy",
            abbrev="Deut",
            aliases=[],
            chapters=34,
        ),
        Book(
            id=6,
            name="Joshua",
            abbrev="Josh",
            aliases=[],
            chapters=24,
        ),
        Book(
            id=7,
            name="Judges",
            abbrev="Judg",
            aliases=["Jdg"],
            chapters=21,
        ),
        Book(
            id=8,
            name="Ruth",
            abbrev="Ruth",
            aliases=[],
            chapters=4,
        ),
        Book(
            id=9,
            name="1 Samuel",
            abbrev="1 Sam",
            aliases=[],
            chapters=31,
        ),
        Book(
            id=10,
            name="2 Samuel",
            abbrev="2 Sam",
            aliases=[],
            chapters=24,
        ),
        Book(
            id=11,
            name="1 Kings",
            abbrev="1 Kgs",
            aliases=["1 Ki"],
            chapters=22,
        ),
        Book(
            id=12,
            name="2 Kings",
            abbrev="2 Kgs",
            aliases=["2 Ki"],
            chapters=22,
        ),
        Book(
            id=13,
            name="1 Chronicles",
            abbrev="1 Chr",
            aliases=[],
            chapters=29,
        ),
        Book(
            id=14,
            name="2 Chronicles",
            abbrev="2 Chr",
            aliases=[],
            chapters=36,
        ),
        Book(
            id=15,
            name="Ezra",
            abbrev="Ezra",
            aliases=[],
            chapters=10,
        ),
        Book(
            id=16,
            name="Nehemiah",
            abbrev="Neh",
            aliases=[],
            chapters=13,
        ),
        Book(
            id=17,
            name="Esther",
            abbrev="Esth",
            aliases=[],
            chapters=10,
        ),
        Book(
            id=18,
            name="Job",
            abbrev="Job",
            aliases=[],
            chapters=42,
        ),
        Book(
            id=19,
            name="Psalm",
            abbrev="Ps",
            aliases=[],
            chapters=150,
        ),
        Book(
            id=20,
            name="Proverbs",
            abbrev="Prov",
            aliases=[],
            chapters=31,
        ),
        Book(
            id=21,
            name="Ecclesiastes",
            abbrev="Eccl",
            aliases=["Qoheleth", "Qoh", "Ecc"],
            chapters=12,
        ),
        Book(
            id=22,
            name="Song of Solomon",
            abbrev="Song",
            aliases=["Canticles", "Cant"],
            chapters=8,
        ),
        Book(
            id=23,
            name="Isaiah",
            abbrev="Isa",
            aliases=[],
            chapters=66,
        ),
        Book(
            id=24,
            name="Jeremiah",
            abbrev="Jer",
            aliases=[],
            chapters=52,
        ),
        Book(
            id=25,
            name="Lamentations",
            abbrev="Lam",
            aliases=[],
            chapters=5,
        ),
        Book(
            id=26,
            name="Ezekiel",
            abbrev="Ezek",
            aliases=[],
            chapters=48,
        ),
        Book(
            id=27,
            name="Daniel",
            abbrev="Dan",
            aliases=[],
            chapters=12,
        ),
        Book(
            id=28,
            name="Hosea",
            abbrev="Hos",
            aliases=[],
            chapters=14,
        ),
        Book(
            id=29,
            name="Joel",
            abbrev="Joel",
            aliases=[],
            chapters=3,
        ),
        Book(
            id=30,
            name="Amos",
            abbrev="Amos",
            aliases=[],
            chapters=9,
        ),
        Book(
            id=31,
            name="Obadiah",
            abbrev="Obad",
            aliases=[],
            chapters=1,
        ),
        Book(
            id=32,
            name="Jonah",
            abbrev="Jonah",
            aliases=["Jon"],
            chapters=4,
        ),
        Book(
            id=33,
            name="Micah",
            abbrev="Mic",
            aliases=[],
            chapters=7,
        ),
        Book(
            id=34,
            name="Nahum",
            abbrev="Nah",
            aliases=[],
            chapters=3,
        ),
        Book(
            id=35,
            name="Habbakuk",
            abbrev="Hab",
            aliases=[],
            chapters=3,
        ),
        Book(
            id=36,
            name="Zephaniah",
            abbrev="Zeph",
            aliases=[],
            chapters=3,
        ),
        Book(
            id=37,
            name="Haggai",
            abbrev="Hag",
            aliases=[],
            chapters=2,
        ),
        Book(
            id=38,
            name="Zechariah",
            abbrev="Zech",
            aliases=[],
            chapters=14,
        ),
        Book(
            id=39,
            name="Malachi",
            abbrev="Mal",
            aliases=[],
            chapters=4,
        ),
    ],
)

DC = Library(
    id=210,
    name="Deuterocanonical",
    abbrev="DC",
    books=[
        Book(
            id=1,
            name="Tobit",
            abbrev="Tob",
            aliases=[],
            chapters=14,
        ),
        Book(
            id=2,
            name="Judith",
            abbrev="Jdt",
            aliases=[],
            chapters=16,
        ),
        Book(
            id=3,
            name="Additions to Esther",
            abbrev="Add Esth",
            aliases=[],
            chapters=7,
            # TODO: Offsets: 11..16; or handle 'Greek Esther' (10 chapters).
        ),
        Book(
            id=4,
            name="Wisdom of Solomon",
            abbrev="Wis",
            aliases=[],
            chapters=19,
        ),
        Book(
            id=5,
            name="Sirach",
            abbrev="Sir",
            aliases=["Ecclesiasticus", "Eccles"],
            chapters=51,
        ),
        Book(
            id=6,
            name="Baruch",
            abbrev="Bar",
            aliases=[],
            chapters=6,
        ),
        Book(
            id=7,
            name="Epistle of Jeremiah",
            abbrev="Ep Jer",
            aliases=["Letter of Jeremiah"],
            chapters=1,
        ),
        Book(
            id=8,
            name="Additions to Daniel",
            abbrev="Add Dan",
            aliases=[],
            chapters=1,
        ),
        Book(
            id=9,
            name="Prayer of Azariah",
            abbrev="Pr Azar",
            aliases=[],
            chapters=1,
        ),
        Book(
            id=10,
            name="Song of the Three Young Men",
            abbrev="Sg Three",
            aliases=[],
            chapters=1,
        ),
        Book(
            id=11,
            name="Susannah",
            abbrev="Sus",
            aliases=[],
            chapters=1,
        ),
        Book(
            id=12,
            name="Bel and the Dragon",
            abbrev="Bel",
            aliases=[],
            chapters=1,
        ),
        Book(
            id=13,
            name="1 Maccabees",
            abbrev="1 Macc",
            aliases=[],
            chapters=16,
        ),
        Book(
            id=14,
            name="2 Maccabees",
            abbrev="2 Macc",
            aliases=[],
            chapters=15,
        ),
    ],
)
DC_ORTHODOX = Library(
    id=220,
    name="Deuterocanonical (Orthodox)",
    abbrev="DCO",
    books=[
        Book(
            id=1,
            name="1 Esdras",
            abbrev="1 Esd",
            aliases=[],
            chapters=9,
        ),
        Book(
            id=2,
            name="Prayer of Manesseh",
            abbrev="Pr Man",
            aliases=[],
            chapters=1,
        ),
        Book(
            id=3,
            name="Psalm 151",
            abbrev="Ps 151",
            aliases=[],
            chapters=1,
        ),
        Book(
            id=4,
            name="3 Maccabees",
            abbrev="3 Macc",
            aliases=[],
            chapters=7,
        ),
        Book(
            id=5,
            name="2 Esdras",
            abbrev="2 Esd",
            aliases=[],
            chapters=16,
        ),
        Book(
            id=6,
            name="4 Maccabees",
            abbrev="4 Macc",
            aliases=[],
            chapters=18,
        ),
    ],
)

NT = Library(
    id=400,
    name="New Testament",
    abbrev="NT",
    books=[
        Book(
            id=1,
            name="Matthew",
            abbrev="Matt",
            aliases=["mt"],
            chapters=28,
        ),
        Book(
            id=2,
            name="Mark",
            abbrev="Mark",
            aliases=["mk"],
            chapters=16,
        ),
        Book(
            id=3,
            name="Luke",
            abbrev="Luke",
            aliases=["lk"],
            chapters=24,
        ),
        Book(
            id=4,
            name="John",
            abbrev="John",
            aliases=["jn"],
            chapters=21,
        ),
        Book(
            id=5,
            name="Acts",
            abbrev="Acts",
            aliases=["ac"],
            chapters=28,
        ),
        Book(
            id=6,
            name="Romans",
            abbrev="Rom",
            aliases=["ro"],
            chapters=16,
        ),
        Book(
            id=7,
            name="1 Corinthians",
            abbrev="1 Cor",
            aliases=[],
            chapters=16,
        ),
        Book(
            id=8,
            name="2 Corinthians",
            abbrev="2 Cor",
            aliases=[],
            chapters=13,
        ),
        Book(
            id=9,
            name="Galatians",
            abbrev="Gal",
            aliases=[],
            chapters=6,
        ),
        Book(
            id=10,
            name="Ephesians",
            abbrev="Eph",
            aliases=[],
            chapters=6,
        ),
        Book(
            id=11,
            name="Philippians",
            abbrev="Phil",
            aliases=[],
            chapters=4,
        ),
        Book(
            id=12,
            name="Colossians",
            abbrev="Col",
            aliases=[],
            chapters=4,
        ),
        Book(
            id=13,
            name="1 Thessalonians",
            abbrev="1 Thess",
            aliases=["1 Th"],
            chapters=5,
        ),
        Book(
            id=14,
            name="2 Thessalonians",
            abbrev="2 Thess",
            aliases=["2 Th"],
            chapters=3,
        ),
        Book(
            id=15,
            name="1 Timothy",
            abbrev="1 Tim",
            aliases=[],
            chapters=6,
        ),
        Book(
            id=16,
            name="2 Timothy",
            abbrev="2 Tim",
            aliases=[],
            chapters=4,
        ),
        Book(
            id=17,
            name="Titus",
            abbrev="Tit",
            aliases=[],
            chapters=3,
        ),
        Book(
            id=18,
            name="Philemon",
            abbrev="Phlm",
            aliases=["Phm"],
            chapters=1,
        ),
        Book(
            id=19,
            name="Hebrews",
            abbrev="Heb",
            aliases=[],
            chapters=13,
        ),
        Book(
            id=20,
            name="James",
            abbrev="Jam",
            aliases=["jas"],
            chapters=5,
        ),
        Book(
            id=21,
            name="1 Peter",
            abbrev="1 Pet",
            aliases=[],
            chapters=5,
        ),
        Book(
            id=22,
            name="2 Peter",
            abbrev="2 Pet",
            aliases=[],
            chapters=3,
        ),
        Book(
            id=23,
            name="1 John",
            abbrev="1 John",
            aliases=["1 Jn"],
            chapters=5,
        ),
        Book(
            id=24,
            name="2 John",
            abbrev="2 John",
            aliases=["2 Jn"],
            chapters=1,
        ),
        Book(
            id=25,
            name="3 John",
            abbrev="3 John",
            aliases=["3 Jn"],
            chapters=1,
        ),
        Book(
            id=26,
            name="Jude",
            abbrev="Jude",
            aliases=["jd"],
            chapters=1,
        ),
        Book(
            id=27,
            name="Revelation",
            abbrev="Rev",
            aliases=["Apocalypse", "Apoc"],
            chapters=22,
        ),
    ],
)
