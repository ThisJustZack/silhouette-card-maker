from enum import Enum

class CardFace(str, Enum):
    FRONT = 'face'
    BACK  = 'reverse'