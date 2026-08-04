from enum import Enum

from plugins.abstraction_base.application.GamePluginAdapter import GamePlugin
from plugins.final_fantasy.application.OCTGNDeckFormat import OCTGNDeckFormat
from plugins.final_fantasy.application.TTSDeckFormat import TTSDeckFormat
from plugins.final_fantasy.application.UntapDeckFormat import UntapDeckFormat
from plugins.abstraction_base.infrastructure.CachedImageRepository import CachedImageRepository
from plugins.abstraction_base.infrastructure.ImageCacheAdapter import ImageCacheAdapter
from plugins.final_fantasy.infrastructure.FinalFantasyImageSearcher import FinalFantasyImageSearcher

GAME_NAME = 'final_fantasy'

class FinalFantasyDeckFormats(Enum):
    OCTGN              = 'octgn_xml'
    TABLETOP_SIMULATOR = 'tts'
    UNTAP              = 'untap'


class FinalFantasyPlugin(GamePlugin):

    def __init__(self, format: FinalFantasyDeckFormats):
        super().__init__()
        image_cache = ImageCacheAdapter(GAME_NAME)
        image_search = FinalFantasyImageSearcher()
        self.image_repository = CachedImageRepository(image_cache, image_search)
        
        match format:
            case FinalFantasyDeckFormats.OCTGN:
                self.format = OCTGNDeckFormat()
            case FinalFantasyDeckFormats.TABLETOP_SIMULATOR:
                self.format = TTSDeckFormat()
            case FinalFantasyDeckFormats.UNTAP:
                self.format = UntapDeckFormat()

    async def parse_deck(self, decklist):
        with open(decklist, 'r') as deck_file:
            deck_text = deck_file.read()
        return await super().parse_deck(deck_text)

    async def save_deck(self, deck):
        return await super().save_deck(deck)
