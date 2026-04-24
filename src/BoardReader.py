def get_all_vertices():
    with open('../data/catan_hex_grid.txt', mode = 'r', encoding = None) as grid:

        vertices = []

        for row_idx, line in enumerate(grid):

            if 'EOF' in line:
                return vertices

            for col_idx, row in enumerate(line):

                if row == '.':
                    vertices.append((col_idx, row_idx))
