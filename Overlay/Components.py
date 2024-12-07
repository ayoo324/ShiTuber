import pygame
from PIL import Image, ImageDraw, ImageFont
from uuid import uuid4
from ctypes import *
class BaseComponent():
    _fields = [
        {'speed_l', c_float},
        ("speed_r", c_float),
        ("speed_u", c_float),
        ("speed_d", c_float),
        ("max_l", c_int),
        ("max_r", c_int),
        ("max_u", c_int),
        ("max_d", c_int),
        ("width", c_int),
        ("height", c_int),
        ("max_velocity_x", c_int),
        ("max_velocity_y", c_int),
        ("decay_x", c_float),
        ("decay_y", c_float),
        ("velocity_x", c_float),
        ("velocity_y", c_float),
        ("pos_x", c_int),
        ("pos_y", c_int),
        ("real_pos_x", c_float),
        ("real_pos_y", c_float),
        ("return_to_center", c_bool),
        ("identifier", c_int)
    ]
    def __init__(self, pos, dimensions):
        self.real_pos_x = pos[0]
        self.real_pos_y = pos[1]
        self.pos_x = pos[0]
        self.pos_y = pos[1]
        self.max_l = pos[0]
        self.max_r = pos[0]
        self.max_u = pos[1]
        self.max_d = pos[1]
        self.velocity_x = 0
        self.velocity_y = 0
        self.max_velocity_x = 0
        self.max_velocity_y = 0
        self.speed_l = 0
        self.speed_r = 0
        self.speed_u = 0
        self.speed_d = 0
        self.decay_x = 0
        self.decay_y = 0
        self.width = dimensions[0]
        self.height = dimensions[1]
        self.identifier = uuid4().int
        self.return_to_center = True

    async def interpolate(self):
        if self.return_to_center:
            center = ( self.max_l + self.max_r ) / 2
            if self.real_pos_x > center:
                if self.real_pos_x - self.velocity_x - self.speed_l < center:
                    self.real_pos = (center, self.real_pos_y)
                    self.velocity = (0, self.velocity_y)
                else:
                    self.left()
            if self.real_pos_x < center:
                if self.real_pos_x + self.velocity_x + self.speed_r  > center:
                    self.real_pos = (center, self.real_pos_y)
                    self.velocity = (0, self.velocity_y)
                else:
                    self.right()

        self.real_pos = (
                        min(
                            max(self.real_pos_x + self.velocity_x, self.max_l), 
                            self.max_r
                        ),
                        min(
                            max(self.real_pos_y + self.velocity_y, self.max_u), 
                            self.max_d
                        )
                    )
        xVel = 0
        if self.velocity_x > 0:
            xVel = max(0, self.velocity_x - self.decay_x)
        elif self.velocity_x < 0:
            xVel = min(0, self.velocity_x + self.decay_x)


        yVel = 0
        if self.velocity_y > 0:
            yVel = max(0, self.velocity_y - self.decay_y)

        elif self.velocity_y < 0:
            yVel = min(0, self.velocity_y + self.decay_y)

        self.velocity = (
                        xVel,
                        yVel
                    )
        

        self.pos = (int(self.real_pos_x), int(self.real_pos_y))

    def left(self):
        self.return_to_center = False
        self.velocity_x = max(self.velocity_x - self.speed_l, -self.max_velocity_x)
    def right(self):
        self.return_to_center = False
        self.velocity_x = min(self.velocity_x + self.speed_r, self.max_velocity_x)
    def up(self):
        self.velocity_y = max(self.velocity_y - self.speed_u, -self.max_velocity_y)
    def down(self):
        self.velocity_y = min(self.velocity_y + self.speed_d, self.max_velocity_y)
    def center(self):
        self.return_to_center = True
    
    def click(self):
        print(f'clicked: {self.identifier}')

    def press(self, key):
        pass

class Component():
    fill = '#FFF'
    value = ''
    label = ''
    image = None
    base = None
    def __init__(self, label, pos, dimensions):
        self.base = BaseComponent(pos, dimensions)
        self.label = label
        self.hide_label = False

    def init_image(self):
        self.image = Image.new("RGBA", self.dimensions())
    
    def create_label(self):
        self.label_image = Image.new("RGBA", (50, 20))
        pen = ImageDraw.Draw(self.image)
        pen.font = ImageFont.truetype('fonts/OpenSans-Medium.ttf', 20)
        pen.text((0, 0), self.label, fill=self.fill)

    def dimensions(self):
        return (self.base.width, self.base.height)

    async def render(self):
        await self.base.interpolate()
        self.init_image()
        if not self.hide_label:
            self.create_label()
        # self.image.resize(self.dimensions)
        return self


class TextDisplay(Component):
    async def render(self):
        await self.base.interpolate()
        self.init_image()
        self.create_label()
        pen = ImageDraw.Draw(self.image)
        pen.font = ImageFont.truetype('fonts/OpenSans-Medium.ttf', 20)
        pen.text((0, 20), self.value, fill=self.fill)
        self.image.resize(self.dimensions())
        return self


class Input(TextDisplay):
    fill = '#FFF'
    def press(self, key):
        if key['key'] == pygame.K_BACKSPACE:
            self.value = self.value[:-1]
        else:
            self.value += key['unicode']
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
        self.image = Image.new("RGBA", self.dimensions(), color=(1, 1, 1))
    async def render(self):
        await self.base.interpolate()
        self.init_image()
        pen = ImageDraw.Draw(self.image)
        pen.rectangle((0, 0, self.dimensions()[0], self.dimensions()[1]))
        self.image.resize(self.dimensions())
        return self


    