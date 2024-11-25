from PIL import Image, ImageDraw, ImageFont
import moderngl
import pygame
from uuid import uuid4
class DOM():
    def __init__(self):
        self.ctx = moderngl.get_context()
        self.img = Image.new('RGBA', pygame.display.get_window_size())
        self.draw = ImageDraw.Draw(self.img)
        self.texture = self.ctx.texture(pygame.display.get_window_size(), 4)
        self.program = self.ctx.program(
            vertex_shader='''
                #version 330 core

                vec2 positions[3] = vec2[](
                    vec2(-1.0, -1.0),
                    vec2(3.0, -1.0),
                    vec2(-1.0, 3.0)
                );

                void main() {
                    gl_Position = vec4(positions[gl_VertexID], 0.0, 1.0);
                }
            ''',
            fragment_shader='''
                #version 330 core

                uniform sampler2D Texture;

                layout (location = 0) out vec4 out_color;

                void main() {
                    ivec2 at = ivec2(gl_FragCoord.xy);
                    at.y = textureSize(Texture, 0).y - at.y - 1;
                    out_color = texelFetch(Texture, at, 0);
                }
            ''',
        )
        self.sampler = self.ctx.sampler(texture=self.texture)
        self.vao = self.ctx.vertex_array(self.program, [])
        self.vao.vertices = 3
        self.canvas_map = {}
        self.idMap = {}
        self.focus = None

    def render(self):
        self.draw.rectangle((0, 0, *self.img.size), fill=(0, 0, 0, 0))
        for component in self.idMap.values():
            self.img.paste(component.render(), component.pos)

        self.texture.write(self.img.tobytes())
        self.ctx.enable_only(self.ctx.BLEND)
        self.sampler.use()
        self.vao.render()
    
    def addComponent(self, component):
        for curX in range(component.pos[0], component.pos[0] + component.dimensions[0]):
            if curX not in self.canvas_map:
                self.canvas_map[curX] = {}
            for curY in range(component.pos[1], component.pos[1] + component.dimensions[1]):
                self.canvas_map[curX][curY] = component.identifier
        self.idMap[component.identifier] = component

    def removeComponent(self, component):
        for curX in range(component.pos[0], component.pos[0] + component.dimensions[0]):
            for curY in range(component.pos[1], component.pos[1] + component.dimensions[1]):
                del self.canvas_map[curX][curY]
        del self.idMap[component.identifier]

    def click(self, x, y):
        if x in self.canvas_map and y in self.canvas_map[x]:
            identifier = self.canvas_map[x][y]
            self.focus = self.idMap[identifier]
            self.focus.click()
        else:
            self.focus = None
    
    def getComponentById(self, identifier):
        return self.idMap[identifier]
