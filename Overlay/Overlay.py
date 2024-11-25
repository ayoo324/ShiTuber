from PIL import Image, ImageDraw, ImageFont
import moderngl
import pygame
from uuid import uuid4
from Helpers.asyncHelpers import execute_multiple_calls
from Overlay.DOM import DOM
from Overlay.Components import TextDisplay, Input, Picture, Rectangle
import io
import random
import time
CHUNK = 8  # Samples: 1024,  512, 256, 128 frames per buffer
RATE = 44100  # Equivalent to Human Hearing at 40 kHz
CHANNELS = 1
AUDIO_THRESHOLD = 50
MAX_MOVEMENT_X = 20
MAX_MOVEMENT_Y = 40
flipCooldown = 0.15
class Overlay:
    def __init__(self):
        self.dom = DOM()

        self.base = Picture((700, 690), (219, 201), "Images/base.png")
        self.base.label = 'Base'
        self.dom.addComponent(self.base)
        for component in self.base.getDebugInputs( (0, 0) ):
            self.dom.addComponent(component)
        self.head = Picture((760, 640), (80, 50), "Images/head.png")
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
    last_average_of_data = 0
    last_sum = 0
    horizontal_movement = 0
    head_speed_up = 5
    head_speed_down = 3
    head_speed_horizontal = 3
    lastFlipTime = time.time()
    def handleAudioData(self, data):
        average_of_data = int(abs(sum(data) / CHUNK))
        cur_sum = self.last_sum

        if average_of_data > AUDIO_THRESHOLD:
            
            self.audioBar.dimensions = (20, int(average_of_data))
            if self.last_average_of_data > average_of_data:
                cur_sum = self.last_sum - self.head_speed_down
            if self.last_average_of_data < average_of_data:
                cur_sum = self.last_sum + self.head_speed_up

            now = time.time()
            if self.lastFlipTime + flipCooldown < now:
                self.lastFlipTime = now
                if random.randint(0, 3) == 1:
                    self.sign = self.sign * -1

            self.last_average_of_data = average_of_data
        else:
            cur_sum = self.last_sum - self.head_speed_down  
            self.last_average_of_data = cur_sum


        if cur_sum < 0:
            cur_sum = 0

        cur_horizontal_movement = self.horizontal_movement
        if average_of_data > AUDIO_THRESHOLD:

            if self.sign >= 0:
                cur_horizontal_movement = cur_horizontal_movement + self.head_speed_horizontal
            else:
                cur_horizontal_movement = cur_horizontal_movement - self.head_speed_horizontal

            if cur_horizontal_movement < -MAX_MOVEMENT_X:
                cur_horizontal_movement = -MAX_MOVEMENT_X
            if cur_horizontal_movement > MAX_MOVEMENT_X:
                cur_horizontal_movement = MAX_MOVEMENT_X
        else:
            if cur_horizontal_movement < 0:
                cur_horizontal_movement = cur_horizontal_movement + self.head_speed_horizontal
                if cur_horizontal_movement > 0:
                    cur_horizontal_movement = 0
            else:
                cur_horizontal_movement = cur_horizontal_movement - self.head_speed_horizontal
                if cur_horizontal_movement < 0:
                    cur_horizontal_movement = 0


        self.horizontal_movement = min(cur_horizontal_movement, MAX_MOVEMENT_X)
        moveX = self.horizontal_movement 
        moveY = min(cur_sum, MAX_MOVEMENT_Y)

        self.last_sum = cur_sum = min(cur_sum, MAX_MOVEMENT_Y)
        self.head.pos = (760 + int(moveX), max(0, 640 - int(moveY)))