import math

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

                    hex_positions.append(((col_pos, row_pos), (col_idx, row_idx)))

                    col_pos += 1

                    if len(hex_positions) == row_end[row_pos]:
                        row_pos += 1
                        col_pos = 0

def find_hex_vertices(hex_physical_coordinates):
    vertices = get_all_vertices()

    distances = []

    for vertex in vertices:
        distances.append((
            math.sqrt(
                math.pow(vertex[0] - hex_physical_coordinates[0], 2) + 
                math.pow(vertex[1] - hex_physical_coordinates[1], 2)), vertex))
        
    distances = sorted(distances)

    hex_distances = distances[0:6]

    hex_vertices = []

    for hex in hex_distances:
        hex_vertices.append(hex[1])

    return hex_vertices



