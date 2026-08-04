from re import compile

from plugins.abstraction_base.application.DeckFormatAdapter import DeckFormat
from plugins.final_fantasy.domain.FinalFantasyCard import FinalFantasyCard

class UntapDeckFormat(DeckFormat[FinalFantasyCard]):

    PATTERN = compile(r'^(\d+)\s(.+)\s\((.+)\)$') # '{Quantity} {Name} ({Serial Code})'

    def __init__(self):
        super().__init__()

    async def is_card_line_of_format(self, card_line):
        return bool(self.PATTERN.match(card_line))

    async def extract_card_data_from_card_line(self, card_line, index):
        match = self.PATTERN.match(card_line)
        if match:
            quantity = int(match.group(1))
            name = match.group(2).strip()
            card_code = match.group(3).strip()
            return FinalFantasyCard(
                id = card_code,
                name = name,
                quantity = quantity,
                placements = [index for _ in range(quantity)],
                front_image = None,
                back_image = None,
                category = None
            )
    
    async def parse_decklist(self, decklist):
        return await super().parse_decklist(decklist)