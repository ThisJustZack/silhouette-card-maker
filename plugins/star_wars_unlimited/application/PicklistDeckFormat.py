from re import compile

from plugins.abstraction_base.application.DeckFormatAdapter import DeckFormat
from plugins.star_wars_unlimited.domain.StarWarsUnlimitedCard import StarWarsUnlimitedCard

from plugins.star_wars_unlimited.application.get_id_for_scm import get_id_for_scm
from plugins.star_wars_unlimited.infrastructure.MissingInformationSearcher import MissingInformationSearcher

class PicklistDeckFormat(DeckFormat[StarWarsUnlimitedCard]):

    PATTERN = compile(r'^((?:\[\s*\]\s*)+)\s*(.+?)\s*(?:\|\s*(.+))?$')

    def __init__(self):
        super().__init__()

    async def is_card_line_of_format(self, card_line):
        stripped = card_line.strip()
        # Skip empty lines, separator lines (-----), and header lines
        if not stripped or stripped.startswith('-') or stripped.startswith('Picklist:'):
            return False
        # Skip card ID lines (e.g., "LAW 003, LAW 267")
        if not stripped.startswith('[') and compile(r'^[A-Z]{2,}\s+\d').match(stripped):
            return False
        return bool(self.PATTERN.match(card_line))

    async def extract_card_data_from_card_line(self, card_line, index):
        match = self.PATTERN.match(card_line)
        if match:
            name = match.group(2).strip()
            title = match.group(3).strip() if match.group(3) else ''
            quantity_group = int(match.group(1).strip())
            quantity = quantity_group.count('[ ]') if quantity_group else 1
            return StarWarsUnlimitedCard(
                id = get_id_for_scm(name = name, title = title),
                name = name,
                title = title,
                quantity = quantity,
                placements = [index for _ in range(quantity)],
                front_image = None,
                back_image = None
            )
    
    async def parse_decklist(self, decklist):
        return await super().parse_decklist(decklist)