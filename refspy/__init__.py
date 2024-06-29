from refspy.manager import Manager
from refspy.setup import get_libraries, get_language


def refspy(corpus="protestant", locale="en_US"):
    return Manager(get_libraries(corpus, locale), get_language(locale[:2]))
