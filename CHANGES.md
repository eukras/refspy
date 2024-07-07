# Changes

## 0.9.* -- BETA DEVELOPMENT

* Initial release 

### 0.9.1-4 -- GAMMA

* Initial release; features and implementation may change before 1.0.0; the
  manager facade should provide a consistent and backwards-compatible interface.

### 0.9.5 -- BETA

* Removed 'depth' from books; determined by book.chapters == 1.
* Removed 'code' from books and library; __.param() is calculated from book.abbrev.
* Detects malformed references.
* Matches partial and abbreviated number ranges.
* Added pdoc for readthedocs.io.
* Added sort_references(), merge_references(), combine_references().

### 0.9.6 -- BETA

* Remove unused functions and types.
* Infer abbreviations in number ranges.
* Added merge_ranges() and combine_ranges() + tests
* Add range constructor functions for verses.

### 0.9.7 -- BETA

* Add make_index() and make_summary(); add to demo.

### 1.0.0 -- ALPHA

(Future)
