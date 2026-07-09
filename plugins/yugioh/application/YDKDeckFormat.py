from plugins.abstraction_base.application.DeckFormatAdapter import DeckFormat
from plugins.abstraction_base.domain.Card import Card
from plugins.abstraction_base.domain.Deck import Deck

class YDKDeckFormat(DeckFormat[Card]):

    DECK_SECTIONS = {"#main": [], "#extra": [], "!side": []}

    def __init__(self):
        super().__init__()

    async def is_card_line_of_format(self, card_line):
        return card_line.isdigit()

    async def extract_card_data_from_card_line(self, card_line, index):
        pass
    
    async def parse_decklist(self, decklist):
        
        cards_of_deck: list[Card] = []

        card_index = 0
        for card_line in decklist:
            if not card_line or card_line in self.DECK_SECTIONS: continue

            is_card = await self.is_card_line_of_format(card_line)
            if not is_card: continue

            card_index += 1
            extracted_card: Card = Card(
                id = card_line,
                name = card_line,
                quantity = 1,
                placements = [card_index],
                front_image = None,
                back_image = None
            )
            print(extracted_card.id, extracted_card.name, extracted_card.quantity)
            cards_of_deck.append(extracted_card)

        return Deck(cards=cards_of_deck)