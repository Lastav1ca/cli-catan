from enum import Enum
from ResourceEnum import Resource

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

player_colors_names = {
    PlayerColor.RED : 'RED',
    PlayerColor.BLUE : 'BLUE',
    PlayerColor.GREEN : 'GREEN',
    PlayerColor.YELLOW : 'YELLOW',
}

class Player:
    def __init__(self, color):
        self.color = color
        self.resources = {
            Resource.SHEEP : 0,
            Resource.WHEAT : 0,
            Resource.WOOD : 0,
            Resource.BRICK : 0,
            Resource.STONE : 0,
        }
        self.owned_settlements = []
        self.owned_cities = []
        self.owned_roads = []
        self.points = 0

    def add_settlement(self, settlement):
        self.owned_settlements.append(settlement)
        self.points += 1

    def add_city(self, city):
        self.owned_cities.append(city)
        self.points += 1

    def add_road(self, road):
        self.owned_roads.append(road)