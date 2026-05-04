import ResourceEnum
import random
from Hex import Hex
from BoardReader import get_all_hexes, find_hex_vertices

class HexGrid():
    def __init__(self):
        self.hexes = self.generate_hex_grid()
        self.map_vertices_to_hex()
        ## HEX GRID
        ##    1    2    3

        ##  4    5    6     7

        ## 8   9   10    11    12

        ##   13  14   15    16

        ##     17   18   19

    def generate_hex_grid(self):

        resources = ([ResourceEnum.Resource.SHEEP] * ResourceEnum.SHEEP_COUNT 
                     + [ResourceEnum.Resource.WHEAT] * ResourceEnum.WHEAT_COUNT 
                     + [ResourceEnum.Resource.WOOD] * ResourceEnum.WOOD_COUNT 
                     + [ResourceEnum.Resource.BRICK] * ResourceEnum.BRICK_COUNT 
                     + [ResourceEnum.Resource.STONE] * ResourceEnum.STONE_COUNT)

        values = [2, 3, 3, 4, 4, 5, 5, 6, 6, 8, 8, 9, 9, 10, 10, 11, 11, 12]

        random.shuffle(resources)
        random.shuffle(values)

        value_resource_iterable = zip(resources, values)

        hexes = []

        hexes.append(Hex(ResourceEnum.Resource.DESERT, None))

        for resource,value in value_resource_iterable:
            hexes.append(Hex(resource, value))

        random.shuffle(hexes)

        return hexes
    
    def map_vertices_to_hex(self):

        hex_coordinates = get_all_hexes()

        hex_idx = 0

        for hex in self.hexes:

            vertex_physical_coordiantes = find_hex_vertices(hex_coordinates[hex_idx])

            hex.set_vertices(vertex_physical_coordiantes)

            hex_idx += 1

    def print_hex_vertices(self):

        idx = 0

        for hex in self.hexes:
            print(f'Hex: {idx} Vertex coords: {hex.vertices}')
            idx += 1
    



