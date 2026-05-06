class Settlement:
    def __init__(self, player, position):
        self.player = player
        self.position = position

class City:
    def __init__(self, player, position):
        self.player = player
        self.position = position

class Road:
    def __init__(self, player, vertex1_coordinates, vertex2_coordinates):
        self.player = player
        self.vertex1_coordinates = vertex1_coordinates
        self.vertex2_coordinates = vertex2_coordinates
        self.road_type, self.positions = self.get_road_info()

    def get_road_info(self): # Returns road type, road positions (3)

        if self.vertex1_coordinates[1] < self.vertex2_coordinates[1]:
            higher_vertex_coordinates = self.vertex1_coordinates
            lower_vertex_coordinates = self.vertex2_coordinates
        else:
            higher_vertex_coordinates = self.vertex2_coordinates
            lower_vertex_coordinates = self.vertex1_coordinates

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
            
        return road_type, road_positions