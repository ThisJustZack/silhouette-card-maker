from pathlib import Path
from typing import Optional

from plugins.abstraction_base.domain.CardFace import CardFace
from plugins.abstraction_base.domain.CardImage import CardImage
from plugins.abstraction_base.infrastructure.ImageCachePort import ImageCacheLike, DEFAULT_IMAGE_CACHE_PATH, DEFAULT_IMAGE_CONTENT_TYPE
from plugins.abstraction_base.infrastructure.EnsurePath import EnsurePath

class ImageCacheAdapter(ImageCacheLike):

    def __init__(self, game: str):
        self.game = game

        image_cache_path = Path('.cache') / 'images'
        self.cache_path = image_cache_path / self.game

        front_cache = self.cache_path / 'front'
        back_cache = self.cache_path / 'double_sided'

        EnsurePath(front_cache)
        EnsurePath(back_cache)

    async def get_face_folder(self, face: CardFace) -> str:
        return 'double_sided' if face == CardFace.BACK else 'front'

    async def get_cached_image_path_by_card_id(self, card_id: str, face: CardFace) -> Path:
        face_folder = await self.get_face_folder(face)
        return self.cache_path / face_folder / DEFAULT_IMAGE_CACHE_PATH.format(CARD_ID=card_id)
    
    async def get_cached_image_path_by_filename(self, filename: str, face: CardFace) -> Path:
        face_folder = await self.get_face_folder(face)
        return self.cache_path / face_folder / filename

    async def get_cached_image(self, card_id, face = CardFace.FRONT):
        cached_image_path = await self.get_cached_image_path_by_card_id(card_id, face)
        try:
            with open(cached_image_path, 'rb') as image_file:
                return CardImage(
                    filename=DEFAULT_IMAGE_CACHE_PATH.format(CARD_ID=card_id),
                    content_type=DEFAULT_IMAGE_CONTENT_TYPE,
                    data=image_file.read()
                )
        except FileNotFoundError:
            return None
    
    async def save_cached_image(self, image, face = CardFace.FRONT):
        if image != None:
            cached_image_path = await self.get_cached_image_path_by_filename(image.filename, face)
            print(face, cached_image_path)
            with open(cached_image_path, 'wb') as image_file:
                image_file.write(image.data)