from re import compile

from plugins.abstraction_base.application.DeckFormatAdapter import DeckFormat
from plugins.abstraction_base.domain.Card import Card
from plugins.cyberpunk.infrastructure.CyberpunkPrintingSearcher import CyberpunkPrintingSearcher

class LimitlessDeckFormat(DeckFormat[Card]):

    PATTERN = compile(r'^(\d+)\s+(.+)\s+(.+)$') # '{Quantity} {Name} {Card Number}'

    def __init__(self):
        super().__init__()

    async def is_card_line_of_format(self, card_line):
        return bool(self.PATTERN.match(card_line))

    async def extract_card_data_from_card_line(self, card_line, index):
        match = self.PATTERN.match(card_line)
        if match:
            printing_searcher = CyberpunkPrintingSearcher()
            card_printing = match.group(3).strip()
            card_name = match.group(2).strip()
            card_quantity = int(match.group(1).strip())
            card = Card(
                id = card_printing,
                name = card_name,
                quantity = card_quantity,
                placements = [index for _ in range(card_quantity)],
                front_image = None,
                back_image = None
            )
            card_printing = await printing_searcher.find_printing(card, card_printing)
            if card_printing != None:
                card.id = card_printing.printing_id
                card.name = card_printing.slug
            return card
    
    async def parse_decklist(self, decklist):
        return await super().parse_decklist(decklist)