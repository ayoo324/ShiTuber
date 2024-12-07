from PIL import Image, ImageDraw
import moderngl
from Helpers.asyncHelpers import execute_multiple_calls
import pygame
from Overlay.DOM import DOM
class DOMRenderer():
    def __init__(self):
        self.dom = DOM()
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
        
        for componentKey in self.idMap.keys():
            self.idMap[componentKey].base = self.dom.overlay_map[componentKey] 

        for component in execute_multiple_calls(*[ component.render() for component in self.idMap.values()]):
            self.img.paste(component.image, component.base.pos)
        
        self.texture.write(self.img.tobytes())
        self.ctx.enable_only(self.ctx.BLEND)
        self.sampler.use()
        self.vao.render()

    def addComponent(self, component):
        self.dom.addComponent(component.base)
        self.dom.overlay_map[component.base.identifier] = component.base
        self.idMap[component.base.identifier] = component

    def removeComponent(self, component):
        self.dom.removeComponent(component.base)
        del self.dom.overlay_map[component.base.identifier]
        del self.dom.idMap[component.base.identifier]

    def click(self, x, y):
        self.dom.click(x, y)
    
    def getComponentById(self, identifier):
        return self.dom.idMap[identifier]