import random
import time
from AudioSettings import *
MAX_MOVEMENT_X = 20
MAX_MOVEMENT_Y = 40
flipCooldown = 0.15
class LogicOverlay:
    dom = None

    def click(self, coordinates):
        (x, y) = coordinates
        self.dom.click(x, y)

    def hasFocus(self):
        return not self.dom.focus == None

    def handleKey(self, key):
        self.dom.focus.press(key)

    def setDOM(self, dom):
        self.dom = dom

    # sign = -1
    # last_average_of_data = 0
    # max_average_crawl = 10
    # lastFlipTime = time.time()
    # def handleAudioData(self, data):
    #     average_of_data = int(abs(sum(data) / CHUNK))
    #     head = self.overlay_map.values()[1]
    #     if average_of_data > AUDIO_THRESHOLD:
    #         if self.last_average_of_data < average_of_data:
    #             head.up()
    #             if self.sign >= 0:
    #                 head.right()
    #             else:
    #                 head.left()
    #         elif self.last_average_of_data > average_of_data:
    #             head.down()
    #             head.center()

    #         now = time.time()
    #         if self.lastFlipTime + flipCooldown < now:
    #             self.lastFlipTime = now
    #             if random.randint(0, 3) == 1:
    #                 self.sign = self.sign * -1
    #     else:
    #         head.down()
    #         head.center()
    #     self.last_average_of_data = max(self.last_average_of_data + self.max_average_crawl, average_of_data)