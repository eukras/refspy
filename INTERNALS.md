# INTERNALS

# Code

```bash
github.com/AlDanial/cloc v 2.04  T=0.04 s (1285.4 files/s, 171816.9 lines/s)
-------------------------------------------------------------------------------
Language                     files          blank        comment           code
-------------------------------------------------------------------------------
Python                          44            933           1122           4396
Markdown                         6            177              0            519
TOML                             1              5              0             35
Text                             3              1              0             30
-------------------------------------------------------------------------------
SUM:                            54           1116           1122           4980
-------------------------------------------------------------------------------
```

## Glossary

`Book`, `Format`, `Index`, `Language`, `Library`, `Number`, `Range`,
`Reference`, and `Verse` are Pydantic types that will raise ValueErrors if
initialised with bad data, say if a verse has Numbers outside the range
`0..999`, or if a Range has a start verse that is greater than its end verse.
These appear in the models and types folders.

- **Book**. A book has id, name, abbrev, aliases, and chapters. No verse counts.
- **Format**. The Format objects define what properties and characters to use when formatting references for various purposes.
- **Index**. An integer which results from expanding a verse by powers of 1000; `verse(1, 7, 16, 1)` becomes the integer `1007016001`. Provided for database indexing if required.
- **Language**. A language has verse_markers (e.g. `v.` and `.vv.`), ambiguous_aliases (e.g. `Is` and `Am`, which are also words), and number prefixes (e.g. `Second` and `II` for `2`).
- **Library**. A library has id, name, abbrev, and a list of Books. See e.g. `libraries/en_US.py`. Library IDs are spaced out in a roughly historical order: OT is 200, NT is 400.
- **Number**. An integer `1..999`. We assume verses/chapters/books/libraries are limited to this size. This may need modifying to accommodate, say, _zero verses_ in the Septuagint.
- **Range**. A pair of `(start, end)` verses; `1 Cor 16:1-2` becomes `range(verse(400, 7, 16, 1), verse(400, 7, 16, 2))`.
- **Reference**. A list of ranges; `1 Cor 16:1-2,6` becomes `reference([range(verse(400, 7, 16, 1), verse(400, 7, 16, 2)), range(verse(400, 7, 16, 6), verse(400, 7, 16, 6))])`. They do not automatically sort or simplify the ranges.
- **Syntax**. The correct characters for matching and formatting references; international or European.
- **Verse**. A quadruple of `(library, book, chapter, verse)` numbers; `1 Cor 16:1` becomes `verse(400, 7, 16, 1)`

## Data Structures

### Libraries and Books

Libraries and books are Pydantic BaseModels, which apply validation checks to
the data whenever created or modified. These are defined by in locale files,
such as `refspy/languages/en_US.py`:

```python
OT = Library(
    id=200,
    name="Old Testament",
    abbrev="OT",
    books=[
        Book(
            id=1,
            name="Genesis",
            abbrev="Gen",
            aliases=['Ge'],
            chapters=50,
        ),
      ...
  ]
)
```

Any major class has its own file, so `Library` is defined in
`refspy/library.py` and so on.

Books and libraries have names, abbrevs, and aliases. If URL params are needed,
they are generated from these. So, the name '1 Corinthians' has the abbrev '1
Cor', and generates the param '1+cor'. The `languages/english.py` file says
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

```python
Verse(library=1, book=2, chapter=3, verse=4)
verse(1, 2, 3, 4)
verse(1, 2, 3, 1004)  # <-- ValueError
```

### Index Numbers

Verses convert to an index value, `verse(1, 2, 3, 4).index() == 1002003004`
(`UNSIGNED INT(12)`), which allows efficient indexing in databases:

```python
sql_clause = " OR ".join([
    f"({column_name} BETWEEN {range.start.index()} AND {range.end.index()})"
    for range in reference.ranges
])
```

Verses are read back with the class method `refspy.verse.Verse.from_index()`.

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

```python
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

```python
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

```python
Range(start=verse_1, end=verse_2)
range(verse_1, verse_2)

Reference(ranges=[range_1, range_2])
reference(range_1, range_2)

ref_1 = reference(
  range(verse(1, 1, 1, 1), verse(1, 1, 1, 3))
)
```

The reference module contains standalone functions for numeric reference
construction that parallel the reference manager's `__.bcv()` method.

```python
book = __.books[NT.id, 1]  # <-- Matthew is NT book ID 1
assert book_reference(NT.id, 1) == __.bcv(book.id)
assert chapter_reference(NT.id, 1, 2) == __.bcv(book.id, 2)
assert verse_reference(NT.id, 1, 2, 3) == __.bcv(book.id, 2, 3)
assert verse_reference(NT.id, 1, 2, 3, 4) == __.bcv(book.id, 2, 3, 4)
```

The same comparison operations that work on ranges also work on references. So
references can be `sorted()`, `min()`, or `max()`. This becomes less intuitive
the more complex their list of ranges becomes.
