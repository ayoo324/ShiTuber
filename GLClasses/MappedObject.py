from ctypes import *
class MappedObject(Structure):
    _fields = [
        ("x", c_int),
        ("y", c_int),
        ("z", c_int),
        ("scale", float),
        ("texture_id", c_int)
    ]
    def __init__(self, position: tuple[3], scale: float, texture_id: int, geometry_id: int):
        self.x = position[0]
        self.y = position[1]
        self.z = position[2]
        self.scale = scale
        self.texture_id = texture_id
        self.geometry_id = geometry_id
        self._as_parameter_ = self._fields
        