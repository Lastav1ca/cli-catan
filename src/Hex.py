from ResourceEnum import Resource, resource_emoji

class Hex:
    def __init__(self, resource_type, value):
        self.resource_yield = resource_type
        self.value = value
        self.vertices = []

    def set_vertices(self, vertices_physical_position):
        self.vertices = vertices_physical_position
        
