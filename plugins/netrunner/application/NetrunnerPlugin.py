from enum import Enum

from plugins.abstraction_base.application.GamePluginAdapter import GamePlugin
from plugins.netrunner.application.bbCodeDeckFormat import bbCodeDeckFormat
from plugins.netrunner.application.JintekiDeckFormat import JintekiDeckFormat
from plugins.netrunner.application.MarkdownDeckFormat import MarkdownDeckFormat
from plugins.netrunner.application.PlainTextDeckFormat import PlainTextDeckFormat
from plugins.netrunner.application.TextDeckFormat import TextDeckFormat
from plugins.abstraction_base.infrastructure.CachedImageRepository import CachedImageRepository
from plugins.abstraction_base.infrastructure.ImageCacheAdapter import ImageCacheAdapter
from plugins.netrunner.infrastructure.NROProxyImageSearcher import NROProxyImageSearcher

GAME_NAME = 'netrunner'

class NetrunnerDeckFormats(Enum):
    BBCODE     = 'bbcode'
    JINTEKI    = 'jinteki'
    MARKDOWN   = 'markdown'
    PLAIN_TEXT = 'plain_text'
    TEXT       = 'text'

class NetrunnerPlugin(GamePlugin):

    def __init__(self, format: NetrunnerDeckFormats):
        image_cache = ImageCacheAdapter(GAME_NAME)
        image_search = NROProxyImageSearcher()
        self.image_repository = CachedImageRepository(image_cache, image_search)
        
        match format:
            case NetrunnerDeckFormats.BBCODE:
                self.format = bbCodeDeckFormat()
            case NetrunnerDeckFormats.JINTEKI:
                self.format = JintekiDeckFormat()
            case NetrunnerDeckFormats.MARKDOWN:
                self.format = MarkdownDeckFormat()
            case NetrunnerDeckFormats.PLAIN_TEXT:
                self.format = PlainTextDeckFormat()
            case NetrunnerDeckFormats.TEXT:
                self.format = TextDeckFormat()

    async def parse_deck(self, decklist):
        with open(decklist, 'r', encoding='utf-8') as deck_file:
            deck_text = deck_file.read()
        return await super().parse_deck(deck_text)

    async def save_deck(self, deck):
        return await super().save_deck(deck)
