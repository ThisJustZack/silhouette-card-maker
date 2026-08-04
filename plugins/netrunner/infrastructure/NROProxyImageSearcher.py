from __future__ import annotations

from typing import Optional
from re import sub

from plugins.abstraction_base.domain.Card import Card
from plugins.abstraction_base.domain.CardImage import CardImage
from plugins.abstraction_base.infrastructure.ImageCachePort import DEFAULT_IMAGE_CACHE_PATH, DEFAULT_IMAGE_CONTENT_TYPE
from plugins.abstraction_base.infrastructure.ImageSearcherPort import ImageSearcherLike

from plugins.abstraction_base.infrastructure.StringManipulation import normalize_string
from plugins.abstraction_base.infrastructure.WebRequest import perform_web_request

NETRUNNERDB_URL_TEMPLATE = 'https://api.netrunnerdb.com/api/v3/public/cards/{CARD_NAME}'
NRO_PROXY_URL_TEMPLATE = 'https://nro-public.s3.nl-ams.scw.cloud/nro/card-printings/v2/webp/english/card/{PRINT_ID}.webp'

class NROProxyImageSearcher(ImageSearcherLike[Card]):
    async def find_image(self, card: Card, face) -> Optional[CardImage]:

        # Query for card info using a normalized name of Latin scripts
        sanitized   = normalize_string(card.name)
        slugified_1 = sub(r'\s+|-|\.', '_', sanitized).lower() # Replace whitespace, dash, and period with underscores (ex. 'Pressure Spike', 'All-nighter', 'Ansel 1.0')
        slugified_2 = sub(r'_+', '_', slugified_1) # Flatten multiple underscores (ex. 'Dr. Nuka Vrolyck')
        slugified_3 = sub(r'_$', '', slugified_2) # Remove underscore when at the end of the string (ex. 'Melange Mining Corp.')

        print(slugified_3)

        request_response = await perform_web_request(NETRUNNERDB_URL_TEMPLATE.format(CARD_NAME=slugified_3))

        if request_response != None:
            json_response = request_response.json()
            if isinstance(json_response.get('data'), list) is True:
                raise ValueError(f'Could not parse data for card "{card.name}"')

            # Get the latest printing id
            latest_print_id = json_response.get('data', {}).get('attributes', {}).get('latest_printing_id')

            if latest_print_id != None:
                card_image = await perform_web_request(NRO_PROXY_URL_TEMPLATE.format(PRINT_ID=latest_print_id))

                return CardImage(filename = DEFAULT_IMAGE_CACHE_PATH.format(CARD_ID=card.id),
                                content_type = DEFAULT_IMAGE_CONTENT_TYPE,
                                data = card_image.content)
