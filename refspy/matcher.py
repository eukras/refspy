"""Match biblical references in texts, returning strings and Reference objects."""

import math
import re
from typing import Dict, Generator, List, Match, Tuple

from refspy import language
from refspy.book import Book
from refspy.language import Language
from refspy.range import Range, range, verse_range
from refspy.reference import (
    Reference,
    book_reference,
    reference,
)
from refspy.utils import (
    add_space_after_book_number,
    get_unnumbered_book_aliases,
    parse_number,
    normalize_spacing,
    trim_trailing_period,
)
from refspy.verse import Number, verse

COLON = r"[:\.]"
DASH = r"[–-]"
END = r"\b"
NUMBER = r"\d+[a-d]?"
SPACE = r"\s*"
RANGE = f"{NUMBER}{DASH}{NUMBER}"
LIST = f"(?:{RANGE}|{NUMBER})(?:\\,\\s*(?:{RANGE}|{NUMBER}))*"

RANGE_OR_NUMBER_COMPILED = re.compile(f"({RANGE}|{NUMBER})")

NUMBER_CAPTURE = re.compile(f"({NUMBER})")
RANGE_CAPTURE = re.compile(f"({NUMBER}){DASH}({NUMBER})")
CHAPTER_RANGE_CAPTURE = re.compile(
    f"{END}({NUMBER}){COLON}({NUMBER}){DASH}({NUMBER}){COLON}({NUMBER}){END}"
)
CHAPTER_VERSES_CAPTURE = re.compile(f"{END}({NUMBER}){COLON}({LIST}){END}")


