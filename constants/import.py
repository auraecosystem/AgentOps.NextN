import random

from arcengine import (
    ARCBaseGame,
    Camera,
    GameAction,
    Level,
    Sprite,
)

BACKGROUND_COLOR = 0  
PADDING_COLOR = 4     

# Available colors for sprites (excluding all black -> white colors for visibility)
SPRITE_COLORS = [6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

# Parameters for Procedural Generation
MIN_SIZE = 1
MAX_SIZE = 4
