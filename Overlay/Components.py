import pygame
from uuid import uuid4
class Component:
    x = 0
    y = 0
    width = 0
    height = 0
    fill = '#FFF'
    def __init__(self):
        self.identifier = uuid4()
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

class Input(TextDisplay):
    fill = '#FFF'
    def press(self, key):
        print(key.unicode)
        if key.key == pygame.K_BACKSPACE:
            self.text = self.text[:-1]
        else:
            self.text += key.unicode