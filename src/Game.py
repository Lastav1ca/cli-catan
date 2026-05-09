import Buildings
from BoardReader import get_hex_grid, is_vertex_empty, is_vertex_adjacent_to_settlement_or_city, get_adjacent_vertices
from BoardWriter import insert_city, insert_settlement
from Player import player_colors_codes, PlayerColor, player_colors_names
from ResourceEnum import resource_emoji, Resource
import random
from Development import DevelopmentCard, KNIGHT_COUNT, ROAD_BUILDING_COUNT, YEAR_OF_PLENTY_COUNT, MONOPOLY_COUNT, VICTORY_POINT_COUNT

class Game:
    def __init__(self):

        self.players = []

        self.settlements = {}
        self.cities = {}
        self.roads = {}
        self.roads_end_points = {} # roads dictionary, but with vertexes as key and player who owns road as value
        
        self.development_cards = self.initialize_development_deck()

    def create_settlement(self, player, position):
        settlement = Buildings.Settlement(player, position)

        self.settlements[position] = player # adding the physical settlement to dictionary with the player it belongs to

        player.add_settlement(settlement)

        insert_settlement(position) # inserting S into position on grid


    def create_city(self, player, position):

        city = Buildings.City(player, position)

        self.cities[position] = player # adding the physical city to dictionary with the player it belongs to

        player.add_city(city)

        insert_city(position) # inserting C into position on grid


    def create_road(self, player, vertex1, vertex2):
        road = Buildings.Road(player, vertex1, vertex2)
        road_type, road_positions = road.get_road_info() 
        for road_position in road_positions:
            self.roads[road_position] = player # adding the physical road parts to dictionary with player it belongs to

            self.roads_end_points[vertex1] = player
            self.roads_end_points[vertex2] = player

            player.add_road(road)
            #print(f'Road position: {road_position} \n')


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

                    
    def roll_dice(self):
        dice1 = random.randint(1, 6)
        dice2 = random.randint(1, 6)

        return dice1 + dice2
    

    def harvest_resources(self, hex_value, grid):

        harvest_hexes = grid.get_hex_by_value(hex_value)

        for hex in harvest_hexes:
            vertices = hex.vertices

            for vertex in vertices:

                if vertex in self.settlements:

                    owner = self.settlements[vertex]

                    owner.resources[hex.resource_yield] += 1

                    if hex.resource_yield == Resource.STONE:

                        print(f'Added: 1 {resource_emoji[hex.resource_yield]}  to {player_colors_names[owner.color]}! \n ')
                    
                    else:

                        print(f'Added: 1 {resource_emoji[hex.resource_yield]} to {player_colors_names[owner.color]}! \n ')
                    

                if vertex in self.cities:

                    owner = self.cities[vertex]

                    owner.resources[hex.resource_yield] += 2

                    if hex.resource_yield == Resource.STONE:

                        print(f'Added: 2 {resource_emoji[hex.resource_yield]}  to {player_colors_names[owner.color]}! \n ')

                    else:

                        print(f'Added: 2 {resource_emoji[hex.resource_yield]} to {player_colors_names[owner.color]}! \n ')


    def is_road_taken(self, vertex1, vertex2):

        if vertex1[1] < vertex2[1]:
            higher_vertex_coordinates = vertex1
            lower_vertex_coordinates = vertex2
        else:
            higher_vertex_coordinates = vertex2
            lower_vertex_coordinates = vertex1

        if higher_vertex_coordinates[0] > lower_vertex_coordinates[0]:
            road_type = f'/'
            road_positions = [(higher_vertex_coordinates[0] - 1, higher_vertex_coordinates[1] + 1), 
                            (higher_vertex_coordinates[0] - 2, higher_vertex_coordinates[1] + 2),
                            (higher_vertex_coordinates[0] - 3, higher_vertex_coordinates[1] + 3)]
        
        elif higher_vertex_coordinates[0] < lower_vertex_coordinates[0]:
            road_type = f'\\'
            road_positions = [(higher_vertex_coordinates[0] + 1, higher_vertex_coordinates[1] + 1), 
                            (higher_vertex_coordinates[0] + 2, higher_vertex_coordinates[1] + 2),
                            (higher_vertex_coordinates[0] + 3, higher_vertex_coordinates[1] + 3)]
        
        else:
            road_type = f'|'
            road_positions = [(higher_vertex_coordinates[0], higher_vertex_coordinates[1] + 1), 
                            (higher_vertex_coordinates[0], higher_vertex_coordinates[1] + 2),
                            (higher_vertex_coordinates[0], higher_vertex_coordinates[1] + 3)]
            
        if road_positions[0] in self.roads:
            return True
        
        return False


    def is_adjacent_to_players_road(self, position, player):

        if(position in self.roads_end_points):
            if(self.roads_end_points[position] == player):
                return True
        
        return False
    

    def is_road_adjacent_to_players_structure(self, vertex1, vertex2, player):

        if vertex1 in self.settlements:
            if self.settlements[vertex1] == player:
                return True
            
        if vertex1 in self.cities:
            if self.cities[vertex1] == player:
                return True
            
        if vertex2 in self.settlements:
            if self.settlements[vertex2] == player:
                return True

        if vertex2 in self.cities:
            if self.cities[vertex2] == player:
                return True
            
        if self.is_adjacent_to_players_road(vertex1, player) or self.is_adjacent_to_players_road(vertex2, player):
            return True
        
        return False
    

    def is_road_blocked(self, vertex1, vertex2, player):

        if vertex1 in self.settlements:
            touching_left, owned_left  = vertex1, self.settlements[vertex1]
        elif vertex1 in self.cities:
            touching_left, owned_left  = vertex1, self.cities[vertex1]
        else:
            touching_left, owned_left  = None, None

        if vertex2 in self.settlements:
            touching_right, owned_right  = vertex2, self.settlements[vertex2]
        elif vertex2 in self.cities:
            touching_right, owned_right  = vertex2, self.cities[vertex2]
        else:
            touching_right, owned_right  = None, None

        if (owned_left != player and touching_left is not None and touching_right is None):
            return True
        if (owned_right != player and touching_right is not None and touching_left is None):
            return True
        
        return False



    def is_players_settlement(self, position, player):

        if position in self.settlements:

            if self.settlements[position] == player:
                return True
        
        return False


    def purchase_settlement(self, player, position):

        if  (player.resources[Resource.BRICK] < 1 or 
        player.resources[Resource.WOOD] < 1 or 
        player.resources[Resource.WHEAT] < 1 or 
        player.resources[Resource.SHEEP] < 1):
            
            print(f'Insufficient funds! \n')
            return
            
        if not is_vertex_empty(position):
                
            print(f'Location unavailable! \n')
            return
        
        if is_vertex_adjacent_to_settlement_or_city(position):

            print(f'Can\'t place settlement there! Another settlement/city is adjacent! \n')
            return

        if not self.is_adjacent_to_players_road(position, player):

            print(f'Can\'t place settlement there! Must have adjacent road of your own connected! \n')
            return

        player.resources[Resource.BRICK] -= 1
        player.resources[Resource.WOOD] -= 1
        player.resources[Resource.WHEAT] -= 1
        player.resources[Resource.SHEEP] -= 1

        self.create_settlement(player, position)
        print(f'{player_colors_names[player.color]} purchased a Settlement!')


    def purchase_city(self, player, position):

        if  (player.resources[Resource.WHEAT] < 2 or 
        player.resources[Resource.STONE] < 3):
            
            print(f'Insufficient funds! \n')
            return
            
        if not self.is_players_settlement(position, player):
            print(f'Must place City on top of your own settlement! \n')
            return

        player.resources[Resource.WHEAT] -= 2
        player.resources[Resource.STONE] -= 3

        self.create_city(player, position)
        print(f'{player_colors_names[player.color]} purchased a City!')


    def purchase_road(self, player, vertex1, vertex2):

        if (player.resources[Resource.BRICK] < 1 or 
        player.resources[Resource.WOOD] < 1):
            print(f'Insufficient funds! \n')
            return
        
        if self.is_road_taken(vertex1, vertex2):
            print(f'Road space is taken! \n')
            return
        
        if not self.is_road_adjacent_to_players_structure(vertex1, vertex2, player):
            print(f'Road must be adjacent to your own road/settlement! \n')
            return
        
        if self.is_road_blocked(vertex1, vertex2, player):
            print(f'Road is blocked \n')
            return
                
        player.resources[Resource.BRICK] -= 1
        player.resources[Resource.WOOD] -= 1

        self.create_road(player, vertex1, vertex2)
        print(f'{player_colors_names[player.color]} purchased a Road!')


    def trade_with_bank(self, player, give_resource, give_amount, get_resource, get_amount):
        player.resources[give_resource] -= give_amount
        player.resources[get_resource] += get_amount

    def trade_with_player(self, player1, player2, give_resource, give_amount, get_resource, get_amount):
        player1.resources[give_resource] -= give_amount
        player2.resources[get_resource] += get_amount

    def initialize_development_deck(self):
        deck = (
            [DevelopmentCard.KNIGHT] * KNIGHT_COUNT + 
            [DevelopmentCard.ROAD_BUILDING] * ROAD_BUILDING_COUNT +
            [DevelopmentCard.MONOPOLY] * MONOPOLY_COUNT + 
            [DevelopmentCard.YEAR_OF_PLENTY] * YEAR_OF_PLENTY_COUNT +
            [DevelopmentCard.VICTORY_POINT] * VICTORY_POINT_COUNT
        )
        random.shuffle(deck)
        return deck
    
