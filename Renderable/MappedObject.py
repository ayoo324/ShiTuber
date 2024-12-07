
class IDGenerator():
    last_id = 0
    def generate_id(self):
        self.last_id = self.last_id + 1
        return self.last_id
generator = IDGenerator()


class MappedObject():
    def __init__(self, position: tuple[3], scale: float, texture_id: int, geometry_id: int, color: tuple[3] = (0, 0, 0), program_id: tuple[2] = 0):
        self.x = position[0]
        self.y = position[1]
        self.z = position[2]
        self.scale = scale
        self.texture_id = texture_id
        self.geometry_id = geometry_id
        self.r = color[0]
        self.g = color[1]
        self.b = color[2]
        self.program_id = program_id
        self.id = generator.generate_id()

    def __iter__(self):
        for key, value in self.__dict__.items():
            if not key.startswith('__') and not callable(value) and not callable(getattr(value, "__get__", None)):
                yield value