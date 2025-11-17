from context import *

from refspy import refspy
from refspy.syntax.european import EUROPEAN
from refspy.syntax.international import INTERNATIONAL

fr = refspy("catholic", "fr_FR")  # Default to 'euro'
fr_intl = refspy("catholic", "fr_FR", "intl")


def test_syntax_setup():
    assert fr.matcher.syntax == EUROPEAN
    assert fr_intl.matcher.syntax == INTERNATIONAL


def test_international_syntax():
    assert fr_intl.r("2 Co. 1:4") == fr.r("2 Co 1,4")
    assert fr_intl.r("2 Co 1:4-5") == fr.r("2 Co 1,4-5")
    assert fr_intl.r("2 Co 1:4,6") == fr.r("2 Co 1,4.6")
    assert fr_intl.r("2 Co 1:4,6-7") == fr.r("2 Co 1,4.6-7")
    assert fr_intl.r("Ro 12:1,1-27") == fr.r("Ro 12,1.15-17")