class Matcher:
    """
    Match:
    - Opening and closing brackets
      - So we don't carry book context past the end of parentheses
    - References
      - Book names (incl. substitutions like 'First' for '1':
        - with no reference: sets context; only returned as a reference if
            requested with include_books=True
        - when book.chapter > 1:
          - 1:2-3:4
          - 1:1,2-3 etc
        - when book.chapter == 1:
          - 1,2-4  (can be verses or chapters, based on book; must not end with
            a number that starts a book name)
      - Stand-alone number references: always have colons or verse markers.
        They rely on context being provided by a previous reference or book
        name.
        - v.1, vv.1-2
        - 1:2-3:4
        - 1:1,2-3 etc (must not end with a number that starts a book name)
    Yield:
      - a (match_str, reference) tuple for each match.
    """

    def __init__(
        self,
        books: Dict[Tuple[Number, Number], Book],
        book_aliases: Dict[str, Tuple[Number, Number]],
        language: Language,
    ):
        self.books = books
        self.language = language
        self.book_alias_keys = book_aliases.keys()
        self.book_aliases = self.expand_book_aliases(book_aliases)
        self.brackets_regexp = re.compile(self.build_brackets_regexp())
        self.reference_regexp = re.compile(self.build_reference_regexp())

    def build_reference_regexp(self) -> str:
        """
        Reference matches are quadruples. For the string ...

        "Big Book 1:2-5 (cf. Small Book 34) is more interesting than vv.2:3-6."

        ... We want to know which references are attached to books and which are just numeric:

            ```
            Matching string
            :                 Book Name
            :                  :            Book Reference
            :                  :             :        Numeric Reference
            :                  :             :         :
            ('Big Book 1:2-5', 'Big Book',   '1:2-5',  None)
            ('Small Book 34',  'Small Book', '34',     None)
            ( None,             None,         None,   '2:3-6')
            ```
        """
        NAME_PATTERN = self.build_book_name_regexp()
        VERSE_MARKER = self.build_verse_marker_regexp()
        NUMBER_LIST = self.build_number_list_regexp()
        REGEXP = "".join(
            [
                "(",
                f"{END}({NAME_PATTERN})",  # Rom
                "(",
                "".join(
                    [
                        f"{SPACE}{NUMBER}{COLON}{NUMBER}{DASH}{NUMBER}{COLON}{NUMBER}",  # Rom 1:2-3:4
                        "|",
                        f"{SPACE}{NUMBER}{COLON}{NUMBER_LIST}",  # Rom 3:4,6-9
                        "|",
                        f"{SPACE}{NUMBER_LIST}",  # Phlm 3-4 (verse), Rom 3-4 (chapter)
                    ]
                ),
                ")?",
                ")|(",
                "".join(
                    [
                        f"{NUMBER}{COLON}{NUMBER}{DASH}{NUMBER}{COLON}{NUMBER}",  # 1:2-3:4
                        "|",
                        f"{NUMBER}{COLON}{NUMBER_LIST}",  # 3:4,6-9
                        "|",
                        f"(?:{VERSE_MARKER}){NUMBER_LIST}",  # vv.3-4
                    ]
                ),
                ")",
            ]
        )
        return REGEXP

    def expand_book_aliases(
        self, aliases: Dict[str, Tuple[int, int]]
    ) -> Dict[str, Tuple[int, int]]:
        """
        SBL style requires e.g. "1 Corinthians" be recognized as "First
        Corinthians" at the start of a sentence. Add these as keys to
        the aliases.

        Note:
            Number prefixes are set in the Language class.
        """
        out = {}
        for alias, library_book in aliases.items():
            out[alias] = library_book
            for number, prefixes in self.language.number_prefixes.items():
                if alias.startswith(number + " "):
                    for prefix in prefixes:
                        out[prefix + alias[1:]] = library_book
        return out

    def build_book_name_regexp(self):
        """
        Sort bookname DESC to match the longest first.
        Replace spaces with multi-space matchers in book names.
        Group book names by prefixes.
        Match substitute prefixes for each prefix number:

        Example:
            ```
            (   (1|First|etc)\\s*(Corinthians|etc)
              | (2|Second|etc)\\s*(Corinthians|etc)
              |   ...
              | (Galatians|Romans|etc)
            )
            ```
        """
        regexp_parts = []
        for number in self.numerical_book_prefixes(reverse=True):
            aliases = [
                alias[len(number + " ") :]
                for alias in self.book_alias_keys
                if alias.startswith(number + " ")
            ]
            regexp_parts.append(
                r"(?:"
                + "|".join([number] + self.language.number_prefixes[number])
                + r")"
                + r"\s*"
                + "(?:"
                + "|".join([escape_book_name(_) for _ in long_names_first(aliases)])
                + ")"
                # + r"(?![^A-Za-z])"  # <-- Need a non-alpha lookahead?
                + r"\b"
                + r"\.?"
            )
        leading_digits = re.compile(r"^\d+\s")
        aliases = [
            alias for alias in self.book_alias_keys if not leading_digits.match(alias)
        ]
        regexp_parts.append(
            r"(?:"
            + "|".join([escape_book_name(_) for _ in long_names_first(aliases)])
            + ")"
            # + r"(?![^A-Za-z])"  # <-- Need a non-alpha lookahead?
            + r"\b"
            + r"\.?"
        )
        return r"|".join(regexp_parts)

    def build_verse_marker_regexp(self):
        return "|".join([re.escape(key) for key in self.language.verse_markers])

    def build_number_list_regexp(self):
        """
        Match a comma-(and-space?)-separated list of numbers and ranges.

        A VERSE NUMBER is a number that can't be the start of a book name or chapter reference.

        We use negative lookaheads to exclude book names (1 Cor) or chapter refs (6:5):

        For en_US, this will look like:

            ```
            (
                1(?![:.]|\\s*(?:Corinthians|Cor|Thess|etc))
              | 2(?![:.]|\\s*(?:Corinthians|Cor|Thess|etc))
              | 3(?![:.]|\\s*(?:Jn))
              | [4-999](?![:.])
            )
            ```
        """
        regexp_parts = []
        # numbers which can be book numbers, when not followed by ':' or book names
        for number in self.numerical_book_prefixes():
            aliases = [
                alias[len(number + " ") :]
                for alias in self.book_aliases.keys()
                if alias.startswith(number + " ")
            ]
            regexp_parts.append(
                number
                + r"(?!"  # <-- negative look-ahead
                + COLON
                + r"|"
                + r"\s*"
                + "(?:"  # <-- non-capturing group
                + "|".join([re.escape(key) for key in sorted(set(aliases))])
                + "))"
            )

        # numbers which cannot be book numbers, when not followed by ':'
        # if it's 4..999, then in regexp that's 4-9 or a 2 or 3 digit number
        regexp_parts.append(
            f"(?:[{len(regexp_parts) + 1}-9]|" + r"\d{2,3}" + f")(?!{COLON})"
        )
        VERSE_NUMBER = r"|".join(regexp_parts)
        REGEXP = f"(?:{RANGE}|{NUMBER})(?:\\,\\s*(?:{RANGE}|(?:{VERSE_NUMBER}){END}))*"
        return REGEXP

    def numerical_book_prefixes(self, reverse=True) -> List[str]:
        prefixes = set()
        for key in self.book_aliases.keys():
            part_1 = key.split(" ")[0]
            if part_1.isdigit():
                prefixes.add(part_1)
        return sorted(prefixes, reverse=reverse)

    def build_brackets_regexp(self) -> str:
        return r"[\(\)]"

    def generate_references(
        self, text: str, include_books: bool = False, include_nones: bool = False
    ) -> Generator[Tuple[str, Reference | None], None, None]:
        """
        Match references and parentheses separately, then take the next lowest
        item (by starting match position) from the regexp match generators, and
        process. Yield references for book names and chapter/verse numbers.

        This is the base function used by `__.find_references()` and
        `__.first_reference()`.

        Args:
            text: In which to find references
            include_books: Whether to match book names alone
            include_nones: Whether to match malformed references
        """
        brackets_matches = self.brackets_regexp.finditer(text)
        reference_matches = self.reference_regexp.finditer(text)

        bracket_stack = []

        brackets_match = next(brackets_matches, None)
        reference_match = next(reference_matches, None)

        unnumbered_book_aliases = get_unnumbered_book_aliases(self.book_aliases)

        while reference_match or brackets_match:
            # Handle the start or end of a bracket
            # 0 means bracket, 1 means reference
            values = [
                brackets_match.start() if brackets_match else math.inf,
                reference_match.start() if reference_match else math.inf,
            ]

            book_ref = None
            index_of_minimum = values.index(min(values))

            if brackets_match and index_of_minimum == 0:
                if brackets_match.group(0) == "(":
                    if len(bracket_stack) > 0:
                        bracket_stack.append(bracket_stack[-1])
                if brackets_match.group(0) == ")":
                    if len(bracket_stack) > 0:
                        del bracket_stack[-1]
                brackets_match = next(brackets_matches, None)

            if reference_match and index_of_minimum == 1:
                match_str, book_name, match_with_book, match_without_book = (
                    reference_match.groups()
                )
                try:
                    if book_name:
                        respaced_book_name = add_space_after_book_number(
                            normalize_spacing(trim_trailing_period(book_name)),
                            unnumbered_book_aliases,
                            self.language.number_prefixes,
                        )

                        if respaced_book_name in self.book_aliases:
                            library_id, book_id = self.book_aliases[respaced_book_name]
                            book = self.books[library_id, book_id]
                            last_range = book_reference(
                                library_id, book_id
                            ).last_range()
                            if match_with_book:
                                if matches := match_chapter_range(match_with_book):
                                    # Rom 1:2-3:4
                                    book_ref = make_chapter_range(last_range, matches)
                                    if book_ref is not None or include_nones:
                                        yield (match_str, book_ref)
                                elif matches := match_chapter_verses(match_with_book):
                                    # Rom 3:4,6-9
                                    book_ref = make_chapter_verses(last_range, matches)
                                    if book_ref is not None or include_nones:
                                        yield (match_str, book_ref)
                                elif matches := match_number_ranges(match_with_book):
                                    if book.chapters == 1:
                                        # Phlm 3-4 (verse)
                                        v = verse_range(
                                            last_range.start.library,
                                            last_range.start.book,
                                            1,
                                            1,
                                        )
                                        book_ref = make_number_ranges(v, matches)
                                        if book_ref is not None or include_nones:
                                            yield (match_str, book_ref)
                                    if book.chapters > 1:
                                        # Rom 3-4 (chapter)
                                        book_ref = make_number_ranges(
                                            last_range, matches, as_chapters=True
                                        )
                                        if book_ref is not None or include_nones:
                                            yield (match_str, book_ref)
                                else:
                                    yield (match_str, None)
                            else:  # no associated reference
                                if bracket_stack:
                                    bracket_stack[-1] = last_range
                                else:
                                    bracket_stack.append(last_range)
                                if include_books and (
                                    trim_trailing_period(match_str)
                                    not in self.language.ambiguous_aliases
                                ):
                                    yield (
                                        match_str,
                                        book_reference(library_id, book_id),
                                    )
                    elif match_without_book:
                        if bracket_stack:
                            last_range = bracket_stack[-1]
                            library_id, book_id = (
                                last_range.start.library,
                                last_range.start.book,
                            )
                            if matches := match_chapter_range(match_without_book):
                                # 1:2-3:4
                                book_ref = make_chapter_range(last_range, matches)
                                if book_ref is not None or include_nones:
                                    yield (match_without_book, book_ref)
                            elif matches := match_chapter_verses(match_without_book):
                                # 3:4,6-9
                                book_ref = make_chapter_verses(last_range, matches)
                                if book_ref is not None or include_nones:
                                    yield (match_without_book, book_ref)
                            elif matches := match_number_ranges(match_without_book):
                                # v.2, vv.3-4
                                book_ref = make_number_ranges(last_range, matches)
                                if book_ref is not None or include_nones:
                                    yield (match_without_book, book_ref)
                            else:
                                if include_nones:
                                    yield (match_without_book, None)
                        else:
                            if include_nones:
                                yield (match_without_book, None)

                except ValueError:
                    if include_nones:
                        yield (match_str or match_without_book, None)

                if book_ref:
                    last_range = book_ref.ranges[-1]
                    if bracket_stack:
                        bracket_stack[-1] = last_range
                    else:
                        bracket_stack.append(last_range)

                reference_match = next(reference_matches, None)


