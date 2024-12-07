import pygame
from Renderable.Renderable import Renderable
from Renderable.MappedObject import MappedObject

def runGameLoop(managed_dictionary, input_queue, render_queue, audio_buffer):
    clock = pygame.time.Clock()
    scene = managed_dictionary['scene']
    scene.setInputQueue(input_queue)
    scene.setRenderQueue(render_queue)
    scene.setAudioBuffer(audio_buffer)
    base = Renderable(
            MappedObject(
                position=(0.0, 0.0, 0.0),
                scale=0.3,
                geometry_id=0,
                texture_id=0,
                program_id=0,
                color=(1.0, 1.0, 1.0)
            )
        )
    head = Renderable(
            MappedObject(
                position=(0.0, 0.0, 0.3),
                scale=0.3,
                geometry_id=0,
                texture_id=1,
                program_id=0,
                color=(1.0, 1.0, 1.0)
            )
        )
    scene.submitToRenderQueue(
        base
    )
    scene.submitToRenderQueue(
        head
    )
    while True:     
        scene.tick()
        clock.tick()