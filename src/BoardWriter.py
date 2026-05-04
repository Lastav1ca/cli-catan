from ResourceEnum import resource_emoji, Resource


def update_board(hexes):
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

        replacements = []

        for col_idx, row in enumerate(line):
            if skip_next:
                skip_next = False
                continue

            if row.isdigit():

                if line[col_idx + 1].isdigit():

                    current_digit = line[col_idx] + line[col_idx + 1]

                    if hexes[hex_idx].value is None:
                        replaced_value = 'D'
                    else:
                        replaced_value = hexes[hex_idx].value

                    replacements.append((current_digit, replaced_value))

                    hex_idx += 1

                    skip_next = True
                else:
                    current_digit = line[col_idx]

                    if hexes[hex_idx].value is None:
                        replaced_value = 'D'
                    else:
                        replaced_value = hexes[hex_idx].value

                    replacements.append((current_digit, replaced_value))
                        
                    hex_idx += 1


        for old, new in replacements:
            line = line.replace(old, str(new))                                    
        content[row_idx] = line

    with open('../data/catan_hex_grid.txt', mode = 'w', encoding = None) as file:
        file.writelines(content)


def insert_hex_resources(hexes):
    pass

def reset_board():
    with open('../data/catan_hex_grid_template.txt', mode = 'r', encoding = None) as file:
        content = file.readlines()

    with open('../data/catan_hex_grid.txt', mode = 'w', encoding = None) as file:
        file.writelines(content)
