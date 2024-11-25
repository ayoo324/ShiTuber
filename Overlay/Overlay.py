from PIL import Image, ImageDraw, ImageFont
import moderngl
import pygame
from uuid import uuid4
from Helpers.asyncHelpers import execute_multiple_calls
from Overlay.DOM import DOM
from Overlay.Components import TextDisplay, Input, Picture
import io
class Overlay:
    def __init__(self):
        self.dom = DOM()

        testTextDisplay = TextDisplay((0, 0), (100, 30))
        testTextDisplay.text='Test'
        testTextDisplay.fill='#F0F'
        self.dom.addComponent(testTextDisplay)

        testTextInputDisplay = Input((30, 30), (100, 30))
        testTextInputDisplay.text='Input'

        self.dom.addComponent(testTextInputDisplay)

        base = Picture((900, 800), (500, 500), "Images/base.png")
        self.dom.addComponent(base)

        head = Picture((900, 300), (100, 100), "Images/head.png")
        self.dom.addComponent(head)

    def render(self):
        self.dom.render()

    def click(self, coordinates):
        (x, y) = coordinates
        self.dom.click(x, y)

    def hasFocus(self):
        return not self.dom.focus == None

    def handleKey(self, key):
        self.dom.focus.press(key)