import moderngl
class Mesh:
    def __init__(self, program, geometry, texture=None):
        self.ctx = moderngl.get_context()
        self.vao = geometry.vertex_array(program)
        self.texture = texture

    def render(self, position, color, scale):
        self.vao.program['use_texture'] = False

        if self.texture:
            self.vao.program['use_texture'] = True
            self.texture.use()

        self.vao.program['position'] = position
        self.vao.program['color'] = color
        self.vao.program['scale'] = scale
        self.vao.render()