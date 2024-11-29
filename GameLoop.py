import time
import pygame
from queue import Full


def runGameLoop(managed_dictionary, input_queue, render_map):
    clock = pygame.time.Clock()
    scene = managed_dictionary['scene']
    scene.setInputQueue(input_queue)
    scene.setRenderMap(render_map)

    while True:     
        scene.tick()
        clock.tick()