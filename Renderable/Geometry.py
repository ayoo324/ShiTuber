import moderngl
from objloader import Obj
class Geometry:
    def __init__(self, path):
        self.ctx = moderngl.get_context()

        obj = Obj.open(path)
        self.vbo = self.ctx.buffer(obj.pack('vx vy vz nx ny nz tx ty'))

    def vertex_array(self, program):
        return self.ctx.vertex_array(program, [(self.vbo, '3f 12x 2f', 'in_vertex', 'in_uv')])