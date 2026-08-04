from __future__ import annotations

from enum import Enum
from typing import Protocol, Optional

from plugins.abstraction_base.domain.Card import C
from plugins.abstraction_base.domain.Deck import Deck
from plugins.abstraction_base.application.DeckFormatPort import DeckFormatLike
from plugins.abstraction_base.infrastructure.ImageRepositoryInterface import ImageRepositoryLike

class GamePluginLike(Protocol[C]):

    format: DeckFormatLike[C]
    image_repository: ImageRepositoryLike[C]
    has_inline_formats: bool
    inline_deck_formats: Optional[list[Enum]]
    is_inline_format: bool
    has_double_sided_cards: bool

    def __init__(self, has_inline_support: bool, has_double_sided_cards: bool):
        ...

    def parse_deck(self, decklist: str) -> Deck[C]:
        ...

    def deduplicate_deck(self, deck: Deck[C]) -> Deck[C]:
        ...

    def get_card_images_for_deck(self, deck: Deck[C]) -> Deck[C]:
        ...

    def save_deck(self, deck: Deck[C]) -> None:
        ...

    def run(self, decklist: str) -> None:
        ...
