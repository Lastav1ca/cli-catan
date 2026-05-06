import Buildings
from BoardReader import get_hex_grid
from BoardWriter import insert_city, insert_settlement
from Player import player_colors_codes, PlayerColor

class Game:
    def __init__(self):
        self.players = []
        self.settlements = {}
        self.cities = {}
        self.roads = {}

    def create_settlement(self, player, position):
        settlement = Buildings.Settlement(player, position)

        self.settlements[position] = player # adding the physical settlement to dictionary with the player it belongs to

        insert_settlement(position) # inserting S into position on grid

    def create_city(self, player, position):

        city = Buildings.City(player, position)

        self.cities[position] = player # adding the physical city to dictionary with the player it belongs to

        insert_city(position) # inserting C into position on grid

    def create_road(self, player, vertex1, vertex2):
        road = Buildings.Road(player, vertex1, vertex2)
        road_type, road_positions = road.get_road_info() 
        for road_position in road_positions:
            self.roads[road_position] = player # adding the physical road parts to dictionary with player it belongs to
            print(f'Road position: {road_position} \n')

    def print_hex_grid(self):
        grid = get_hex_grid() 

        for row_idx, line in enumerate(grid):

            replacements = [] # List of replacements (tuples) in each line to print
                              # 1. position, 2. value, 3. color
            
            for col_idx, col in enumerate(line):
                #print(f'Currently at {(col_idx, row_idx)} \n')

                if col == 'S':

                    owner = self.settlements[(col_idx, row_idx)]

                    color_code = player_colors_codes[owner.color]

                    replacements.append((col_idx, 'S', color_code))

                if col == 'C':

                    owner = self.cities[(col_idx, row_idx)]

                    color_code = player_colors_codes[owner.color]

                    replacements.append((col_idx, 'C', color_code))

                if col == '/' and (col_idx, row_idx) in self.roads:

                    owner = self.roads[(col_idx, row_idx)]

                    color_code = player_colors_codes[owner.color]

                    replacements.append((col_idx, '/', color_code))

                if col == '\\' and (col_idx, row_idx) in self.roads:

                    owner = self.roads[(col_idx, row_idx)]

                    color_code = player_colors_codes[owner.color]

                    replacements.append((col_idx, '\\', color_code))

                if col == '|' and (col_idx, row_idx) in self.roads:

                    owner = self.roads[(col_idx, row_idx)]

                    color_code = player_colors_codes[owner.color]

                    replacements.append((col_idx, '|', color_code))     

            
            for replacement in reversed(replacements):

                line = line[:replacement[0]] + replacement[2] + replacement[1] + player_colors_codes[0] + line[replacement[0] + 1:]
            
            print(line)

                    
