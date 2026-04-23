![RefSpy Logo](https://github.com/eukras/refspy/raw/master/media/refspy-logo.png)

[![Python package](https://github.com/eukras/refspy/actions/workflows/python-package.yml/badge.svg)](https://github.com/eukras/refspy/actions/workflows/python-package.yml)
[![Documentation Status](https://readthedocs.org/projects/refspy/badge/?version=latest)](https://refspy.readthedocs.io/en/latest/?badge=latest)

[![python](https://img.shields.io/badge/Python-3.11-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
![Version: 0.11.6 Beta](https://img.shields.io/badge/Version-0.11.6-purple)
![Status: BETA](https://img.shields.io/badge/Status-BETA-red)

Refspy is a Python package for working with Bible references in plain text.

[![Github Stars](https://img.shields.io/github/stars/eukras/refspy)](https://img.shields.io/github/stars/eukras/refspy)

# README

- [eukras/refspy on Github](https://github.com/eukras/refspy) | [Report Issue](https://github.com/eukras/refspy/issues) | [Contact Author](mailto:nigel@chapman.id.au)
- [refspy on PyPI](https://pypi.org/project/refspy/) &rarr; `pip install refspy`.
- [INTERNALS.md](https://github.com/eukras/refspy/blob/master/INTERNALS.md) | [refspy on ReadTheDocs](https://refspy.readthedocs.io/en/latest/refspy.html) &rarr; See `docs/` dir.
- [CHANGES.md](https://github.com/eukras/refspy/blob/master/CHANGES.md) | [TODO.md](https://github.com/eukras/refspy/blob/master/TODO.md)

## Online Demonstration

[Bible Rocket](https://www.chapman.id.au/bible-rocket) is an online demonstration of most of the features of the `refspy`
package. It will match, link, and index Bible references in human-written text.

|                                                                   Online Demonstration                                                                    |                                                                                                Example of Distribution Graph                                                                                                |
| :-------------------------------------------------------------------------------------------------------------------------------------------------------: | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: |
| [![Bible Rocket](https://github.com/eukras/refspy/raw/master/media/bible-rocket.png)](https://github.com/eukras/refspy/raw/master/media/bible-rocket.png) | [![Reference Distribution](https://github.com/eukras/refspy/raw/master/media/the-westminster-confession-of-faith-1646.svg)](https://github.com/eukras/refspy/raw/master/media/the-westminster-confession-of-faith-1646.svg) |

## Multi-language Demonstration

The script [demo.py](https://github.com/eukras/refspy/blob/master/demo.py) will generate files like `demo/en_US.html` for all languages, which are used to make the following screenshots.

|                                                              `en_US` ([@eukras](https://github.com/eukras))                                                               |                                                             `fr_FR` ([@a2ohm](https://www.github.com/a2ohm))                                                              |
| :-----------------------------------------------------------------------------------------------------------------------------------------------------------------------: | :-----------------------------------------------------------------------------------------------------------------------------------------------------------------------: |
| [![RefSpy Demo: en_US](https://github.com/eukras/refspy/raw/master/media/refspy-demo-en_US.png)](https://github.com/eukras/refspy/raw/master/media/refspy-demo-en_US.png) | [![RefSpy Demo: fr_FR](https://github.com/eukras/refspy/raw/master/media/refspy-demo-fr_FR.png)](https://github.com/eukras/refspy/raw/master/media/refspy-demo-fr_FR.png) |

## Features

- Match international and European syntaxes (Matt 5:3,7-9 / Matt 5,3.7-9).
- Use contextual book references to interpret partial references (e.g. "in Romans see 5:4").
- Sequentially replace matched references.
- Compile indexes of all matched references, or all verse ranges covered; list the most referenced chapters (hotspots) in a list of references.
- Format references as names, abbreviated names, and URL parameters.
- Generate HTML links of any required format.
- Construct and manipulate verses, ranges, and references.
- Compare and sort verses, ranges, and references.
- Collate references by library and book for iteration.
- Test if references or ranges contain, overlap, or adjoin one another; merge overlapping references and join adjacent ones.
- Store verses as `UNSIGNED INT(12)` for database indexing.
- Generally follow established conventions, so SBL style and SBL/USFM book names in English.

Not implemented:

- Old style references: Rev. 2 and 3, Matt. 28. 20; Acts 1. 8, 2 Cor. 9. 1-12 (1930s). Matt. xxv. 46. Dan. xii. 2. 2 Thes. i. 7-10. Ephes. iv. 18 (1790s).

# HOWTO

## The Reference Manager

Initialising `refspy` with corpus and language names will return a reference
manager. This provides a single convenient interface for the whole library.
By default, refspy provides a Protestant canon in English.

```python
from refspy import refspy
__ = refspy()
```

Or, to create specific canons:

```python
from refspy.languages.english import ENGLISH
from refspy.languages.french import FRENCH
from refspy.libraries.en_US import DC, DC_ORTHODOX, NT, OT
from refspy.libraries.fr_FR import DC as DC_FR, NT as NT_FR, OT as OT_FR
from refspy.manager import Manager

# Protestant, equivalent to `refspy()`
__ = refspy('protestant', 'en_US')
__ = Manager(libraries=[OT, NT], language=ENGLISH)

# Catholic
__ = refspy('catholic', 'fr_FR')
__ = Manager(libraries=[OT_FR, DC_FR, NT_FR], language=FRENCH)

# Orthodox
__ = refspy('orthodox', 'en_US')
__ = Manager(libraries=[OT, DC, DC_ORTHODOX, NT], language=ENGLISH)
```

Additionally, a third argument can specify International or European syntax
for references, that is, whether to write `Matt 5:3,7-9` or `Matt 5,3.7-9`.
If not argument is given, the default syntax for the specified language will be
used.

The file `refspy/setup.py` shows valid names for libraries and languages.
There's only English initially. The `en_US` libraries conform to the SBL Style
Guide for book names and abbreviations. Other libraries can be defined and
added locally following the structure in `refspy.libraries.en_US`. If they
follow established academic usage where possible, please contribute them to the
project.

### Creating references

Shortcut functions can create simple references using any book name,
abbreviation, or alias in the libraries list. Firstly, we can create
references from strings:

```python
ref = __.r('Rom 2:6,9,1,2')
```

We can construct references more programmatically with `__.bcv()`:

```python
assert __.name(__.bcv('Rom')) == 'Romans'
assert __.name(__.bcv('Rom', 2)) == 'Romans 2'
assert __.name(__.bcv('Rom', 2, 2)) == 'Romans 2:2'
assert __.name(__.bcv('Rom', 2, 2, 3)) == 'Romans 2:2-3'
```

Or `__.bcr()` to specify book, chapter and verse ranges:

```python
assert __.name(__.bcr('Rom', 2, [(2, 3), 7])) == "Romans 2:2-3,7"
```

### Options

Both `refspy()` and `refspy.matcher.Matcher()` take the following optional
argument, which modify this usage. To obtain more fine-grained control of
aliasing, make your own copy of `refspy.libraries.en_US` and use it with
`Manager(libraries=[MY_LIB])`.

#### `include_two_letter_aliases=True` (default: `True`)

Allow two-letter book aliases to be matched: e.g. `Ge` for Genesis or `1 Ti`
for First Timothy. Note short names given as `abbrevs` (like `Ps`)
will not be filtered like aliases are. Aliases (e.g. `Is`, `Am`) that are also
common words will be only be matched as part of references (So `Am 3:1` but
not `Am`); the list of `ambiguous_aliases` for a language is supplied in the
language file, e.g. `refspy/languages/english.py`.

```
from refspy import refspy
__ = refspy(include_two_letter_aliases=True)
match, ref = __.first_reference('2Ti 1')
assert ref == __.bcv('2 Tim', 1)
```

### Formatting references

```python
ref = __.r('Rom 2:3-4,7')

assert __.name(ref) == 'Romans 2:3–4, 7'
assert __.book(ref) == 'Romans'
assert __.numbers(ref) == '2:3–4, 7'
assert __.abbrev_name(ref) == 'Rom 2:3–4, 7'
assert __.abbrev_book(ref) == 'Rom'
assert __.abbrev_numbers(ref) == '2:3–4, 7'
```

Some utility functions can be used to turn these into usable URL parameters if needed:

```python
from refspy.utils import url_param, url_escape

ref = __.r('2 Cor 3:4-5')
assert url_param(__.abbrev_name(ref)) == '2+cor+3.4-5'
assert url_escape(__.abbrev_name(ref)) == '2%20Cor%203%3A4-5'
```

In general, though, templating is a better way to make links.

### Templating references

```python
bible_gateway = (
    '<a href="https://www.biblegateway.com/passage/'
  + '?search={LINK}&version=NRSVA">'
  + '{NAME}'
  + '</a>'
)
ref = __.r('2 Cor 3:4-5')
link = __.template(reference, bible_gateway)

assert link.find('2%20Cor%203%3A4-5') > 0
assert link.find('2 Corinthians 3:4–5') > 0
```

The full list of template fields is:

| Field                  | Output                      |
| ---------------------- | --------------------------- |
| `{LINK}`               | `1%20Cor%202%3A3-4`         |
| `{NAME}`               | `1 Corinthians 2:3–4`       |
| `{BOOK}`               | `1 Corinthians`             |
| `{NUMBERS}`            | `2:3–4`                     |
| `{ASCII_NUMBERS}`      | `2:3-4`                     |
| `{ABBREV_NAME}`        | `1 Cor 2:3–4`               |
| `{ABBREV_BOOK}`        | `1 Cor`                     |
| `{ABBREV_NUMBERS}`     | `2:3–4`                     |
| `{ESC_NAME}`           | `1%20Corinthians%202%3A3-4` |
| `{ESC_BOOK}`           | `1%20Corinthians`           |
| `{ESC_NUMBERS}`        | `2%3A3-4`                   |
| `{ESC_ABBREV_NAME}`    | `1%20Cor%202%3A3-4`         |
| `{ESC_ABBREV_BOOK}`    | `1%20Cor`                   |
| `{ESC_ABBREV_NUMBERS}` | `2%3A3-4`                   |
| `{PARAM_NAME}`         | `1+cor+2.3-4`               |
| `{PARAM_BOOK}`         | `1+cor`                     |
| `{PARAM_NUMBERS}`      | `2.3-4`                     |

The `{LINK}` field is like `{ESC_ABBREV_NAME}`, but will use English-style
verse formatting with any language, which suits linking to sites like
Bible Gateway.

Templates can be passed as optional arguments to other rendering functions, say
to generate links within indexes.

```python
__.make_index(references, template=bible_gateway)
```

### Comparing references

A reference can be a set of any valid verses and verse ranges spread across multiple books or even libraries.

```python
rom_2 = __.r('Rom 2')
rom_4 = __.r('Rom 4')
rom_4a = __.bc('rom', 4)

assert rom_2 < rom_4
assert not rom_2 >= rom_4
assert rom_4 == rom_4a
```

Because references can be compared using the `<` operator, they can also be sorted without any special functions, and used in `min()` and `max()`.

```python
assert __.sort_references([rom_4, rom_2]) == [rom_2, rom_4]
assert sorted([rom_4, rom_2]) == [rom_2, rom_4]  # <-- Same
assert min([rom_4, rom_2]) == rom_2
```

### Contains, Overlaps, Adjoins

We will commonly want to know if one reference `contains()`, or `overlaps()` another. The `adjoins()` function works out adjacency for chapters and verses, but note it is limited by not knowing the lengths of chapters.

```python
gen1 = __.r('Gen 1')
gen2 = __.r('Gen 2')
gen1_22_23 = __.r('Gen 1:22-23')
gen1_24_28 = __.r('Gen 1:24-28')

assert gen1.contains(gen1_22_23)
assert gen1_22_23.overlaps(gen1)
assert gen1_22_23.adjoins(gen1_24_28)
assert gen1.adjoins(gen2)
assert not gen1.overlaps(gen2)
```

## Sort, Merge, and Combine

References can be simplified by merging overlapping ranges and combining those
that are adjacent.

```python
assert __.merge_references([gen1_22_23, gen1]) == gen1
assert __.combine_references([gen1, gen2]) == __.r('Gen 1-2')
assert __.combine_references([gen1_22_23, gen1_24_28]) == __.r('Gen 1:22-28')
```

Under the hood, these methods just join the range lists together and merge or
combine them into a new reference. (Note the `*` operator to unpack lists into
arguments for `reference()`.)

```python
from refspy.range import merge_ranges, combine_ranges

assert reference(*merge_ranges(ranges)) == __.merge_references([reference(*ranges)])
assert reference(*combine_ranges(ranges)) == __.combine_references([reference(*ranges)])
```

## Manipulating references

Among other transformations, references can be turned into their (first) book
objects or references to just their books or chapters.

```python
ref1 = __.ref('Rom 2:3-4,7')

assert __.get_book(ref1).chapters == 16
assert __.name(ref1.book_reference()) == 'Romans'
assert __.name(ref1.chapter_reference()) == 'Romans 2'
```

### Navigating references

```python
assert __.next_chapter(rom_2) == rom_3
assert __.prev_chapter(rom_2) == rom_1
assert __.prev_chapter(rom_1) == acts_28
assert __.prev_chapter(matt_1) is None
```

To create chapter references:

```python
from refspy.libraries.en_US import NT

nt_chapter_refs_ = [
  __.bcv(book.name, ch)
  for ch in range(1, book.chapters)
  for book in NT.books
]
```

### Matching references in text

To find references in text and print HTML links for them:

```python
url = 'https://www.biblegateway.com/passage/?search=%s&version=NRSVA"

text = "Rom 1; 1 Cor 8:3,4; Rev 22:3-4"

strs, refs = __.find_references(text)
for match_str, ref in zip(strs, refs):
   print(f"{match_str} -> {url % __.param(ref)}")
```

### Replacing references in text

To produce the demo image above, we can use the `sequential_replace` function from `refspy/utils`:

```python
from refspy.utils import sequential_replace

strs, tags = [], []
for match_str, ref in __.find_references(text,
                                         include_books=True,
                                         include_nones=True):
    strs.append(match_str)
    if ref is None: # purple
          tags.append(f'<span class="refspy-invalid-reference">{match_str}</span>')
    elif ref.is_book(): # yellow
        tags.append(f'<span class="refspy-contextual-reference">{match_str}</span>')
    else: # green
        tags.append(
            f'<span class="refspy-reference">{match_str}</span><sup>{__.abbrev_name(ref)}</sup>'
        )
html = sequential_replace(text, strs, tags)}
```

### Collating and Indexing

To produce the index for the demo image above:

```python
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
