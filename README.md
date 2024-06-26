# README 

![RefSpy Logo](refspy-logo.svg)


[![python](https://img.shields.io/badge/Python-3.11-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![License: GPLv3](https://img.shields.io/badge/License-MIT-blue.svg)](https://www.gnu.org/licenses/MIT)


See [docs/INTERNALS.md](docs/INTERNALS.md) for implementation.

## Introduction

Refspy is a biblical referencing library in Python. We use context
to interpret shorthand references, like a human reader would. We match number
patterns that represent references, and match book names as context for
interpreting them: 

```
In Romans we want 1:3-4, 7 and, in 1 Corinthians, we want 2:5.
   >>>>>>         ^^^^^^^^         >>>>>>>>>>>>>          ^^^
```

In isolation, a number or a range (`1` or `2-3`) could refer to either verses
or chapters, or to chapter numbers for a publication, or other regular numbers
that have nothing to do with biblical referencing. So, we only match numbers
that are preceded by a book name, a chapter number and colon (`4:`), or a verse
marker (`v.`, `vv.`). The book name lets us say whether the reference will be
to chapters or verses, and the others are unambiguous.

```
Romans 1:3-4, 7 (but not 1 Cor 4:2 or v.5!) and vv.9-10.
^^^^^^^^^^^^^^^          ^^^^^^^^^    ^^^       ^^^^^^^
```

We also accommodate some natural language conventions. Here, the final
reference is still matched as Romans 1:9-10, ignoring the aside that was given
in parentheses. SBL conventions require that '1 Corinthians' also match 'First
Corinthians' at the start of a sentence, so we match that everywhere.

Apart from this we try to offer every feature that other referencing tools
provide, such as comparisons and indexing methods. The library's internals are
described below. 


## Demo

![RefSpy Demo](refspy-demo.png)

## Features

* Find biblical references in strings, using normal shorthands
* Construct and manipulate verses, ranges, and references
* Format references as names, abbreviations, or URL parameters
* Store verses as `UNSIGNED INT(12)` for database indexing
* Compare and sort verses, ranges, and references (`<`, `==`, `>=`)
* Test if a range contains, overlaps, or adjoins another range
* Combine and simplify ranges.
* Collate references by library and book for iteration
* Merge and split references
* Generate links to online bibles
* Sequentially replace matched references in strings, e.g. with HTML links
* In English, we follow SBL conventions, including matching 'First Corinthians'
  for '1 Corinthians'.


## Installation

```
pip install refspy
```


## The Reference Manager


Initialising `refspy` with corpus and language names will return a reference
manager. This provides a single convenient interface for the whole library. 

```
from refspy import refspy

__ = refspy()  # <-- Defaults to 'protestant', 'en_US'

__ = refspy('protestant', 'en_US')  

__ = refspy('protestant', 'el_KO')  # <-- with koine greek 
__ = refspy('catholic', 'es_ES')
__ = refspy('orthodox', 'el_GR')
```

The file `refspy/corpus.py` shows valid corpus names, and `refspy/language.py` contains valid language names.
```
from refspy.language.en import ENGLISH
from refspy.libraries.en_US import NT, OT, OT_Apoc
from refspy.libraries.es_ES import NT as NT_es
from refspy.manager import Manager 

M1 = Manager(libraries=[OT, NT], ENGLISH)            # Protestant Canon in English
M2 = Manager(libraries=[OT, OT_Apoc, NT], ENGLISH)   # Catholic Canon in English
M3 = Manager(libraries=[NT_es], SPANISH)             # New Testament in Spanish
```



The `en_US` libraries conform to the SBL Style Guide for book names and
abbreviations. Accordingly, we use semicolons (`;`) to separate chapter-level
references. 


### Creating references 

Shortcut functions can create simple references using any book name,
abbreviation, code, or alias in the libraries list. Firstly, we can create
references from strings:

```
___.r('Rom 2:3-4,7')
```

A reference contains a list of ranges (see below). It can sort and combine
these to keep the references as compact as possible. We can use the `__.name`
and `__.abbrev` functions to get back string references again:

TODO: Combinations

```
ref = __.r('Rom 2:6,9,1,2')
assert __.name(ref) == 'Romans 2:1-2,6,9'

ref = __.r('Rom 2:6,9,1,2', sort=False, combine=False)
assert __.abbrev(ref) == 'Rom 2:6,9,1,2'
```

We can construct references more programmatically with `__.bcv()`:

```
___.bcv('rom')                # Rom (whole book)  
___.bcv('rom', 2)             # Rom 2 (whole chapter)
___.bcv('rom', 2, 2)          # Rom 2:2
___.bcv('rom', 2, 2, 3)       # Rom 2:2-3 (optional end verse)
```

Or `__.bcr()` to specify book, chapter and verse ranges:

```
___.bcr('rom', 2, [(2, 3), 7])    # Rom 2:2-3,7 (from range) 
```

We could make chapter references for the whole New Testament like this:

```
nt_chapter_refs_ = [  
  __.bcv(book.id, ch)   
  for ch in range(1, book.chapters)   
  for book in NT.books  
] 
```


### Comparing references

A reference can be a set of any verses and verse ranges spread across multiple
libraries. Comparing references A and B means checking that all ranges in A are
less than all ranges in B. For large or complex references this is not
intuitive and not recommended. Comparing simple references is reasonable,
however, as it just involves comparing simple ranges: 

```
rom_2 = __.r('Rom 2')
rom_4 = __.r('Rom 4')
rom_4a = __.bc('rom', 4)

rom_2 < rom_4    # True
rom_2 >= rom_4   # False
rom_4 == rom_4a  # True
```

Because references can be compared with `<`, they can also be sorted. 

```
sorted([rom_4, rom_2]) == [rom_2, rom_4]  # True
```

We can also check several kinds of comparisons between references:

```
gen1 = __.r('Gen 1') 
gen2 = __.r('Gen 2') 
gen1_23_23 = __.r('Gen 1:22-23') 
gen1_24_28 = __.r('Gen 1:24-28')
  
gen = __.b('Gen')
ex = __.b('Ex')

# Check ranges...
gen1.contains(gen1_22_23)       # True
gen1_22_23.overlaps(gen1)       # True
gen1_22_23.adjoins(gen1_24_28)  # True
gen1.adjoins(gen2)              # True
gen1.overlaps(gen2)             # False
gen.adjoins(ex)                 # True
gen.overlaps(ex)                # False```
```


### Manipulating references

References can be turned into their first book object, a list of books, or a
reference to just their book or chapter ranges.

```
ref1 = __.ref('Rom 2:3-4,7')

__.book(ref1).name      # Romans
__.book(ref1).abbrev    # Rom
__.book(ref1).code      # rom

ref2 = __.ref('Rom 2, Php 4')

", ".join(__.book().name for _ in __.books(ref2, unique=True, sorted=True))  
  
^ Romans, Philippians

__.name(__.book_reference(ref1))       # Romans
__.name(__.chapter_reference(ref1))    # Romans 2
```


### Formatting references

```
ref = ___.r('Rom 2:3-4, 7')

__.name(ref)           # 'Romans 2:3-4,7'
__.abbrev(ref)         # 'Rom 2:3-4,7'
__.code(ref)           # 'rom+2.3-4,7'
__.numbers(ref)        # '2:3-4,7'
```


### Navigating references

```
assert next_chapter(rom_2) == rom_3
assert prev_chapter(rom_2) == rom_1
```


### Matching references in text

Here's how we might find references in text and print HTML links for them:

```
url = 'https://www.biblegateway.com/passage/'

text = "Rom 1; 1 Cor 8:3,4; Rev 22:3-4"
   
strs, refs = __.find_references(text)
for s, ref in zip(strs, refs):
   print f"{s} -> {url}{?search={__.code(ref)}&version=NRSVA"
```


### Replacing references in text

### Collating and traversing

Because a reference can contain ranges that span multiple libraries, it can
make more sense to collate them than to sort them. 

References lists can be created for strings using __.find_references(), and
grouped into libraries and books using __.collate(). 

In this example, we find references in a text and print them as an formatted
reference index:

```
matches, references = __.find_references(text):
library_collation = __.collate(references) 
for library, book_collation in library_collation:
  print(library.name)
  for book, book_references in book_collation:
    print('  ' + book.name)
    for reference in book_references:
      print('    ' + __.name(reference) + '. ' + __.url(reference))
```

The `examples/create_index.py` file processes the following text in this way:

```
The major theme of Romans is how Jewish Christians relate to Hellenistic
Christians and vice-versa. Or rather, in light of apparent difficulties, how
they should relate. Paul’s headline statements present “the gospel” as God’s
promise, in Jewish scripture, to make gentiles his people, just as much as Jews
(1:1–4; 1:16–17; 15:7–13; 16:25–27, cf. 10:15; Isa 52:7; 61:1), whether they
were the ‘wise’ Hellenists of Rome and Athens or mere ‘foolish’ barbarians
(1:14). God is not the God of Jews only, but the God of gentiles too (3:29),
and he shows no partiality in judging or saving either (2:11), thus showing
himself to be just. Good and evil will be recompensed, and those with faith and
faithfulness (pistis, same word) will be saved, “the Jew first and also the
Greek” (1:16; 2:9–10, and ch.2–3 generally). But gentile Christians are like
branches grafted into a Jewish olive tree (11:17-24). This raises many
questions for Christians of gentile or Jewish identities, which the letter then
pursues. Is there any advantage in being Jewish (3:1–4); where is this ‘faith’
in the Old Testament (ch.4); what things may we “boast” or take pride in, if
not our identities as Jews or gentiles (2:17, 23; 3:27; 4:2; 5:1–11; 11:18;
15:17; cf. 1 Cor 1:26–31; 2 Cor 5:11–12; and 2 Cor 10–12 generally); was the
Jewish law a bad thing (5:12–21); how is God’s grace related to it (6:1–14);
does God’s grace mean sin doesn’t really matter (6:15–23); how do we overcome
that same tendency to sin that made the law ineffective (7–8); did God’s
promise to Israel fail and why aren’t more Jews Christians and is Israel
finished (ch.9–11); how do people who respect food laws and religious holidays
get on with people who don’t, without quarreling? (13:11–15:6; cf.
16:17–20). How Jewish and gentile Christians should relate is the thread of
the letter from start to end. It is the conflicted state of these
relations that calls forth the exhortations to love one another, live
peaceably, and not think of ourselves more highly than we should (11:25,
12:3; 12:11–13:10, 15:7–13). Paul emphasises all the way through that the
gospel reconciles both Jews and gentiles to God and each other in Christ.  
```

It produces the output:

CONTINUE

