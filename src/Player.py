from enum import Enum

class PlayerColor(Enum):
    RED = 1
    BLUE = 2
    GREEN = 3
    YELLOW = 4

player_colors_codes = {
    0 : '\033[0m',
    PlayerColor.RED : f'\033[31m',
    PlayerColor.BLUE : f'\033[34m',
    PlayerColor.GREEN : f'\033[32m',
    PlayerColor.YELLOW : f'\033[33m',
}

class Player:
    def __init__(self, color):
        self.color = color