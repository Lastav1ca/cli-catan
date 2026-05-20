import math


def get_all_vertices(): 

    # Helper function to return position of every vertex on the board
    # Returns a list of tuples with coordinates as (col position, row position)

    with open('../data/catan_hex_grid.txt', mode = 'r', encoding = 'utf-8') as file:

        vertices = []

        for row_idx, line in enumerate(file):

            if 'EOF' in line:
                return vertices

            for col_idx, col in enumerate(line):

                if col == '.' or col == 'S' or col == 'C':
                    vertices.append((col_idx, row_idx))

        return vertices


def get_all_hexes_positions():

    # Helper function to return position of every hex on the board
    # Returns a list of tuples with coordinates as (col position, row position) - every coordinate is the location of the digit inside the hex (the center)

    with open('../data/catan_hex_grid.txt', mode = 'r', encoding = 'utf-8') as file:

        hex_positions = []

        for row_idx, line in enumerate(file):

            if 'EOF' in line:
                return hex_positions
            
            for col_idx, col in enumerate(line):

                if col.isdigit() or col == 'D' or col == 'R':

                    if line[col_idx - 1].isdigit():
                        continue

                    hex_positions.append((col_idx, row_idx))

        return hex_positions


def find_hex_vertices(hex_physical_coordinates):

    # Finds physical position of every vertex that a hex has, based on hexes physical coordinates

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

    # Returns the hex grid in its uncolored state

    with open('../data/catan_hex_grid.txt', mode = 'r', encoding = 'utf-8') as file:
        content = file.readlines()

    content.pop()

    return content


def get_empty_vertices(): 

    # Helper function to return position of every free vertex on the board
    # Returns a list of tuples with coordinates as (col position, row position)

    with open('../data/catan_hex_grid.txt', mode = 'r', encoding = 'utf-8') as file:

        vertices = []

        for row_idx, line in enumerate(file):

            if 'EOF' in line:
                return vertices

            for col_idx, col in enumerate(line):

                if col == '.':
                    vertices.append((col_idx, row_idx))

        return vertices


def is_vertex_empty(vertex):
    empty_vertices = get_empty_vertices()

    if vertex in empty_vertices:
        return True

    return False


def get_adjacent_vertices(vertex):

    adjacent_vertices = []   

    grid = get_hex_grid()

    for row_idx, line in enumerate(grid):

        for col_idx, col in enumerate(line):

            if ((col_idx, row_idx) == vertex):

                if (col_idx, row_idx + 2) == '.' or (col_idx, row_idx + 2) == 'S' or (col_idx, row_idx + 2) == 'C':
                    adjacent_vertices.append((col_idx, row_idx + 2))
                                             
                if (col_idx, row_idx - 2) == '.' or (col_idx, row_idx - 2) == 'S' or (col_idx, row_idx - 2) == 'C':
                    adjacent_vertices.append((col_idx, row_idx + 2))

                if (col_idx + 4, row_idx + 4) == '.' or (col_idx + 4, row_idx + 4) == 'S' or (col_idx + 4, row_idx + 4) == 'C':
                    adjacent_vertices.append((col_idx + 4, row_idx + 4))

                if (col_idx + 4, row_idx - 4) == '.' or (col_idx + 4, row_idx - 4) == 'S' or (col_idx + 4, row_idx - 4) == 'C':
                    adjacent_vertices.append((col_idx + 4, row_idx - 4))

                if (col_idx - 4, row_idx + 4) == '.' or (col_idx - 4, row_idx + 4) == 'S' or (col_idx - 4, row_idx + 4) == 'C':
                    adjacent_vertices.append((col_idx - 4, row_idx + 4))

                if (col_idx - 4, row_idx - 4) == '.' or (col_idx - 4, row_idx - 4) == 'S' or (col_idx - 4, row_idx - 4) == 'C':
                    adjacent_vertices.append((col_idx - 4, row_idx - 4))

                break
        break

    return adjacent_vertices


def get_empty_adjacent_vertices(vertex):

    empty_adjacent_vertices = []   

    grid = get_hex_grid()

    for row_idx, line in enumerate(grid):

        for col_idx, col in enumerate(line):

            if ((col_idx, row_idx) == vertex):

                if (col_idx, row_idx + 2) == '.':
                    empty_adjacent_vertices.append((col_idx, row_idx + 2))
                                             
                if (col_idx, row_idx - 2) == '.':
                    empty_adjacent_vertices.append((col_idx, row_idx + 2))

                if (col_idx + 4, row_idx + 4) == '.':
                    empty_adjacent_vertices.append((col_idx + 4, row_idx + 4))

                if (col_idx + 4, row_idx - 4) == '.':
                    empty_adjacent_vertices.append((col_idx + 4, row_idx - 4))

                if (col_idx - 4, row_idx + 4) == '.':
                    empty_adjacent_vertices.append((col_idx - 4, row_idx + 4))

                if (col_idx - 4, row_idx - 4) == '.':
                    empty_adjacent_vertices.append((col_idx - 4, row_idx - 4))

                break
        break

    return empty_adjacent_vertices


def is_vertex_adjacent_to_settlement_or_city(vertex):
    adjacent = get_adjacent_vertices(vertex)
    empty = get_empty_adjacent_vertices(vertex)

    if len(empty) == len(adjacent):
        return False
    
    return True

    