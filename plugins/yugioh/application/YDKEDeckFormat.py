from base64 import b64decode
from numpy import frombuffer, uint32

from plugins.abstraction_base.application.DeckFormatAdapter import DeckFormat
from plugins.abstraction_base.domain.Card import Card
from plugins.abstraction_base.domain.Deck import Deck

class YDKEDeckFormat(DeckFormat[Card]):

    def __init__(self):
        super().__init__()

    async def is_card_line_of_format(self, card_line):
        pass
    
    async def base64_to_passcodes(self, base64_string):
        return frombuffer(b64decode(base64_string), dtype=uint32).tolist()

    async def extract_card_data_from_card_line(self, card_line, index):
        pass
    
    async def parse_decklist(self, decklist):
        
        cards_of_deck: list[Card] = []
        components = decklist[len("ydke://"):].split('!')

        main  = await self.base64_to_passcodes(components[0])
        extra = await self.base64_to_passcodes(components[1])
        side  = await self.base64_to_passcodes(components[2])

        deck = main + extra + side
        
        card_index = 0
        for card in deck:
            card_index += 1
            extracted_card: Card = Card(
                id = card,
                name = card,
                quantity = 1,
                placements = [card_index],
                front_image = None,
                back_image = None
            )
            cards_of_deck.append(extracted_card)

        return Deck(cards=cards_of_deck)