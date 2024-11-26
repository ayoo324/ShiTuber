from Overlay.DOM import DOM
from Overlay.Components import Picture, Rectangle
import random
import time
CHUNK = 128  # Samples: 1024,  512, 256, 128 frames per buffer
RATE = 44100  # Equivalent to Human Hearing at 40 kHz
CHANNELS = 1
AUDIO_THRESHOLD = 150
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
        self.head.speed = (3, 3, 5, 5)
        self.head.decay = (0, 0)
        self.head.max_pos = (740, 780, 340, 640)
        self.head.max_velocity = (10, 5)
        self.dom.addComponent(self.head)
        for component in self.head.getDebugInputs( (250, 0) ):
            self.dom.addComponent(component)

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
    max_average_crawl = 10
    lastFlipTime = time.time()
    def handleAudioData(self, data):
        average_of_data = int(abs(sum(data) / CHUNK))

        if average_of_data > AUDIO_THRESHOLD:
            if self.last_average_of_data > average_of_data:
                self.head.up()
                if self.sign >= 0:
                    self.head.right()
                else:
                    self.head.left()
            elif self.last_average_of_data < average_of_data:
                self.head.down()
                self.head.center()

            now = time.time()
            if self.lastFlipTime + flipCooldown < now:
                self.lastFlipTime = now
                if random.randint(0, 3) == 1:
                    self.sign = self.sign * -1
        else:
            self.head.down()
            self.head.center()
        self.last_average_of_data = max(self.last_average_of_data + self.max_average_crawl, average_of_data)