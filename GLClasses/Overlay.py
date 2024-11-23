from PIL import Image, ImageDraw, ImageFont
import moderngl
import pygame
from uuid import uuid4
from Helpers.asyncHelpers import execute_multiple_calls
class Overlay:
    def __init__(self, size):
        self.dom = DOM(size)
        testTextDisplay = TextDisplay()
        testTextDisplay.text='Test'
        testTextDisplay.x=0
        testTextDisplay.y=0
        testTextDisplay.width=100
        testTextDisplay.height=50

        self.dom.addComponent(testTextDisplay)

    def render(self):
        self.dom.render()

    def drawText(self, textDisplay):
        return self.draw.text((textDisplay.posX, textDisplay.posY), textDisplay.text, fill=textDisplay.fill)

    def click(self, coordinates):
        (x, y) = coordinates
        self.dom.click(x, y)

    def hasFocus(self):
        return not self.dom.focus == None

    def handleKey(self, key):
        self.dom.focus.press(key)

class Component:
    x = 0
    y = 0
    width = 0
    height = 0
    identifier = uuid4()
    fill = '#FFF'
    def render(self, pen):
        pass
    def click(self):
        print(f'clicked: {self.identifier}')

    def press(self, key):
        pass


class TextDisplay(Component):
    text = ''
    def getText(self):
        return self.text
    def render(self, pen):
        pen.text((self.x, self.y), self.text, fill=self.fill)
    def press(self, key):
        if key.key == pygame.K_BACKSPACE:
            self.text = self.text[:-1]
        else:
            self.text += key.unicode

class Input(TextDisplay):
    fill = '#000'
    def render(self, pen):
        pen.text((self.x, self.y), self.text, fill=self.fill)


class DOM():
    def __init__(self, canvas_size):
        self.ctx = moderngl.get_context()
        self.img = Image.new('RGBA', canvas_size)
        self.draw = ImageDraw.Draw(self.img)
        self.draw.font = ImageFont.truetype('fonts/OpenSans-Medium.ttf', 20)
        self.texture = self.ctx.texture(canvas_size, 4)
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
        self.canvas_size = canvas_size
        self.canvas_map = [[0]* canvas_size[0]]*canvas_size[1]
        self.idMap = {}
        self.focus = None

    def render(self):
        self.draw.rectangle((0, 0, *self.img.size), fill=(0, 0, 0, 0))
        
        for component in self.idMap.values():
            component.render(self.draw)

        self.texture.write(self.img.tobytes())
        self.ctx.enable_only(self.ctx.BLEND)
        self.sampler.use()
        self.vao.render()
    
    def addComponent(self, component):
        for curX in range(component.x, component.x + component.width):
            for curY in range(component.y, component.y + component.height):
                self.canvas_map[curX][curY] = component.identifier
        self.idMap[component.identifier] = component

    def removeComponent(self, component):
        for curX in range(component.x, component.x + component.width):
            for curY in range(component.y, component.y + component.height):
                self.canvas_map[curX][curY] = 0
        del self.idMap[component.identifier]

    def click(self, x, y):
        identifier = self.canvas_map[x][y]
        if identifier == 0:
            self.focus = None
            pass
        else:
            self.focus = self.idMap[identifier]
            self.focus.click()
    
    def getComponentById(self, identifier):
        return self.idMap[identifier]
