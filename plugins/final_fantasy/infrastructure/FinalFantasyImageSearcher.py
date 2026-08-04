from __future__ import annotations

from typing import Optional, Mapping, Any
from re import sub
from unicodedata import normalize

from plugins.final_fantasy.domain.FinalFantasyCard import FinalFantasyCard
from plugins.abstraction_base.domain.CardImage import CardImage
from plugins.abstraction_base.infrastructure.ImageCachePort import DEFAULT_IMAGE_CACHE_PATH, DEFAULT_IMAGE_CONTENT_TYPE
from plugins.abstraction_base.infrastructure.ImageSearcherPort import ImageSearcherLike

from plugins.abstraction_base.infrastructure.WebRequest import perform_web_request, WebRequestType, PayloadType

FINAL_FANTASY_API_URL = 'https://fftcg.square-enix-games.com/na/get-cards'

class FinalFantasyImageSearcher(ImageSearcherLike[FinalFantasyCard]):
    async def find_image(self, card: FinalFantasyCard, face) -> Optional[CardImage]:

        print(card.name)
        payload = {
            'language': 'en',
            # When a serial code is provided, search by code only — combining name and
            # code with exactmatch returns no results from the FFTCG API.
            'text': '' if card.id else card.name,
            'type': [],
            'element': [],
            'cost': [],
            'rarity': [],
            'power': [],
            'category_1': [card.category] if card.category else [],
            'set': [],
            'multicard': '',
            'ex_burst': '',
            'code': card.id,
            'special': '',
            'exactmatch': 1
        }

        request_response = await perform_web_request(FINAL_FANTASY_API_URL,
                                                    request_type = WebRequestType.POST,
                                                    request_payload_type = PayloadType.JSON, request_payload = payload)
        
        if request_response != None:
            json_response = request_response.json()
            cards_from_response: Mapping[str, Any] = json_response.get('cards', [])

            image_url = None if not cards_from_response else cards_from_response[0].get('images').get('full')[0]

            if image_url != None:
                card_image = await perform_web_request(image_url)

                return CardImage(filename = DEFAULT_IMAGE_CACHE_PATH.format(CARD_ID=card.id),
                                content_type = DEFAULT_IMAGE_CONTENT_TYPE,
                                data = card_image.content)