import Buildings
from BoardReader import get_hex_grid, is_vertex_empty, is_vertex_adjacent_to_settlement_or_city, get_adjacent_vertices
from BoardWriter import insert_city, insert_settlement, insert_robber
from Player import player_colors_codes, PlayerColor, player_colors_names
from ResourceEnum import resource_emoji, Resource
import random
from Development import DevelopmentCard, KNIGHT_COUNT, ROAD_BUILDING_COUNT, YEAR_OF_PLENTY_COUNT, MONOPOLY_COUNT, VICTORY_POINT_COUNT

class Game:
    def __init__(self, players=None):

        self.players = players if players is not None else []

        self.settlements = {}
        self.cities = {}
        self.roads = {}
        self.roads_end_points = {} # roads dictionary, but with vertexes as key and player who owns road as value

        self.development_cards = self.initialize_development_deck()


    def add_player(self, player):
        self.players.append(player)

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


    def _print_grid_axes_header(self, width):
        row_label_pad = '    '  # matches "{row:3} " prefix width
        tens = ''.join(str(c // 10) if c >= 10 else ' ' for c in range(width))
        ones = ''.join(str(c % 10) for c in range(width))
        print(row_label_pad + tens)
        print(row_label_pad + ones)


    def print_hex_grid(self):
        grid = get_hex_grid()

        max_width = max((len(line.rstrip('\n')) for line in grid), default=0)
        self._print_grid_axes_header(max_width)

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

            print(f'{row_idx:3} {line}', end='')

                    
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
        player1.resources[get_resource] += get_amount

        player2.resources[get_resource] -= get_amount
        player2.resources[give_resource] += give_resource


    def purchase_development_card(self, player):
        if (player.resources[Resource.SHEEP] < 1 or
            player.resources[Resource.WHEAT] < 1 or
            player.resources[Resource.STONE] < 1):
            print(f'Insufficient funds! \n')
            return

        if not self.development_cards:
            print(f'Development card deck is empty! \n')
            return

        player.resources[Resource.SHEEP] -= 1
        player.resources[Resource.WHEAT] -= 1
        player.resources[Resource.STONE] -= 1

        card = self.development_cards.pop()
        player.new_development_cards[card] += 1
        print(f'{player_colors_names[player.color]} bought a Development Card!')


    def end_turn(self, player):
        for card, amount in player.new_development_cards.items():
            player.development_cards[card] += amount
            player.new_development_cards[card] = 0


    def get_players_on_hex(self, hex_obj, exclude=None):
        # returns list of unique players owning a settlement/city on any vertex of hex_obj
        owners = []
        for vertex in hex_obj.vertices:
            owner = None
            if vertex in self.settlements:
                owner = self.settlements[vertex]
            elif vertex in self.cities:
                owner = self.cities[vertex]
            if owner is not None and owner is not exclude and owner not in owners:
                owners.append(owner)
        return owners


    def steal_random_resource(self, thief, victim):
        available = [r for r, amount in victim.resources.items() if amount > 0]
        if not available:
            print(f'{player_colors_names[victim.color]} has no resources to steal! \n')
            return
        stolen = random.choice(available)
        victim.resources[stolen] -= 1
        thief.resources[stolen] += 1
        print(f'{player_colors_names[thief.color]} stole 1 {resource_emoji[stolen]} from {player_colors_names[victim.color]}! \n')


    def play_knight(self, player, hex_num, hexes, victim=None):
        if player.development_cards[DevelopmentCard.KNIGHT] < 1:
            print(f'No Knight cards to play! \n')
            return

        if not 1 <= hex_num <= len(hexes):
            print(f'Hex index {hex_num} out of range! \n')
            return

        player.development_cards[DevelopmentCard.KNIGHT] -= 1

        insert_robber(hex_num, hexes)

        target_hex = hexes[hex_num - 1]
        candidates = self.get_players_on_hex(target_hex, exclude=player)

        if not candidates:
            print(f'No players to steal from on this hex. \n')
            return

        if victim is None:
            victim = candidates[0]
        elif victim not in candidates:
            print(f'{player_colors_names[victim.color]} has no buildings on that hex! \n')
            return

        self.steal_random_resource(player, victim)


    def play_road_building(self, player, road1_v1, road1_v2, road2_v1, road2_v2):
        if player.development_cards[DevelopmentCard.ROAD_BUILDING] < 1:
            print(f'No Road Building cards to play! \n')
            return

        if self.is_road_taken(road1_v1, road1_v2):
            print(f'First road space is taken! \n')
            return
        if not self.is_road_adjacent_to_players_structure(road1_v1, road1_v2, player):
            print(f'First road must be adjacent to your own road/settlement! \n')
            return
        if self.is_road_blocked(road1_v1, road1_v2, player):
            print(f'First road is blocked! \n')
            return

        # card is consumed once we start placing — second road can chain off the first
        player.development_cards[DevelopmentCard.ROAD_BUILDING] -= 1
        self.create_road(player, road1_v1, road1_v2)

        if self.is_road_taken(road2_v1, road2_v2):
            print(f'Second road space is taken! Forfeited. \n')
            return
        if not self.is_road_adjacent_to_players_structure(road2_v1, road2_v2, player):
            print(f'Second road must be adjacent to your own road/settlement! Forfeited. \n')
            return
        if self.is_road_blocked(road2_v1, road2_v2, player):
            print(f'Second road is blocked! Forfeited. \n')
            return

        self.create_road(player, road2_v1, road2_v2)
        print(f'{player_colors_names[player.color]} played Road Building!')


    def play_year_of_plenty(self, player, resource1, resource2):
        if player.development_cards[DevelopmentCard.YEAR_OF_PLENTY] < 1:
            print(f'No Year of Plenty cards to play! \n')
            return

        player.development_cards[DevelopmentCard.YEAR_OF_PLENTY] -= 1
        player.resources[resource1] += 1
        player.resources[resource2] += 1
        print(f'{player_colors_names[player.color]} played Year of Plenty: +1 {resource_emoji[resource1]} +1 {resource_emoji[resource2]} \n')


    def play_monopoly(self, player, resource):
        if player.development_cards[DevelopmentCard.MONOPOLY] < 1:
            print(f'No Monopoly cards to play! \n')
            return

        player.development_cards[DevelopmentCard.MONOPOLY] -= 1

        total = 0
        for other in self.players:
            if other is player:
                continue
            total += other.resources[resource]
            other.resources[resource] = 0

        player.resources[resource] += total
        print(f'{player_colors_names[player.color]} monopolized {resource_emoji[resource]} and took {total}! \n')


    def play_victory_point(self, player):
        if player.development_cards[DevelopmentCard.VICTORY_POINT] < 1:
            print(f'No Victory Point cards to play! \n')
            return

        player.development_cards[DevelopmentCard.VICTORY_POINT] -= 1
        player.points += 1
        print(f'{player_colors_names[player.color]} gained 1 Victory Point! \n')


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


    # ---------- Helpers for the core game loop ----------

    RESOURCE_INPUT_MAP = {
        'wood': Resource.WOOD,
        'brick': Resource.BRICK,
        'sheep': Resource.SHEEP,
        'wheat': Resource.WHEAT,
        'stone': Resource.STONE,
    }

    DEV_CARD_INPUT_MAP = {
        'knight': DevelopmentCard.KNIGHT,
        'road': DevelopmentCard.ROAD_BUILDING,
        'yop': DevelopmentCard.YEAR_OF_PLENTY,
        'monopoly': DevelopmentCard.MONOPOLY,
        'vp': DevelopmentCard.VICTORY_POINT,
    }


    def _parse_vertex(self, raw):
        try:
            parts = raw.replace('(', '').replace(')', '').split(',')
            return (int(parts[0].strip()), int(parts[1].strip()))
        except (ValueError, IndexError):
            return None


    def _parse_resource(self, raw):
        return self.RESOURCE_INPUT_MAP.get(raw.strip().lower())


    def _prompt_vertex(self, msg):
        while True:
            raw = input(msg)
            v = self._parse_vertex(raw)
            if v is not None:
                return v
            print('Bad vertex format. Use "col,row" e.g. "10,4".')


    def _prompt_resource(self, msg):
        while True:
            raw = input(msg)
            r = self._parse_resource(raw)
            if r is not None:
                return r
            print('Bad resource. Choose from: wood, brick, sheep, wheat, stone.')


    def _prompt_int(self, msg, lo, hi):
        while True:
            raw = input(msg)
            try:
                n = int(raw.strip())
                if lo <= n <= hi:
                    return n
            except ValueError:
                pass
            print(f'Enter an integer between {lo} and {hi}.')


    def get_hexes_for_vertex(self, vertex, board):
        return [h for h in board.hexes if vertex in h.vertices]


    def total_resources(self, player):
        return sum(player.resources.values())


    # ---------- Setup phase ----------

    def place_initial_settlement(self, player, position):
        if not is_vertex_empty(position):
            print(f'Location unavailable! \n')
            return False
        if is_vertex_adjacent_to_settlement_or_city(position):
            print(f"Can't place settlement there! Another settlement/city is adjacent! \n")
            return False
        self.create_settlement(player, position)
        return True


    def place_initial_road(self, player, vertex1, vertex2, anchor):
        if anchor not in (vertex1, vertex2):
            print(f'Initial road must touch the settlement you just placed ({anchor})! \n')
            return False
        if self.is_road_taken(vertex1, vertex2):
            print(f'Road space is taken! \n')
            return False
        self.create_road(player, vertex1, vertex2)
        return True


    def grant_starting_resources(self, player, position, board):
        for hex_obj in self.get_hexes_for_vertex(position, board):
            if hex_obj.resource_yield == Resource.DESERT:
                continue
            player.resources[hex_obj.resource_yield] += 1
            print(f'  +1 {resource_emoji[hex_obj.resource_yield]} from hex {hex_obj.value}')


    def setup_phase(self, board):
        print('\n========== SETUP PHASE ==========')
        order = list(self.players) + list(reversed(self.players))

        for round_idx, player in enumerate(order):
            is_second_round = round_idx >= len(self.players)
            label = '2nd' if is_second_round else '1st'
            print(f"\n{player_colors_names[player.color]}'s {label} placement")

            self.print_hex_grid()

            while True:
                pos = self._prompt_vertex('  Settlement vertex (col,row): ')
                if self.place_initial_settlement(player, pos):
                    break

            self.print_hex_grid()

            while True:
                v1 = self._prompt_vertex('  Road vertex 1 (col,row): ')
                v2 = self._prompt_vertex('  Road vertex 2 (col,row): ')
                if self.place_initial_road(player, v1, v2, pos):
                    break

            if is_second_round:
                print(f'  Starting resources for {player_colors_names[player.color]}:')
                self.grant_starting_resources(player, pos, board)

        print('\n========== SETUP COMPLETE ==========\n')


    # ---------- Robber + dice ----------

    def discard_half(self, player):
        total = self.total_resources(player)
        if total <= 7:
            return
        to_discard = total // 2
        print(f'\n{player_colors_names[player.color]} has {total} resources and must discard {to_discard}.')
        while to_discard > 0:
            print(f'  Current: {self._format_resources(player)}')
            res = self._prompt_resource(f'  Discard which? ({to_discard} left): ')
            if player.resources[res] < 1:
                print('  You have none of that resource.')
                continue
            player.resources[res] -= 1
            to_discard -= 1


    def move_robber_and_steal(self, player, board):
        hex_num = self._prompt_int(f'  Move robber to hex # (1-{len(board.hexes)}): ', 1, len(board.hexes))
        insert_robber(hex_num, board.hexes)
        target_hex = board.hexes[hex_num - 1]
        candidates = self.get_players_on_hex(target_hex, exclude=player)
        if not candidates:
            print('  No players to steal from on this hex.')
            return
        if len(candidates) == 1:
            victim = candidates[0]
        else:
            print('  Players on that hex:')
            for i, c in enumerate(candidates, 1):
                print(f'    {i}. {player_colors_names[c.color]}')
            choice = self._prompt_int('  Steal from #: ', 1, len(candidates))
            victim = candidates[choice - 1]
        self.steal_random_resource(player, victim)


    def handle_seven(self, current_player, board):
        print('\n>>> Rolled a 7! Robber activates. <<<')
        for p in self.players:
            self.discard_half(p)
        print(f'\n{player_colors_names[current_player.color]} moves the robber.')
        self.move_robber_and_steal(current_player, board)


    # ---------- Turn ----------

    def _format_resources(self, player):
        return ' '.join(f'{resource_emoji[r]}x{player.resources[r]}' for r in self.RESOURCE_INPUT_MAP.values())


    def _format_dev_cards(self, player):
        parts = []
        for name, card in self.DEV_CARD_INPUT_MAP.items():
            parts.append(f'{name}:{player.development_cards[card]}')
        return ' '.join(parts)


    def print_player_status(self, player):
        print(f'\n--- {player_colors_names[player.color]} | VP: {player.points} ---')
        print(f'  Resources: {self._format_resources(player)}')
        print(f'  Dev cards (playable): {self._format_dev_cards(player)}')


    def take_turn(self, player, board):
        print(f"\n========== {player_colors_names[player.color]}'s turn ==========")
        input('  Press Enter to roll dice...')
        roll = self.roll_dice()
        print(f'  Rolled: {roll}')

        if roll == 7:
            self.handle_seven(player, board)
        else:
            self.harvest_resources(roll, board)

        self.action_menu(player, board)
        self.end_turn(player)


    def action_menu(self, player, board):
        while True:
            self.print_player_status(player)
            print('  Actions:')
            print('    1. Build road')
            print('    2. Build settlement')
            print('    3. Build city')
            print('    4. Buy development card')
            print('    5. Play development card')
            print('    6. Trade with bank (4:1)')
            print('    7. Show board')
            print('    8. End turn')
            choice = self._prompt_int('  Choose: ', 1, 8)

            if choice == 1:
                v1 = self._prompt_vertex('  Road vertex 1: ')
                v2 = self._prompt_vertex('  Road vertex 2: ')
                self.purchase_road(player, v1, v2)
            elif choice == 2:
                pos = self._prompt_vertex('  Settlement vertex: ')
                self.purchase_settlement(player, pos)
            elif choice == 3:
                pos = self._prompt_vertex('  City vertex: ')
                self.purchase_city(player, pos)
            elif choice == 4:
                self.purchase_development_card(player)
            elif choice == 5:
                self.play_dev_card_menu(player, board)
            elif choice == 6:
                self.trade_with_bank_menu(player)
            elif choice == 7:
                self.print_hex_grid()
            elif choice == 8:
                return

            if self.check_winner() is not None:
                return


    def trade_with_bank_menu(self, player):
        give = self._prompt_resource('  Give resource (4 of): ')
        if player.resources[give] < 4:
            print(f'  Not enough {resource_emoji[give]} (need 4).')
            return
        get = self._prompt_resource('  Get resource (1 of): ')
        if give == get:
            print('  Trade must be different resources.')
            return
        self.trade_with_bank(player, give, 4, get, 1)
        print(f'  Traded 4 {resource_emoji[give]} -> 1 {resource_emoji[get]}')


    def play_dev_card_menu(self, player, board):
        print('  Which card? (knight, road, yop, monopoly, vp)')
        while True:
            raw = input('  Card: ').strip().lower()
            if raw in self.DEV_CARD_INPUT_MAP:
                card = self.DEV_CARD_INPUT_MAP[raw]
                break
            print('  Invalid. Options: knight, road, yop, monopoly, vp.')

        if player.development_cards[card] < 1:
            print('  You do not have that card available.')
            return

        if card == DevelopmentCard.KNIGHT:
            hex_num = self._prompt_int(f'  Move robber to hex # (1-{len(board.hexes)}): ', 1, len(board.hexes))
            self.play_knight(player, hex_num, board.hexes)
        elif card == DevelopmentCard.ROAD_BUILDING:
            v1a = self._prompt_vertex('  Road 1 vertex 1: ')
            v1b = self._prompt_vertex('  Road 1 vertex 2: ')
            v2a = self._prompt_vertex('  Road 2 vertex 1: ')
            v2b = self._prompt_vertex('  Road 2 vertex 2: ')
            self.play_road_building(player, v1a, v1b, v2a, v2b)
        elif card == DevelopmentCard.YEAR_OF_PLENTY:
            r1 = self._prompt_resource('  Resource 1: ')
            r2 = self._prompt_resource('  Resource 2: ')
            self.play_year_of_plenty(player, r1, r2)
        elif card == DevelopmentCard.MONOPOLY:
            r = self._prompt_resource('  Monopolize which resource: ')
            self.play_monopoly(player, r)
        elif card == DevelopmentCard.VICTORY_POINT:
            self.play_victory_point(player)


    # ---------- Win condition + main loop ----------

    def check_winner(self):
        for p in self.players:
            if p.points >= 10:
                return p
        return None


    def play_game(self, board):
        self.setup_phase(board)

        turn_idx = 0
        while True:
            current = self.players[turn_idx % len(self.players)]
            self.take_turn(current, board)

            winner = self.check_winner()
            if winner is not None:
                print(f'\n*** {player_colors_names[winner.color]} WINS with {winner.points} VP! ***')
                return winner

            turn_idx += 1

