from context import *

from refspy.reference import is_book_reference
from refspy.refspy import refspy
from refspy.utils import sequential_replace

URL = "https://github.com/eukras/refspy/refspy/docs/demo.py"

__ = refspy()

text = """
Bible references look like Rom 1:1,6-7, 1 Cor 2-3, or Phlm 2-3, with no spaces
in the number part. Whereas '2-3' indicates verses in Philemon it indicates
whole chapters in 1 Corinthians. If we've already mentioned a book like Second
Corinthians or II Cor (allowing line wrapping), we'll want to identify
subsequent references, like 5:21 or vv.25,37-38, by the last mentioned book or
reference, like a human reader. If we refer to say Hebrews (but then Revelation
in parentheses), subsequent references like 10:10 will still be to Hebrews. 
"""

matches = __.find_references(text, include_books=True)
strs, tags = [], []
for match_str, ref in matches:
    strs.append(match_str)
    if is_book_reference(ref):
        tags.append(f'<span class="yellow">{match_str}</span>')
    else:
        tags.append(
            f'<span class="green">{match_str}</span><sup>{__.abbrev(ref)}</sup>'
        )
index = []
for library, book_collation in __.collate(
    sorted([ref for _, ref in matches if not is_book_reference(ref)])
):
    for book, reference_list in book_collation:
        new_reference = __.merge(reference_list)
        index.append(__.abbrev(new_reference))


print("""
<html>
    <head>
        <style>
            a { text-decoration: none; }
            sup { font-family: sans-serif; font-size: xx-small;
                  color: purple; padding: 1px 3px; border: 1px solid purple;
                  border-radius: 3px; margin-left: 2px; }
            .green { background-color: #aaffaa; }
            .yellow { background-color: #ffffaa; }
        </style>
    </head>
    <body>
        <p><b>REFSPY</b>. <i>A Python library for biblical referencing.</i></p>
        <p>In the text below, references are highlighted in green, while book
        names that aren't themselves references, but are used for context, are
        highlighted in yellow. The identified references are noted in
        superscript, and an index is compiled at the end.

""")
print(f"""
    <pre>{text}</pre>
    <p>{sequential_replace(text, strs, tags)}</p>
    <p><b>Index</b>. {"; ".join(index)}</p>
    <p>Generated by: <a href="{URL}">{URL}</a><p>
</html>
""")