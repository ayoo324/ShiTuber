import pygame
from PIL import Image, ImageDraw, ImageFont
from uuid import uuid4
class Component:
    fill = '#FFF'
    value = ''
    label = ''
    image = None
    def __init__(self, label, pos, dimensions):
        self.pos = pos
        self.label = label
        self.dimensions = dimensions
        self.identifier = uuid4()
        self.hide_label = False
    def init_image(self):
        self.image = Image.new("RGBA", self.dimensions)
    
    def create_label(self):
        self.label_image = Image.new("RGBA", (50, 20))
        pen = ImageDraw.Draw(self.image)
        pen.font = ImageFont.truetype('fonts/OpenSans-Medium.ttf', 20)
        pen.text((0, 0), self.label, fill=self.fill)

    def render(self):
        self.init_image()
        if not self.hide_label:
            self.create_label()
        return self.image.resize(self.dimensions)
    def click(self):
        print(f'clicked: {self.identifier}')

    def press(self, key):
        pass

    def updateParentX(self):
        try:
            value = int(self.value)
            self.parent.pos = (value, self.parent.pos[1])
        except:
            pass
    def updateParentY(self):
        try:
            value = int(self.value)
            self.parent.pos = (self.parent.pos[0], value)
        except:
            pass
    def updateParentW(self):
        try:
            value = int(self.value)
            self.parent.dimensions = (value, self.parent.dimensions[1])
        except:
            pass
    def updateParentH(self):
        try:
            value = int(self.value)
            self.parent.dimensions = (self.parent.dimensions[0], value)
        except:
            pass

    def getDebugInputs(self, offsets):
        
        self.BaseX = Input(f'{self.label} X', (offsets[0], offsets[1]), (200, 60))
        self.BaseX.value = str(self.pos[0])
        self.BaseX.parent = self
        self.BaseX.onEdit = self.BaseX.updateParentX

        self.BaseY = Input(f'{self.label} Y', (offsets[0], offsets[1] + 60), (200, 60))
        self.BaseY.value= str(self.pos[1])
        self.BaseY.parent = self
        self.BaseY.onEdit = self.BaseY.updateParentY

        self.BaseW = Input(f'{self.label} Width', (offsets[0], offsets[1] + 120), (200, 60))
        self.BaseW.value = str(self.dimensions[0])
        self.BaseW.parent = self
        self.BaseW.onEdit = self.BaseW.updateParentW

        self.BaseH = Input(f'{self.label} Height', (offsets[0], offsets[1] + 180), (200, 60))
        self.BaseH.value= str(self.dimensions[1])
        self.BaseH.parent = self
        self.BaseH.onEdit = self.BaseH.updateParentH
        return [
            self.BaseX,
            self.BaseY,
            self.BaseW,
            self.BaseH
        ]

class TextDisplay(Component):
    def render(self):
        self.init_image()
        self.create_label()
        pen = ImageDraw.Draw(self.image)
        pen.font = ImageFont.truetype('fonts/OpenSans-Medium.ttf', 20)
        pen.text((0, 20), self.value, fill=self.fill)
        return self.image.resize(self.dimensions)


class Input(TextDisplay):
    fill = '#FFF'
    def press(self, key):
        if key.key == pygame.K_BACKSPACE:
            self.value = self.value[:-1]
        else:
            self.value += key.unicode
        try:
            self.onEdit()
        except Exception:
            pass

class Picture(Component):
    def __init__(self, pos, dimensions, imagePath):
        super().__init__('', pos, dimensions)
        self.hide_label = True
        self.value = imagePath

    def init_image(self):
        if self.image is None:
            self.image = Image.open(self.value)

    def getDebugInputs(self, offsets):      
        return super().getDebugInputs(offsets)

class Rectangle(Component):
    def init_image(self):
        self.image = Image.new("RGBA", self.dimensions, color=(1, 1, 1))
    def render(self):
        self.init_image()
        pen = ImageDraw.Draw(self.image)
        pen.rectangle((0, 0, self.dimensions[0], self.dimensions[1]))
        return self.image.resize(self.dimensions)


    