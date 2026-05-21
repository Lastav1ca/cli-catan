import sys
sys.stdout.reconfigure(encoding='utf-8')

from Board import HexGrid
from BoardWriter import initialize_board, reset_board
from Player import Player, PlayerColor
from Game import Game


def prompt_player_count():
    while True:
        raw = input('How many players? (2-4): ').strip()
        try:
            n = int(raw)
            if 2 <= n <= 4:
                return n
        except ValueError:
            pass
        print('Enter 2, 3, or 4.')


def build_players(n):
    colors = [PlayerColor.RED, PlayerColor.BLUE, PlayerColor.GREEN, PlayerColor.YELLOW]
    return [Player(c) for c in colors[:n]]


if __name__ == '__main__':
    reset_board()
    board = HexGrid()
    initialize_board(board)

    print('========== CLI CATAN ==========')
    n = prompt_player_count()
    players = build_players(n)

    game = Game(players)
    game.play_game(board)
