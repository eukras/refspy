# CHANGES

## 1.0.0

(Future)

## 0.11.1 -- BETA -- MULTILINGUAL

* Structural changes to support multiple languages.
* Add French book names and referencing conventions.

## 0.10.1 -- BETA -- BREAKING CHANGE

* make_index, make_summary, make_hotspots now return `str`,
while make_index_references, make_summary_references, make_hotspots_references
return `List[Reference]`. This is a consistent way to access the Reference
objects in all cases.

## 0.9 -- ALPHA -- INITIAL DEVELOPMENT

### 0.9.14 -- BETA

* fix: make_hotposts_text() arg names; affecting demo.py

### 0.9.13 -- BETA

* Calculate hotspots (i.e. most referenced chapters)
* Prevent matching e.g. '0.4' (no longer handle params in regular text). 
* Article Wiki integration: support for reference indexes in book-length documents.

### 0.9.7 -- BETA

* Add __.make_index() and __.make_summary(), incl. for demo.
* `url_param()` and `url_escape()` replace `__.param()`.
* Add __.template() to Manager, integrate with summary example.
* More compact and efficient book names in regexp (group by prefixes).

### 0.9.6 -- BETA

* Remove unused functions and types.
* Infer abbreviations in number ranges: 123-24 becomes 123-124.
* Added merge_ranges() and combine_ranges() + tests.
* Add range constructor functions for verses.

### 0.9.5 -- BETA

* Removed 'depth' from books; determined by book.chapters == 1.
* Removed 'code' from books and library; __.param() is calculated 
    from book.abbrev.
* Detects malformed references.
* Matches partial and abbreviated number ranges.
* Added pdoc for readthedocs.io.
* Added sort_references(), merge_references(), combine_references().

### 0.9.1-4 -- INITIAL CHECK-IN

* Initial release; features and implementation may change before 1.0.0; the
  manager facade should provide a consistent and backwards-compatible
  interface.
