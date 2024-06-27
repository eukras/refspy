from context import *

from refspy.helper import refspy
from refspy.utils import normalize_spacing, sequential_replace


__ = refspy()


def test_normalize_spacing():
    text = "  a  \t\t b    c  \n\r  d   e   "
    assert normalize_spacing(text) == " a b c d e "


def test_sequential_replace():
    text = """
    1 Cor 1; 1 Cor 1:1; 1 Cor 1:1-4
    """
    url = "https://www.biblegateway.com/passage/?search=%s&version=NRSVA"

    matches = __.find_references(text)
    strs = [s for s, _ in matches]
    tags = [f'<a href="{url % __.code(ref)}">{s}</a>' for s, ref in matches]
    html = sequential_replace(text, strs, tags)
    assert html.count("<a href") == 3
    assert html.count("biblegateway.com") == 3
    assert html.count("1cor+1") == 3
    assert html.count("1 Cor 1") == 3
    assert html.count("</a>") == 3
