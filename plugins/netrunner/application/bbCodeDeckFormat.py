from re import compile

from plugins.abstraction_base.application.DeckFormatAdapter import DeckFormat
from plugins.abstraction_base.domain.Card import Card
from plugins.netrunner.infrastructure.IsValidSet import is_valid_set

class bbCodeDeckFormat(DeckFormat[Card]):

    IDENTITY_PATTERN = compile(r'\[url=(https://netrunnerdb.com/en/card/\d+)\](.+)\[/url\] \((.+)\).*') # '[url={URL}]{Name}[/url] ({Set})'
    PATTERN          = compile(r'(\d+)x \[url=(https://netrunnerdb.com/en/card/\d+)\](.+)\[/url\] \[i\]\((.+)\)\[/i\].*') # '{Quantity}x [url={URL}]{Name}[/url] [i]({Set})[/i]'

    def __init__(self):
        super().__init__()

    async def is_card_line_of_format(self, card_line):
        match = self.PATTERN.match(card_line)
        if match:
            set_name = match.group(4).strip()
            return await is_valid_set(set_name)
        else:
            match = self.IDENTITY_PATTERN.match(card_line)
            if match:
                set_name = match.group(3).strip()
                return await is_valid_set(set_name)
        return False
    
    async def extract_identity_card_data(self, card_line, index):
        match = self.IDENTITY_PATTERN.match(card_line)
        if match:
            name = match.group(2).strip()
            
            return Card(
                id = name,
                name = name,
                quantity = 1,
                placements = [index for _ in range(1)],
                front_image = None,
                back_image = None
            )
    
    async def extract_card_data(self, card_line, index):
        match = self.PATTERN.match(card_line)
        if match:
            name = match.group(3).strip()
            quantity = int(match.group(1).strip())
            
            return Card(
                id = name,
                name = name,
                quantity = quantity,
                placements = [index for _ in range(quantity)],
                front_image = None,
                back_image = None
            )

    async def extract_card_data_from_card_line(self, card_line, index):
        identity_card = await self.extract_identity_card_data(card_line, index)
        card          = await self.extract_card_data(card_line, index)

        return card if card is not None else identity_card
    
    async def parse_decklist(self, decklist):
        return await super().parse_decklist(decklist)