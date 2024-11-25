from PIL import Image, ImageDraw, ImageFont
import moderngl
import pygame
from uuid import uuid4
from Helpers.asyncHelpers import execute_multiple_calls
from Overlay.DOM import DOM
from Overlay.Components import TextDisplay, Input, Picture, Rectangle
import io
AUDIO_THRESHOLD = 30
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
    sign = -1
    last_sum_of_data = 0
    head_speed_up = 0.7
    head_speed_down = 2
    def handleAudioData(self, data):
        sum_of_data = abs(sum(data) / 1000)
        self.audioBar.dimensions = (20, int(sum_of_data))
        cur_sum = 0
        if self.last_sum_of_data > sum_of_data:
            cur_sum = self.last_sum_of_data - self.head_speed_down
        if self.last_sum_of_data < sum_of_data and sum_of_data > 5:
            cur_sum = self.last_sum_of_data + self.head_speed_up

        if sum_of_data > AUDIO_THRESHOLD:
            self.sign = self.sign * -1

        self.head.pos = (int(760 + (cur_sum * self.sign)), max(0, 20 - int(cur_sum)))

        self.last_sum_of_data = cur_sum