def match_chapter_range(text) -> Match | None:
    """Match a pair of chapter-and-verse references.

    Example:
        `Rom 1:2-3:4`
    """
    if match := CHAPTER_RANGE_CAPTURE.search(text):
        return match
    return None


def make_chapter_range(last: Range, match: Match) -> Reference | None:
    """Create pair of chapter-and-verse references from a match.

    See `match_chapter_range`.

    Example:
        `Rom 1:2-3:4`
    """
    if last.is_same_book():
        c1, v1, c2, v2 = match.groups()
        return reference(
            range(
                verse(
                    last.start.library,
                    last.start.book,
                    parse_number(c1),
                    parse_number(v1),
                ),
                verse(
                    last.end.library, last.end.book, parse_number(c2), parse_number(v2)
                ),
            )
        )
    return None


def match_chapter_verses(text) -> Match | None:
    """Match a verse list preceded by a chapter marker.

    Example:
        `Rom 3:4,6-9`
    """
    if match := CHAPTER_VERSES_CAPTURE.search(text):
        return match
    return None


def make_chapter_verses(last: Range, match: Match) -> Reference | None:
    """Create a reference from verse list preceded by a chapter marker.

    See `match_chapter_verses`.

    Example:
        `Rom 3:4,6-9`
    """
    if last.is_same_book():
        chapter, numbers = match.groups()
        if range_match := match_number_ranges(numbers):
            last_range = range(
                verse(last.start.library, last.start.book, int(chapter), 1),
                verse(last.end.library, last.end.book, int(chapter), 999),
            )
            if reference := make_number_ranges(last_range, range_match):
                return reference
    return None


