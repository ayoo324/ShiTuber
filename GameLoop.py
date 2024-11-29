import pygame
from Renderable.Renderable import Renderable
from Renderable.MappedObject import MappedObject

def runGameLoop(managed_dictionary, input_queue, render_map, render_queue):
    clock = pygame.time.Clock()
    scene = managed_dictionary['scene']
    scene.setInputQueue(input_queue)
    scene.setRenderMap(render_map)
    scene.setRenderQueue(render_queue)
    testObject = Renderable(
            MappedObject(
                0,
                position=(0, 0, 0),
                scale=1.0,
                geometry_id=0,
                texture_id=0,
                program_id=0,
                color=(1.0, 1.0, 1.0)
            )
        )
    scene.submitToRenderQueue(
        testObject
    )
    while True:     
        scene.tick()
        clock.tick()