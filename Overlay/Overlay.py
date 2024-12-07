from Overlay.DOMRenderer import DOMRenderer
from Overlay.LogicOverlay import LogicOverlay
from Overlay.Components import Picture, Rectangle, TextDisplay
import random
import time
from AudioSettings import *
MAX_MOVEMENT_X = 20
MAX_MOVEMENT_Y = 40
flipCooldown = 0.15
class Overlay:
    def __init__(self):
        self.logic_overlay = LogicOverlay()
        self.domRenderer = DOMRenderer()
        self.logic_overlay.setDOM(self.domRenderer.dom)

        # self.base = Picture((700, 690), (219, 201), "Images/base.png")
        # self.base.label = 'Base'
        # self.domRenderer.addComponent(self.base)
        # for component in self.base.getDebugInputs( (0, 0) ):
        #     self.domRenderer.addComponent(component)
        # self.head = Picture((760, 640), (80, 50), "Images/head.png")
        # self.head.label = 'Head'
        # self.head.base.speed_l = 3
        # self.head.base.speed_r = 3
        # self.head.base.speed_u = 5
        # self.head.base.speed_d = 5
        # self.head.base.decay_x = 0
        # self.head.base.decay_y = 0
        # self.head.base.max_l = 740
        # self.head.base.max_r = 780
        # self.head.base.max_u = 340
        # self.head.base.max_d = 640
        # self.head.base.max_velocity_x = 10
        # self.head.base.max_velocity_y = 5
        # self.domRenderer.addComponent(self.head)
        # for component in self.head.getDebugInputs( (250, 0) ):
        #     self.domRenderer.addComponent(component)

        self.audio_level = TextDisplay('Audio', (0, 0), (250, 80))
        self.domRenderer.addComponent(self.audio_level)

        self.time_since_last_frame = TextDisplay('MS', (0, 80), (250, 80))
        self.domRenderer.addComponent(self.time_since_last_frame)

        self.audio_bar = Rectangle('Audio Levels', (0, 260), (40, 10))
        self.domRenderer.addComponent(self.audio_bar)


    def render(self):
        self.domRenderer.render()

    def click(self, coordinates):
        (x, y) = coordinates
        self.domRenderer.click(x, y)

    def hasFocus(self):
        return not self.domRenderer.focus == None

    def handleKey(self, key):
        self.domRenderer.focus.press(key)