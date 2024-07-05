![RefSpy Logo](https://github.com/eukras/refspy/raw/master/media/refspy-logo.png)

Refspy is a Python package for working with biblical references in ordinary text.

[![python](https://img.shields.io/badge/Python-3.11-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
![Version: 0.9 BETA](https://img.shields.io/badge/Version-0.9_BETA-red)


# README 

* [eukras/refspy on Github](https://github.com/eukras/refspy) | [Report Issue](https://github.com/eukras/refspy/issues) | [Contact Author](mailto:nigel@chapman.id.au)
* [refspy on PyPI](https://pypi.org/project/refspy/) --> `pip install refspy`
* [refspy on ReadTheDocs](https://readthedocs.io/) (or see [docs/html/](docs/html/) dir)


## Demo

![RefSpy Demo](https://github.com/eukras/refspy/raw/master/media/refspy-demo.png)

(See `demo.py`)

## Features

* Find biblical references in strings, using normal shorthands
* Construct and manipulate verses, ranges, and references
* Format references as names, abbreviated names, and URL parameters
* Store verses as `UNSIGNED INT(12)` for database indexing
* Compare and sort verses, ranges, and references (`<`, `==`, `>=`)
* Test if a range contains, overlaps, or adjoins another range
* Collate references by library and book for iteration
* Sequentially replace matched references in strings, e.g. with HTML links
* In English, we follow SBL conventions, including matching 'First Corinthians'
  for '1 Corinthians'.


## The Reference Manager


Initialising `refspy` with corpus and language names will return a reference
manager. This provides a single convenient interface for the whole library. 
By default, refspy provides a Protestant canon in English.

```
from refspy import refspy
__ = refspy()
```

Or, to create specific canons:

```
from refspy.language.en import ENGLISH
from refspy.libraries.en_US import DC, DC_ORTHODOX, NT, OT
from refspy.manager import Manager 

# Protestant
__ = refspy('protestant', 'en_US')
__ = Manager(libraries=[OT, NT], ENGLISH)

# Catholic
__ = refspy('catholic', 'en_US')
__ = Manager(libraries=[OT, DC, NT], ENGLISH)

# Orthodox
__ = refspy('orthodox', 'en_US')
__ = Manager(libraries=[OT, DC, DC_ORTHODOX, NT], ENGLISH)
```

The file `refspy/setup.py` shows valid names for libraries and languages.
There's only English initially. The `en_US` libraries conform to the SBL Style
Guide for book names and abbreviations. Other libraries can be defined and
added locally following the structure in `refspy.libraries.en_US`. If they 
follow established academic usage where possible, please contribute them to 
the project.


### Creating references 

Shortcut functions can create simple references using any book name,
abbreviation, or alias in the libraries list. Firstly, we can create
references from strings:

```
ref = __.r('Rom 2:6,9,1,2')
```

We can construct references more programmatically with `__.bcv()`:

```
ref = ___.bcv('Rom')                # Rom (whole book)  
ref = ___.bcv('Rom', 2)             # Rom 2 (whole chapter)
ref = ___.bcv('Rom', 2, 2)          # Rom 2:2
ref = ___.bcv('Rom', 2, 2, 3)       # Rom 2:2-3 (optional end verse)
```

Or `__.bcr()` to specify book, chapter and verse ranges:

```
ref = ___.bcr('Rom', 2, [(2, 3), 7])    # Rom 2:2-3,7 (from range) 
```


### Formatting references

```
ref = ___.r('Rom 2:3-4, 7')

assert __.name(ref) == 'Romans 2:3–4,7'
assert __.abbrev(ref) == 'Rom 2:3–4,7'
assert __.param(ref) == 'rom+2.3-4,7'
assert __.numbers(ref) == '2:3–4,7'
```


### Comparing references

A reference can be a set of any verses and verse ranges spread across multiple
libraries. Comparing references A and B just means comparing their first verse. 

```
rom_2 = __.r('Rom 2')
rom_4 = __.r('Rom 4')
rom_4a = __.bc('rom', 4)

assert rom_2 < rom_4
assert not rom_2 >= rom_4
assert rom_4 == rom_4a
```

Because references can be compared with `<`, they can also be sorted, or used
in `min()` and `max()`. 

```
assert sorted([rom_4, rom_2]) == [rom_2, rom_4]
assert min([rom_4, rom_2]) == rom_2
```

### Contains, Overlaps, Adjoins

We will commonly want to know if one reference `contains()`, or `overlaps()`
another. The `adjoins()` function works out adjacency for chapters and verses,
but note it is limited by not knowing the lengths of chapters. (Adjacency may
be used in future to combine and simplify references.)

```
gen1 = __.r('Gen 1') 
gen2 = __.r('Gen 2') 
gen1_23_23 = __.r('Gen 1:22-23') 
gen1_24_28 = __.r('Gen 1:24-28')
  
assert gen1.contains(gen1_22_23)
assert gen1_22_23.overlaps(gen1)
assert gen1_22_23.adjoins(gen1_24_28)
assert gen1.adjoins(gen2)
assert not gen1.overlaps(gen2)
```

## Manipulating references

Among other transformations, references can be turned into their (first) book
objects or references to just their books or chapters.

```
ref1 = __.ref('Rom 2:3-4,7')

assert __.book(ref1).chapters == 16
assert __.name(ref1.book_reference()) == 'Romans'
assert __.name(ref1.chapter_reference(ref1)) == 'Romans 2'
```

### Navigating references

```
assert next_chapter(rom_2) == rom_3
assert prev_chapter(rom_2) == rom_1
assert prev_chapter(rom_1) == acts_28
assert prev_chapter(matt_1) == None
```

To create chapter references:

```
from refspy.libraries.en_US import NT

nt_chapter_refs_ = [  
  __.bcv(book.name, ch)   
  for ch in range(1, book.chapters)   
  for book in NT.books  
] 
```


### Matching references in text

To find references in text and print HTML links for them:

```
url = 'https://www.biblegateway.com/passage/?search=%s&version=NRSVA"

text = "Rom 1; 1 Cor 8:3,4; Rev 22:3-4"
   
strs, refs = __.find_references(text)
for match_str, ref in zip(strs, refs):
   print(f"{match_str} -> {url % __.param(ref)}")
```

### Replacing references in text

To produce the demo image above, we use the `sequential_replace` function from `refspy/utils`:

```
from refspy.utils import sequential_replace

matches = __.find_references(text, include_books=True)
strs, tags = [], []
for match_str, ref in matches:
    strs.append(match_str)
    if ref.is_book():
        tags.append(f'<span class="yellow">{match_str}</span>')
    else:
        tags.append(
            f'<span class="green">{match_str}</span><sup>{__.abbrev(ref)}</sup>'
        )
html = sequential_replace(text, strs, tags)}
```

### Collating and Indexing

To produce the index for the demo image above:

```
matches = __.find_references(text)

index = []
for library, book_collation in __.collate(
    sorted([ref for _, ref in matches])
):
    for book, reference_list in book_collation:
        new_reference = __.merge(reference_list)
        index.append(__.abbrev(new_reference))

html_list = "; ".join(index)
```

# Internals

## Glossary

`Book`, `Format`, `Language`, `Library`, `Number`, `Range`, `Reference`, and
`Verse` are Pydantic types that will raise ValueErrors if initialised with bad
data, say if a verse has Numbers outside the range `0..999`, or if a Range has
a start verse that is greater than its end verse.

- **Book**. A book has id, name, abbrev, aliases, and chapters. No verse counts.
- **Format**. The Format objects define what properties and characters to use when formatting references for various purposes.
- **Index**. An integer which results from expanding a verse by powers of 1000; `verse(1, 7, 16, 1)` becomes the integer `1007016001`
- **Library**. A library has id, name, abbrev, and a list of Books. See e.g. `libraries/en_US.py`. Library IDs are spaced out in a roughly historical order: OT is 200, NT is 400.
- **Number**. An integer `1..999`. We assume verses/chapters/books/libraries are limited to this size. This may need modifying to accommodate, say, _zero verses_ in the Septuagint.
- **Range**. A pair of `(start, end)` verses; `1 Cor 16:1-2` becomes `range(verse(400, 7, 16, 1), verse(400, 7, 16, 2))`.
- **Reference**. A list of ranges; `1 Cor 16:1-2,6` becomes `reference([range(verse(400, 7, 16, 1), verse(400, 7, 16, 2)), range(verse(400, 7, 16, 6), verse(400, 7, 16, 6))])`. They do not automatically sort or simplify the ranges.
- **Verse**. A quadruple of `(library, book, chapter, verse)` numbers; `1 Cor 16:1` becomes `verse(400, 7, 16, 1)`


## Data Structures

### Libraries and Books

Libraries and books are Pydantic BaseModels, which apply validation checks to
the data whenever created or modified. These are defined by in locale files,
such as `refspy/languages/en_US.py`:

```
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
      ...
  ]
)
```

Any major class has its own file, so `Library` is defined in
`refspy/library.py` and so on.

Books and libraries have names, abbrevs, and aliases. If URL params are needs,
they are generated from these. So, the name '1 Corinthians' has the abbrev '1
Cor', wand generates the param '1cor'. The `languages/english.py` file says
that numeric prefixes must also match `I` and `First` (etc). The params are
lowercase with no spaces.

## Verses

A verse contains library, book, chapter, and verse numbers. The library, book,
chapter, and verse numbers are all in 1-3 digits, in the range 1-999. It is
assumed that there will not be 1000 or more verse in a chapter, chapters in a
book, books in a library, or total libraries.

Refspy does not know or care how many verses there are in a chapter. It is
expected that this will be determined from a database of texts by any client
application, especially since not all verse numbers actually exist in texts
(e.g. due to copying errors in the Vulgate at the time verse numbers were
assigned). However, knowing the number of chapters per book allows the previous
and next chapter to be determined, say, for navigating a library.

```
Verse(library=1, book=2, chapter=3, verse=4)
verse(1, 2, 3, 4)
verse(1, 2, 3, 1004)  # <-- ValueError
```

### Index Numbers

Verses convert to an index value, `verse(1, 2, 3, 4).index() == 1002003004`
(`UNSIGNED INT(12)`), which allows efficient indexing in databases:

```
sql_clause = " OR ".join([
    f"({column_name} BETWEEN {range.start.index()} AND {range.end.index()})"
    for range in reference.ranges
])
```

## Ranges

A range contains start and end verses.

A whole chapter is referenced as `range(verse(1, 1, 1, 1), verse(1, 1, 1, 999))`.

A whole book is referenced as `range(verse(1, 1, 1, 1), verse(1, 1, 999, 999))`.

So, a chapter or book contains every range and verse within that chapter or
book, however long the chapter or book are.

Verses and ranges convert to tuples e.g. `((1, 2, 3, 4), (1, 2, 3, 5))` which can
be sorted and compared. 

Ranges can be tested for containment, overlap, or adjacency. Note that this
does not take account of which verse numbers actually exist in any given text.

```
# Make ranges...
gen1 = range(verse(1, 1, 1, 1), verse(1, 1, 1, 999))
gen1_22_23 = range(verse(1, 1, 1, 22), verse(1, 1, 1, 23))
gen1_24_28 = range(verse(1, 1, 1, 24), verse(1, 1, 1, 28))
gen1 = range(verse(1, 1, 1, 1), verse(1, 1, 1, 999))
gen = range(verse(1, 1, 1, 1), verse(1, 1, 999, 999))
exod = range(verse(1, 2, 1, 1), verse(1, 2, 999, 999))

assert gen.is_book()
assert gen1.is_chapter()

assert gen1.contains(gen1_22_23)
assert gen1_22_23.overlaps(gen1)
assert gen1_22_23.adjoins(gen1_24_28)
assert gen1.adjoins(gen2)
assert not gen1.overlaps(gen2)
assert gen.adjoins(exod)
assert not gen.overlaps(exod)
```

Comparison operators can also be used, as well as sorting:

```
assert gen1 < gen2
assert not gen1 == gen2

gen_1_and_2 = range(verse(1, 1, 1, 1), verse(1, 1, 2, 999))

assert gen1 + gen2 == gen_1_and_2
assert sorted([gen2, gen1]) == [gen1, gen2]
assert min([gen2, gen1]) == gen1
```

## References

References are lists of verse ranges. These are entirely numerical objects.

References, ranges, and verses have shorter constructor functions for
programming convenience. Note `reference()` does not require list brackets.

```
Range(start=verse_1, end=verse_2)
range(verse_1, verse_2)

Reference(ranges=[range_1, range_2])
reference(range_1, range_2)

ref_1 = reference(
  range(verse(1, 1, 1, 1), verse(1, 1, 1, 3))
)

book_reference(1, 2)
chapter_reference(1, 2, 3)
verse_reference(1, 2, 3, 4) 
```

The same comparison operations that work on ranges also work on references. So
references can be `sorted()`, `min()`, or `max()`. This becomes less intuitive the
more complex their list of ranges becomes.

