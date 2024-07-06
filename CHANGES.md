# Changes

## 0.9.1-4 -- BETA

* Initial release; features and implementation may change before 1.0.0; the
  manager facade should provide a consistent and backwards-compatible interface.

## 0.9.5 -- BETA

* Removed 'depth' from books; determined by book.chapters == 1.
* Removed 'code' from books and library; __.param() is calculated from book.abbrev.
* Detects malformed references.
* Matches partial and abbreviated number ranges.
* Added pdoc for readthedocs.io.
* Added sort_references(), merge_references(), combine_references().

