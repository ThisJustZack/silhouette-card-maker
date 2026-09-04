from enum import Enum
from pathlib import Path

from plugins.abstraction_base.application.GamePluginAdapter import GamePlugin
from plugins.cyberpunk.application.LimitlessDeckFormat import LimitlessDeckFormat
from plugins.cyberpunk.application.CyberpunkTCGURLDeckFormat import CyberpunkTCGURLDeckFormat
from plugins.abstraction_base.infrastructure.CachedImageRepository import CachedImageRepository
from plugins.abstraction_base.infrastructure.ImageCacheAdapter import ImageCacheAdapter
from plugins.cyberpunk.infrastructure.CyberpunkImageSearcher import CyberpunkImageSearcher

GAME_NAME = 'cyberpunk'

class CyberpunkDeckFormats(Enum):
    LIMITLESS = 'limitless'
    CYBERPUNKTCG_URL = 'cyberpunktcg_url'

class CyberpunkPlugin(GamePlugin):

    inline_deck_formats = [ CyberpunkDeckFormats.CYBERPUNKTCG_URL ]

    def __init__(self, format: CyberpunkDeckFormats):
        super().__init__(has_inline_support=True)
        image_cache = ImageCacheAdapter(GAME_NAME)
        image_search = CyberpunkImageSearcher()
        self.image_repository = CachedImageRepository(image_cache, image_search)
        
        match format:
            case CyberpunkDeckFormats.LIMITLESS:
                self.format = LimitlessDeckFormat()
            case CyberpunkDeckFormats.CYBERPUNKTCG_URL:
                self.format = CyberpunkTCGURLDeckFormat()

        self.is_inline_format = format in self.inline_deck_formats

    async def parse_deck(self, decklist):
        is_decklist_a_file: bool = Path(decklist).exists()
        
        if self.is_inline_format and not is_decklist_a_file:
            deck_text = decklist
        else:
            with open(decklist, 'r') as deck_file:
                deck_text = deck_file.read()
        return await super().parse_deck(deck_text)

    async def save_deck(self, deck):
        return await super().save_deck(deck)
