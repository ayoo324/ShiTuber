from Renderable.ImageTexture import ImageTexture
from Renderable.Mesh import Mesh
from Renderable.Geometry import Geometry
from Renderable.LogicRenderable import LogicRenderable
class Renderable(LogicRenderable):
    mesh = None
    is_loaded = False
    def load(self, program, texture:ImageTexture, geometry:Geometry):
        self.mesh = Mesh(program, geometry, texture)
        self.is_loaded = True

    def render(self):
        return self.mesh.render((self.mapped_object.x, self.mapped_object.z, self.mapped_object.y), (self.mapped_object.r, self.mapped_object.g, self.mapped_object.b), self.mapped_object.scale)
