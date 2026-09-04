from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Mapping, Any, Tuple
from re import sub
from unicodedata import normalize

from plugins.abstraction_base.domain.Card import C

from plugins.abstraction_base.infrastructure.WebRequest import perform_web_request

CYBERPUNK_API_URL_TEMPLATE = 'https://api.netdeck.gg/api/cards/cyberpunk?q=n:\"{CARD_NAME}\"&limit=60&offset=0'

@dataclass
class CardPrinting:
    printing_id: str
    slug: str

class CyberpunkPrintingSearcher():
    async def find_printing(self, card: C, print_number: str) -> Optional[CardPrinting]:

		# Replace whitespace with + (ex. 'V - Streetkid', 'Royce - Psycho on the Edge', 'T-Bug - Amateur Philosopher')
        slugified = sub(r'\s+', '+', card.name)
        
        request_response = await perform_web_request(CYBERPUNK_API_URL_TEMPLATE.format(CARD_NAME=slugified))
        
        if request_response != None:
            json_response = request_response.json()
            cards_from_response: Mapping[str, Any] = json_response.get('items') if len(json_response.get('items')) > 0 else []

            for card_of_response in cards_from_response:
                response_print_number = card_of_response.get('print_number').upper()
                if print_number[-(len(response_print_number)):] == response_print_number:
                    return CardPrinting(printing_id=card_of_response.get('printing_id'), slug=card_of_response.get('slug'))
