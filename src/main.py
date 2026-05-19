import sys
sys.stdout.reconfigure(encoding='utf-8')

from Board import HexGrid
from BoardWriter import initialize_board, insert_hex_values, insert_hex_resources, reset_board, insert_robber
from Player import Player, PlayerColor
from Game import Game
from ResourceEnum import Resource

def give_road_resources(player):
    player.resources[Resource.BRICK] = 1
    player.resources[Resource.WOOD] = 1

def print_resources(player, name):
    print(f'{name} resources: {dict(player.resources)}')

if __name__ == '__main__':

    game = Game()
    game_board = HexGrid()

    player_red = Player(PlayerColor.RED)
    player_green = Player(PlayerColor.GREEN)

    reset_board()
    initialize_board(game_board)

    # Red has a settlement and a road
    game.create_settlement(player_red, (10, 4))
    game.create_road(player_red, (14, 0), (10, 4))

    # Green has a settlement at a vertex adjacent to reds road endpoint
    game.create_settlement(player_green, (14, 0))

    game.print_hex_grid()

    print('\n--- TEST 1: insufficient resources ---')
    game.purchase_road(player_red, (10, 4), (6, 8))

    print('\n--- TEST 2: valid road placement ---')
    give_road_resources(player_red)
    print_resources(player_red, 'RED before')
    game.purchase_road(player_red, (10, 4), (10, 8))
    print_resources(player_red, 'RED after')

    print('\n--- TEST 3: duplicate road ---')
    give_road_resources(player_red)
    game.purchase_road(player_red, (14, 0), (10, 4))

    print('\n--- TEST 4: not adjacent to own network ---')
    give_road_resources(player_red)
    game.purchase_road(player_red, (34, 16), (30, 12))

    print('\n--- TEST 5: road blocked by opponent settlement ---')
    give_road_resources(player_red)
    game.purchase_road(player_red, (14, 0), (18, 4))

    #print('\n--- TEST 6: place robber ---')
    #insert_robber(3)

    game.print_hex_grid()
