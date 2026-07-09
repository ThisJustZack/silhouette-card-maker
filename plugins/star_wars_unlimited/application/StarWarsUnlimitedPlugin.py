from enum import Enum

from plugins.abstraction_base.application.GamePluginAdapter import GamePlugin
from plugins.star_wars_unlimited.application.MeleeDeckFormat import MeleeDeckFormat
from plugins.star_wars_unlimited.application.PicklistDeckFormat import PicklistDeckFormat
from plugins.star_wars_unlimited.application.SWUDBJSONDeckFormat import SWUDBJSONDeckFormat
from plugins.abstraction_base.infrastructure.CachedImageRepository import CachedImageRepository
from plugins.abstraction_base.infrastructure.ImageCacheAdapter import ImageCacheAdapter
from plugins.star_wars_unlimited.infrastructure.SWUDBImageSearcher import SWUDBImageSearcher

GAME_NAME = 'star_wars_unlimited'

class StarWarsUnlimitedDeckFormats(Enum):
    MELEE     = 'melee'
    PICKLIST  = 'picklist'
    SWUDBJSON = 'swudb_json'

class StarWarsUnlimitedPlugin(GamePlugin):

    def __init__(self, format: StarWarsUnlimitedDeckFormats):
        image_cache = ImageCacheAdapter(GAME_NAME)
        image_search = SWUDBImageSearcher()
        self.image_repository = CachedImageRepository(image_cache, image_search)
        
        match format:
            case StarWarsUnlimitedDeckFormats.MELEE:
                self.format = MeleeDeckFormat()
            case StarWarsUnlimitedDeckFormats.PICKLIST:
                self.format = PicklistDeckFormat()
            case StarWarsUnlimitedDeckFormats.SWUDBJSON:
                self.format = SWUDBJSONDeckFormat()

    async def parse_deck(self, decklist):
        with open(decklist, 'r') as deck_file:
            deck_text = deck_file.read()
        return await super().parse_deck(deck_text)

    async def save_deck(self, deck):
        return await super().save_deck(deck)
