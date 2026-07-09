from enum import Enum
from pathlib import Path

from plugins.abstraction_base.application.GamePluginAdapter import GamePlugin
from plugins.yugioh.application.YDKDeckFormat import YDKDeckFormat
from plugins.yugioh.application.YDKEDeckFormat import YDKEDeckFormat
from plugins.abstraction_base.infrastructure.CachedImageRepository import CachedImageRepository
from plugins.abstraction_base.infrastructure.ImageCacheAdapter import ImageCacheAdapter
from plugins.yugioh.infrastructure.YGOProDeckImageSearcher import YGOProDeckImageSearcher

GAME_NAME = 'yugioh'

class YugiohDeckFormats(Enum):
    YDK  = 'ydk'
    YDKE = 'ydke'

INLINE_DECK_FORMATS = [ YugiohDeckFormats.YDKE ]

class YugiohPlugin(GamePlugin):

    is_inline_format: bool = False

    def __init__(self, format: YugiohDeckFormats):
        image_cache = ImageCacheAdapter(GAME_NAME)
        image_search = YGOProDeckImageSearcher()
        self.image_repository = CachedImageRepository(image_cache, image_search)
        
        match format:
            case YugiohDeckFormats.YDK:
                self.format = YDKDeckFormat()
            case YugiohDeckFormats.YDKE:
                self.format = YDKEDeckFormat()

        self.is_inline_format = format in INLINE_DECK_FORMATS

    async def parse_deck(self, decklist):
        is_decklist_a_file: bool = Path(decklist).exists()

        if self.is_inline_format and not is_decklist_a_file:
            deck_text = decklist.replace('"', '')
        else:
            with open(decklist, 'r') as deck_file:
                if isinstance(self.format, YDKEDeckFormat):
                    deck_text = deck_file.read()
                else:
                    deck_text = deck_file.read().splitlines()
        return await super().parse_deck(deck_text)

    async def save_deck(self, deck):
        return await super().save_deck(deck)
