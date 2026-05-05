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


def reset_board():
    with open('../data/catan_hex_grid_template.txt', mode = 'r', encoding = None) as file:
        content = file.readlines()

    with open('../data/catan_hex_grid.txt', mode = 'w', encoding = None) as file:
        file.writelines(content)
