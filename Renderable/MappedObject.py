from ctypes import *
class MappedObject(Structure):
    _fields = [
        {'id', c_int},
        ("x", c_int),
        ("y", c_int),
        ("z", c_int),
        ("scale", c_float),
        ("texture_id", c_int),
        ("program_id", c_int),
        ("geometry_id", c_int),
        ("r", c_float),
        ("g", c_float),
        ("b", c_float)
    ]
    def __init__(self, id, position: tuple[3], scale: float, texture_id: int, geometry_id: int, color: tuple[3] = (0, 0, 0), program_id: tuple[2] = 0):
        self.x = position[0]
        self.y = position[1]
        self.z = position[2]
        self.scale = scale
        self.texture_id = texture_id
        self.geometry_id = geometry_id
        self._as_parameter_ = self._fields
        self.r = color[0]
        self.g = color[1]
        self.b = color[2]
        self.program_id = program_id
        self.id = id
        