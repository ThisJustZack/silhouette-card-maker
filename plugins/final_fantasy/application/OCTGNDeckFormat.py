from re import compile
from xml.etree import ElementTree

from plugins.abstraction_base.application.DeckFormatAdapter import DeckFormat
from plugins.final_fantasy.domain.FinalFantasyCard import FinalFantasyCard
from plugins.abstraction_base.domain.Deck import Deck

class OCTGNDeckFormat(DeckFormat[FinalFantasyCard]):

    PATTERN = compile(r'^(.+?)\s*\(([^)]+)\)$')  # 'Name (Category)'

    def __init__(self):
        super().__init__()

    async def is_card_line_of_format(self, card_line):
        return card_line.get('qty', 1) and card_line.get('text') and self.PATTERN.match(card_line.get('text'))

    async def extract_card_data_from_card_line(self, card_line, index):
        match = self.PATTERN.match(card_line.get('text'))
        if match:
            quantity = card_line.get('qty', 1)
            name = match.group(1).strip()
            category = match.group(2).strip()
            return FinalFantasyCard(
                id = name,
                name = name,
                quantity = quantity,
                placements = [index for _ in range(quantity)],
                front_image = None,
                back_image = None,
                category = category
            )
    
    async def parse_decklist(self, decklist):

        cards_of_deck = []

        root = ElementTree.fromstring(decklist)

        card_index = 0
        for section in root.findall('section'):
            for card in section.findall('card'):
                is_card_line = await self.is_card_line_of_format(card)
                if is_card_line:
                    card_index += 1
                    card_data = await self.extract_card_data_from_card_line(card, card_index)
                    cards_of_deck.append(card_data)

        return Deck(cards=cards_of_deck)
