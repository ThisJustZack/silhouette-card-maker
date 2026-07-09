from json import loads

from plugins.abstraction_base.application.DeckFormatAdapter import DeckFormat
from plugins.star_wars_unlimited.domain.StarWarsUnlimitedCard import StarWarsUnlimitedCard
from plugins.abstraction_base.domain.Deck import Deck

from plugins.star_wars_unlimited.application.get_id_for_scm import get_id_for_scm
from plugins.star_wars_unlimited.infrastructure.MissingInformationSearcher import MissingInformationSearcher

class SWUDBJSONDeckFormat(DeckFormat[StarWarsUnlimitedCard]):

    def __init__(self):
        super().__init__()

    async def is_card_line_of_format(self, card_line):
        return bool(card_line.get('id') and card_line.get('count'))

    async def extract_card_data_from_card_line(self, card_line, index):
        is_card_line = await self.is_card_line_of_format(card_line)
        if is_card_line:
            missing_search = MissingInformationSearcher()
            card_id = card_line.get('id')
            card_quantity = card_line.get('count')
            card_name, card_title = missing_search.get_card_name_and_title(StarWarsUnlimitedCard(id = card_id))
            return StarWarsUnlimitedCard(
                id = get_id_for_scm(name = card_name, title = card_title),
                name = card_name,
                title = card_title,
                quantity = card_quantity,
                placements = [index],
                front_image = None,
                back_image = None
            )
    
    async def parse_decklist(self, decklist):
        cards_of_deck = []

        data = loads(decklist)
        cards = [data.get('leader', {})] + [data.get('base', {})] + data.get('deck', []) + data.get('sideboard', [])

        card_index = 0
        for card in cards:
            is_card_line = await self.is_card_line_of_format(card)
            if is_card_line:
                card_index += 1
                card_data = await self.extract_card_data_from_card_line(card, card_index)
                cards_of_deck.append(card_data)
        
        return Deck(cards=cards_of_deck)