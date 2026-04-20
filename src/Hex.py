from ResourceEnum import Resource, resource_emoji

class Hex:
    def __init__(self, resource_type, value):
        self.resource_yield = resource_type
        self.value = value
        self.touching_structures = []
        self.coordinates = (0, 0)

    def get_hex_lines(self):
        
        lines = []

        lines.append('_____')

        lines.append('/     \\')

        lines.append(f'/  {resource_emoji[self.resource_yield]}  \\')

        lines.append(f'\   {self.value if self.value is not None else ''}    /')

        lines.append('\_____/')
        