def match_number_ranges(text) -> List[str]:
    """Match a list of numbers and number ranges.

    Example:
        `Phlm 1,3-4` (verse), `Rom 1,3-4` (chapter)
    """
    return RANGE_OR_NUMBER_COMPILED.findall(text)


def make_number_ranges(
    last: Range, matches: List[str], as_chapters: bool = False
) -> Reference | None:
    """Create a reference from a list of numbers and number ranges.

    Args:
        last: a verse to which this number list is relative.
        matches: the result of `match_number_ranges()`
        as_chapters: Treat these numbers as chapters rather than verses.

    Example:
        `Phlm 3-4` (verse), `Rom 3-4` (chapter)

    Note:
        If the end number is less than the start number, we check whether it
        might be an abbreviated reference. `123-24` or even `17-8` can be
        interpreted as `123-124` and `17-18` respectively. We test whether the
        second number has fewer digits than the first.
    """
    ranges = []
    for text in matches:
        if range_matches := RANGE_CAPTURE.match(text):
            start, end = range_matches.group(1, 2)
        elif number_matches := NUMBER_CAPTURE.match(text):
            start = end = number_matches.group(1)
        else:
            continue
        if parse_number(end) < parse_number(start):
            if new_end := infer_abbreviation(start, end):
                end = new_end
            else:
                return None
        if as_chapters:
            if last.is_same_book():
                ranges.append(
                    range(
                        verse(
                            last.start.library, last.start.book, parse_number(start), 1
                        ),
                        verse(last.end.library, last.end.book, parse_number(end), 999),
                    )
                )
        else:
            if last.is_same_chapter():
                ranges.append(
                    range(
                        verse(
                            last.start.library,
                            last.start.book,
                            last.start.chapter,
                            parse_number(start),
                        ),
                        verse(
                            last.end.library,
                            last.end.book,
                            last.end.chapter,
                            parse_number(end),
                        ),
                    )
                )
    if ranges:
        return reference(*ranges)
    else:
        return None


def escape_book_name(name: str) -> str:
    """Regexp escape a name, but match multiple spaces.

    This covers line wrapping, indentation, and so on, in the middle of a book
    name.
    """
    return r"\s+".join([re.escape(_) for _ in name.split(" ")])


def long_names_first(names: List[str]) -> List[str]:
    """Remove duplicates and sort descending."""
    return sorted(set(names), key=len)[::-1]


def infer_abbreviation(start: str, end: str) -> str | None:
    """If a number range ends with a smaller number, try to infer an abbreviation.

    If the end number has fewer digits the the start number then we return a
    copy of the start number with its final digits overprinted by the end
    number.

    * In `123-24`, `24` clearly means `124`.
    * In `12-4`, `4` should probably be interpreted as `14`.
    * In `9-4`, `4` is simply a wrong number. We could guess `14`, but it's too
        uncertain.

    Returns:
        None: if no inference is made.
    """
    if int(end) < int(start):
        if len(end) < len(start):
            return start[: 0 - len(end)] + end
        else:
            return None
    return end
