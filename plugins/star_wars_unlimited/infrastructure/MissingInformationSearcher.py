from re import compile

from plugins.abstraction_base.infrastructure.WebRequest import perform_web_request
from plugins.star_wars_unlimited.domain.StarWarsUnlimitedCard import StarWarsUnlimitedCard

class MissingInformationSearcher:

    CARD_ID_PATTERN = compile(r'([A-Z]+)_(\d+)')
    CARD_NAME_DUEL_PATTERN = compile(r'(.+) \/\/.+') # Chancellor Palpatine // Darth Sidious from TWI_017
    
    SWUDB_CARD_NUMBER_URL_TEMPLATE = 'https://api.swu-db.com/cards/{SET_ID}/{SET_NUMBER}?format=json'

    async def get_card_name_and_title(self, card: StarWarsUnlimitedCard):
        match = self.CARD_ID_PATTERN.match(card.id)
        if match:
            set_id = match.group(1).strip().lower()
            set_number = int(match.group(2).strip())

            # Query for card name
            request_response = await perform_web_request(self.SWUDB_CARD_NUMBER_URL_TEMPLATE.format(SET_ID=set_id, SET_NUMBER=set_number))
            card_information = request_response.json()
            name = card_information.get('Name')
            name_match = self.CARD_NAME_DUEL_PATTERN.match(name)
            if name_match:
                name = name_match.group(1).strip()

            title = card_information.get('Subtitle') or '' if card_information.get('Type') != 'Base' else ''

            # These are incorrectly hosted by swu-db
            if name == 'Darth Tyrannus':
                name = 'Darth Tyranus'
            if title == 'Darth Tyrannus':
                title = 'Darth Tyranus'

            return (name, title)