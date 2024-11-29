from Renderable.ImageTexture import ImageTexture
from Renderable.Mesh import Mesh
from Renderable.ModelGeometry import ModelGeometry
import uuid
class Renderable:
    mesh = None
    x = 0
    y = 0
    z = 0
    r = 1.0
    g = 0.0
    b = 0.0
    scale = 1.
    uuid = uuid.uuid4()
    def __init__(self, program, texture, geometry):
        
        self.textureForBase = ImageTexture(texture)
        self.cube_geometry = ModelGeometry(geometry)
        self.program = program
        self.mesh = Mesh(program, self.cube_geometry, self.textureForBase)
    def move_to(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    async def render(self):
        return await self.mesh.render((self.x, self.y, self.z), (self.r, self.g, self.b), self.scale)
