import math

def get_all_vertices(): 

    # Helper function to return position of every vertex on the board
    # Returns a list of tuples with coordinates as (col position, row position)

    with open('../data/catan_hex_grid.txt', mode = 'r', encoding = None) as file:

        vertices = []

        for row_idx, line in enumerate(file):

            if 'EOF' in line:
                return vertices

            for col_idx, col in enumerate(line):

                if col == '.':
                    vertices.append((col_idx, row_idx))

def get_all_hexes():
    with open('../data/catan_hex_grid.txt', mode = 'r', encoding = None) as file:

        hex_positions = []

        for row_idx, line in enumerate(file):

            if 'EOF' in line:
                return hex_positions
            
            for col_idx, col in enumerate(line):

                if col.isdigit() or col == 'D':

                    if line[col_idx - 1].isdigit():
                        continue

                    hex_positions.append((col_idx, row_idx))



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

def get_hex_grid():
    with open('../data/catan_hex_grid.txt', mode = 'r', encoding = None) as file:
        content = file.readlines()

    content.pop()

    return content

