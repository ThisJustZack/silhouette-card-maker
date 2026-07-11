from re import compile

from plugins.abstraction_base.application.DeckFormatAdapter import DeckFormat
from plugins.abstraction_base.domain.Card import Card
from plugins.netrunner.application.PlainTextDeckFormat import PlainTextDeckFormat

class TextDeckFormat(PlainTextDeckFormat):

    def __init__(self):
        super().__init__()
