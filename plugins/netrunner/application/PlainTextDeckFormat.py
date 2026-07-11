from re import compile

from plugins.abstraction_base.application.DeckFormatAdapter import DeckFormat
from plugins.abstraction_base.domain.Card import Card
from plugins.netrunner.infrastructure.IsValidSet import is_valid_set

class PlainTextDeckFormat(DeckFormat[Card]):

    PATTERN = compile(r'^(?:(\d+)x\s+)?(.+?)(?:\s+)?(?:\((.+)\))?\s*(?:[•●\s]+)?$') # '{Quantity}x {Name} ({Set})' where Quantity and Set are optional and the text is possibly followed by influence pips "•"

    def __init__(self):
        super().__init__()

    async def is_card_line_of_format(self, card_line):
        match = self.PATTERN.match(card_line)
        print('is_card_line', card_line, bool(match))
        if match:
            set_name = match.group(3).strip() if match.group(3) is not None else None
            return await is_valid_set(set_name) if set_name is not None else True
        else:
            return False

    async def extract_card_data_from_card_line(self, card_line, index):
        print('extract', card_line)
        match = self.PATTERN.match(card_line)
        if match:
            quantity = 1 if match.group(1) is None else int(match.group(1).strip())
            name = match.group(2).strip()
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