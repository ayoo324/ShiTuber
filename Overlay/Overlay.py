from PIL import Image, ImageDraw, ImageFont
import moderngl
import pygame
from uuid import uuid4
from Helpers.asyncHelpers import execute_multiple_calls
from Overlay.DOM import DOM
from Overlay.Components import TextDisplay, Input
class Overlay:
    def __init__(self, size):
        self.dom = DOM(size)

        testTextDisplay = TextDisplay()
        testTextDisplay.text='Test'
        testTextDisplay.x=0
        testTextDisplay.y=0
        testTextDisplay.width=100
        testTextDisplay.height=30
        testTextDisplay.fill='#F0F'
        self.dom.addComponent(testTextDisplay)

        testTextInputDisplay = Input()
        testTextInputDisplay.text='Input'
        testTextInputDisplay.x=30
        testTextInputDisplay.y=30
        testTextInputDisplay.width=100
        testTextInputDisplay.height=30

        self.dom.addComponent(testTextInputDisplay)

    def render(self):
        self.dom.render()

    def click(self, coordinates):
        (x, y) = coordinates
        self.dom.click(x, y)

    def hasFocus(self):
        return not self.dom.focus == None

    def handleKey(self, key):
        self.dom.focus.press(key)