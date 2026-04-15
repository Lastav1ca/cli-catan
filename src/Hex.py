from ResourceEnum import Resource

class Hex:
    def __init__(self, resource_type, value):
        self.resource_yield = resource_type
        self.value = value
        self.touching_structures = []
        