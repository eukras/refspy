from refspy.corpus import get_corpus
from refspy.language import get_language
from refspy.manager import Manager


def refspy(corpus="protestant", locale="en_US"):
    return Manager(get_corpus(corpus, locale), get_language(locale[:2]))
