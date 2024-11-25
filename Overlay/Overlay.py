from PIL import Image, ImageDraw, ImageFont
import moderngl
import pygame
from uuid import uuid4
from Helpers.asyncHelpers import execute_multiple_calls
from Overlay.DOM import DOM
from Overlay.Components import TextDisplay, Input, Picture, Rectangle
import io

class Overlay:
    def __init__(self):
        self.dom = DOM()

        self.base = Picture((700, 70), (219, 201), "Images/base.png")
        self.base.label = 'Base'
        self.dom.addComponent(self.base)
        for component in self.base.getDebugInputs( (0, 0) ):
            self.dom.addComponent(component)
        self.head = Picture((760, 20), (80, 50), "Images/head.png")
        self.head.label = 'Head'
        self.dom.addComponent(self.head)
        for component in self.head.getDebugInputs( (250, 0) ):
            self.dom.addComponent(component)

        self.audioBar = Rectangle('Audio', (0, 400), (20, 0))

        self.dom.addComponent(self.audioBar)


    def render(self):

        self.dom.render()

    def click(self, coordinates):
        (x, y) = coordinates
        self.dom.click(x, y)

    def hasFocus(self):
        return not self.dom.focus == None

    def handleKey(self, key):
        self.dom.focus.press(key)

    def handleAudioData(self, data):
        sum_of_data = sum(data) / 1000
        self.audioBar.dimensions = (20, int(abs(sum_of_data)))