from ResourceEnum import resource_emoji, Resource
from Player import player_colors_codes, PlayerColor


def initialize_board(hex_grid):
    hexes = hex_grid.hexes
    insert_hex_values(hexes)
    insert_hex_resources(hexes)


def insert_hex_values(hexes):

    with open('../data/catan_hex_grid.txt', mode = 'r', encoding = None) as file:
        content = file.readlines()

    hex_idx = 0
    skip_next = False

    for row_idx, line in enumerate(content):

        if 'EOF' in line:
            break

        replacements = [] #replacements is a list of tuples which contains 
                          # 1. the start replacement position
                          # 2. the end replacement position
                          # 3. the new value to insert

        for col_idx, col in enumerate(line):

            if skip_next:
                skip_next = False
                continue

            if col.isdigit():

                digit_replacement_pos = col_idx

                if hexes[hex_idx].resource_yield == Resource.DESERT:
                    new_digit = 'D'
                else:
                    new_digit = hexes[hex_idx].value
    
                hex_idx += 1

                if line[col_idx + 1].isdigit(): #checks if current hex has double digit number (10, 11...)
                    
                    if len(str(new_digit)) == 2: #if the replacement value is also double digit

                        replacements.append((digit_replacement_pos, (digit_replacement_pos + 2), str(new_digit)))
                        skip_next = True
                        continue

                    else:

                        new_digit = f' {new_digit}'

                        replacements.append((digit_replacement_pos, (digit_replacement_pos + 2), str(new_digit)))
                        skip_next = True
                        continue


                if len(str(new_digit)) == 2: 

                        replacements.append((digit_replacement_pos - 1, (digit_replacement_pos + 1), str(new_digit)))
                        continue

                replacements.append((digit_replacement_pos, (digit_replacement_pos + 1), str(new_digit)))
                continue

        for start_pos, end_pos, value in reversed(replacements):
            line = line[:start_pos] + value + line[end_pos:]
        content[row_idx] = line

    with open('../data/catan_hex_grid.txt', mode = 'w', encoding = None) as file:
        file.writelines(content)


def insert_hex_resources(hexes):

    with open('../data/catan_hex_grid.txt', mode = 'r', encoding = None) as file:
        content = file.readlines()

    hex_idx = 0
    skip_next = False

    for row_idx, line in enumerate(content):

        if 'EOF' in line:
            break

        replacements = [] #replacements is a list of tuples which contains 
                          # 1. the replacement position
                          # 2. the value to insert

        for col_idx, col in enumerate(line):

            if col == 'r':

                new_emoji = str(resource_emoji[hexes[hex_idx].resource_yield])

                if hexes[hex_idx].resource_yield == Resource.DESERT:
                    
                    #needed an extra check here for Stone and Desert emojis, as they are 2 characters long when printed

                    new_emoji = f'{new_emoji} '

                    replacements.append((col_idx, new_emoji))
                    hex_idx += 1
                    continue

                replacements.append((col_idx, new_emoji))
                hex_idx += 1

        for position, value in reversed(replacements):
            line = line[:position] + value + line[position + 2:]
        content[row_idx] = line
            

    with open('../data/catan_hex_grid.txt', mode = 'w', encoding = None) as file:
        file.writelines(content)


def insert_settlement(vertex_coordinates):

    with open('../data/catan_hex_grid.txt', mode = 'r', encoding = None) as file:
        content = file.readlines()

    position_found = False

    for row_idx, line in enumerate(content):

        for col_idx, row in enumerate(line):
            #print(f'Koordinate {(col_idx, row_idx)} \n')
            
            if (col_idx, row_idx) == vertex_coordinates:
                
                position_found = True
            
        if position_found:

            line = line[:vertex_coordinates[0]] + 'S' + line[vertex_coordinates[0] + 1:]
            #print(f'Koordinate {line[vertex_coordinates[0]:]} \n')
            content[row_idx] = line

            break

    with open('../data/catan_hex_grid.txt', mode = 'w', encoding = None) as file:
        file.writelines(content)

def insert_city(vertex_coordinates):

    with open('../data/catan_hex_grid.txt', mode = 'r', encoding = None) as file:
        content = file.readlines()

    position_found = False

    for row_idx, line in enumerate(content):

        for col_idx, row in enumerate(line):
            #print(f'Koordinate {(col_idx, row_idx)} \n')
            
            if (col_idx, row_idx) == vertex_coordinates:
                
                position_found = True
            
        if position_found:

            line = line[:vertex_coordinates[0]] + 'C' + line[vertex_coordinates[0] + 1:]
            #print(f'Koordinate {line[vertex_coordinates[0]:]} \n')
            content[row_idx] = line

            break

    with open('../data/catan_hex_grid.txt', mode = 'w', encoding = None) as file:
        file.writelines(content)

def insert_road(vertex1_coordinates, vertex2_coordinates, player):

    if vertex1_coordinates[1] < vertex2_coordinates[1]:
        higher_vertex_coordinates = vertex1_coordinates
        lower_vertex_coordinates = vertex2_coordinates
    else:
        higher_vertex_coordinates = vertex2_coordinates
        lower_vertex_coordinates = vertex1_coordinates

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
        
    player_color = player_colors_codes[player.color]
    road = f'{player_color}' + f'{road_type}' + f'{player_colors_codes[0]}'
    
    #print(f'\n Higher: {higher_vertex_coordinates} \n')
    #print(f'\n Road: {road} \n')

    with open('../data/catan_hex_grid.txt', mode = 'r', encoding = None) as file:
        content = file.readlines()

    positions_found = 0

    road_found = False

    for row_idx, line in enumerate(content):

        for col_idx, row in enumerate(line):

            if (col_idx, row_idx) == road_positions[road_found]:
                road_found = True
        
        if road_found:
            line = line[:road_positions[0][0]] + road + line[road_positions[0][0]+1:]
            positions_found += 1
            content[row_idx] = line

            if positions_found >= 2:
                break

    with open('../data/catan_hex_grid.txt', mode = 'w', encoding = None) as file:
        file.writelines(content)

def reset_board():
    with open('../data/catan_hex_grid_template.txt', mode = 'r', encoding = None) as file:
        content = file.readlines()

    with open('../data/catan_hex_grid.txt', mode = 'w', encoding = None) as file:
        file.writelines(content)
