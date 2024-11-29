from Renderable.MappedObject import MappedObject
class LogicRenderable():
    mesh = None
    mapped_object = None
    def __init__(self, mapped_object: MappedObject):
        self.mapped_object = mapped_object

    def move_to(self, x, y, z):
        self.mapped_object.x = x
        self.mapped_object.y = y
        self.mapped_object.z = z
