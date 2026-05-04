from Board import HexGrid
from BoardReader import get_all_vertices, get_all_hexes, find_hex_vertices, print_hex_grid
from BoardWriter import insert_hex_values, reset_board

if __name__ == '__main__':
    #print(get_all_vertices())
    #print(f'\n Length: {len(get_all_vertices())}')

    #print(get_all_hexes())
    #print(f'\n Length: {len(get_all_hexes())}')

    #print(find_hex_vertices((14, 5)))
    
    game_board = HexGrid()
    #game_board.print_hex_vertices()


    insert_hex_values(game_board.hexes)
    print_hex_grid()
    reset_board()

