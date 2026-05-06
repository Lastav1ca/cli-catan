import Buildings
from BoardReader import get_hex_grid

class Game:
    def __init(self):
        self.players = []
        self.settlements = []
        self.cities = []
        self.roads = []

    def create_settlement(self, player, position):
        settlement = Buildings.Settlement(player, position)
        self.settlements.append(settlement)

    def create_city(self, player, position):
        city = Buildings.City(player, position)
        self.settlements.append(city)

    def create_road(self, player, vertex1, vertex2):
        road = Buildings.Road(player, vertex1, vertex2)
        self.settlements.append(road)

    def print_hex_grid(self):
        grid = get_hex_grid()

        for row_idx, line in enumerate(grid):
            print(line)