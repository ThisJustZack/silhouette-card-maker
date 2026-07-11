from re import compile

from plugins.abstraction_base.application.DeckFormatAdapter import DeckFormat
from plugins.abstraction_base.domain.Card import Card
from plugins.netrunner.infrastructure.IsValidSet import is_valid_set

class MarkdownDeckFormat(DeckFormat[Card]):

    PATTERN = compile(r'^(?:\* (\d+)x )?\[(.+)\]\((.+)\) _\((.+)\)_.*$') # '* {Quantity}x [{Name}]({URL}) _({Set})_' where Quantity is optional to support identity cards

    def __init__(self):
        super().__init__()

    async def is_card_line_of_format(self, card_line):
        match = self.PATTERN.match(card_line)
        if match:
            set_name = match.group(4).strip()
            return await is_valid_set(set_name)
        else:
            return False

    async def extract_card_data_from_card_line(self, card_line, index):
        match = self.PATTERN.match(card_line)
        if match:
            name = match.group(2).strip()
            quantity = 1 if match.group(1) is None else int(match.group(1).strip())
            return Card(
                id = name,
                name = name,
                quantity = quantity,
                placements = [index for _ in range(quantity)],
                front_image = None,
                back_image = None
            )
    
    async def parse_decklist(self, decklist):
        return await super().parse_decklist(decklist)