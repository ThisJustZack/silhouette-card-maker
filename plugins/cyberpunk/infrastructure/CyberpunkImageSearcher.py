from __future__ import annotations

from typing import Optional, Mapping, Any
from re import sub
from unicodedata import normalize

from plugins.abstraction_base.domain.Card import C
from plugins.abstraction_base.domain.CardImage import CardImage
from plugins.abstraction_base.infrastructure.ImageCachePort import DEFAULT_IMAGE_CACHE_PATH, DEFAULT_IMAGE_CONTENT_TYPE
from plugins.abstraction_base.infrastructure.ImageSearcherPort import ImageSearcherLike

from plugins.abstraction_base.infrastructure.WebRequest import perform_web_request

CYBERPUNK_API_URL_TEMPLATE = 'https://api.netdeck.gg/api/cards/cyberpunk/{CARD_NAME}?printing={CARD_ID}'

class CyberpunkImageSearcher(ImageSearcherLike[C]):
    async def find_image(self, card: C, face) -> Optional[CardImage]:
        
        card_response = await perform_web_request(CYBERPUNK_API_URL_TEMPLATE.format(CARD_NAME=card.name, CARD_ID=card.id))


        if card_response != None:
            json_of_response = card_response.json()

            card_image = await perform_web_request(json_of_response.get('image_url'))

            if card_image != None:
                return CardImage(filename = DEFAULT_IMAGE_CACHE_PATH.format(CARD_ID=card.id),
                                content_type = DEFAULT_IMAGE_CONTENT_TYPE,
                                data = card_image.content)
