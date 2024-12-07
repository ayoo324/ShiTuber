from Renderable.MappedObject import MappedObject
import random
import time
from AudioSettings import *
MAX_MOVEMENT_X = 20
MAX_MOVEMENT_Y = 40
flipCooldown = 0.15
class LogicRenderable():
    mesh = None
    mapped_object = None
    sign = -1
    last_average_of_data = 0
    max_average_crawl = 10
    lastFlipTime = time.time()
    def __init__(self, mapped_object: MappedObject):
        self.mapped_object = mapped_object

    def move_to(self, x, y, z):
        self.mapped_object.x = x
        self.mapped_object.y = y
        self.mapped_object.z = z

    def set_render_id(self, render_id):
        self.mapped_object.id = render_id