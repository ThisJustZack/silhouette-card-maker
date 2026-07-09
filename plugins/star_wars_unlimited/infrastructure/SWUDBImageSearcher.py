from __future__ import annotations

from typing import Optional
from re import compile, sub
from urllib.parse import quote
from io import BytesIO

from plugins.star_wars_unlimited.domain.StarWarsUnlimitedCard import StarWarsUnlimitedCard
from plugins.abstraction_base.domain.CardImage import CardImage
from plugins.abstraction_base.infrastructure.ImageCachePort import DEFAULT_IMAGE_CACHE_PATH, DEFAULT_IMAGE_CONTENT_TYPE, DEFAULT_IMAGE_FORMAT
from plugins.abstraction_base.infrastructure.ImageSearcherPort import ImageSearcherLike

from plugins.abstraction_base.infrastructure.ImageManipulation import prepare_for_image_manipulation
from plugins.abstraction_base.infrastructure.WebRequest import perform_web_request

SWUDB_NAME_URL_TEMPLATE = 'https://swudb.com/api/search/{NAME}{TITLE_QUERY}?grouping=cards&sortorder=setno&sortdir=desc'
SWUDB_ART_URL_TEMPLATE  = 'https://swudb.com/images/cards/{CARD_REF}'

class SWUDBImageSearcher(ImageSearcherLike[StarWarsUnlimitedCard]):

    CARD_ID_PATTERN = compile(r'^(.+)-(.+)$')

    async def find_image(self, card: StarWarsUnlimitedCard) -> Optional[CardImage]:

        title_query = '' if card.title == '' else f' title:"{quote(card.title)}"'
        name_response = await perform_web_request(SWUDB_NAME_URL_TEMPLATE.format(NAME=card.name, TITLE_QUERY=title_query))
        printings = name_response.json().get('printings', [])

        if not printings:
            return

        printing = printings[0]
        card_image = await perform_web_request(SWUDB_ART_URL_TEMPLATE.format(CARD_REF=sub('.+cards/', '', printing.get('frontImagePath'))))

        if card_image != None:
            prepared_image = await prepare_for_image_manipulation(card_image.content)

            if prepared_image.height < prepared_image.width:
                prepared_image = prepared_image.rotate(90, expand=True)

            image_buffer = BytesIO()
            prepared_image.save(image_buffer, format=DEFAULT_IMAGE_FORMAT)

            return CardImage(filename = DEFAULT_IMAGE_CACHE_PATH.format(CARD_ID=card.id),
                                content_type = DEFAULT_IMAGE_CONTENT_TYPE,
                                data = image_buffer.getvalue())
