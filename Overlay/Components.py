import pygame
from PIL import Image, ImageDraw, ImageFont
from uuid import uuid4
class Component:
    fill = '#FFF'
    value = ''
    def __init__(self, pos, dimensions):
        self.pos = pos
        self.dimensions = dimensions
        self.identifier = uuid4()
        self.init_image()
    def init_image(self):
        self.image = Image.new("RGBA", self.dimensions)
    def render(self):
        return self.image
    def click(self):
        print(f'clicked: {self.identifier}')

    def press(self, key):
        pass

class TextDisplay(Component):
    def render(self):
        pen = ImageDraw.Draw(self.image)
        pen.font = ImageFont.truetype('fonts/OpenSans-Medium.ttf', 20)
        pen.text((0, 0), self.value, fill=self.fill)
        return self.image


class Input(TextDisplay):
    fill = '#FFF'
    def press(self, key):
        if key.key == pygame.K_BACKSPACE:
            self.value = self.value[:-1]
        else:
            self.value += key.unicode


class Picture(Component):
    def __init__(self, pos, dimensions, imagePath):
        self.pos = pos
        self.dimensions = dimensions
        self.value = imagePath
        self.identifier = uuid4()
        self.init_image()

    def init_image(self):
        self.image = Image.open(self.value).resize(self.dimensions)
        