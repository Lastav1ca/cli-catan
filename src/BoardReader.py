def get_all_vertices():
    with open('../data/catan_hex_grid.txt', mode = 'r', encoding = None) as grid:

        vertices = []

        for row_idx, line in enumerate(grid):

            if 'EOF' in line:
                return vertices

            for col_idx, row in enumerate(line):

                if row == '.':
                    vertices.append((col_idx, row_idx))

def get_all_hexes():
    with open('../data/catan_hex_grid.txt', mode = 'r', encoding = None) as grid:

        row_pos = 0
        col_pos = 0

        row_end = [3, 7, 12, 16, 20]

        hex_positions = []

        for row_idx, line in enumerate(grid):

            if 'EOF' in line:
                return hex_positions
            
            for col_idx, row in enumerate(line):

                if row.isdigit():

                    if line[col_idx - 1].isdigit():
                        continue

                    hex_positions.append((col_pos, row_pos))

                    col_pos += 1

                    if len(hex_positions) == row_end[row_pos]:
                        row_pos += 1
                        col_pos = 0

