from GLClasses.Scene import Scene
from Displayable.LogicalScene import LogicalScene
import os
from multiprocessing import Manager, Process, Queue
from queue import Full
import pygame
from GameLoop import runGameLoop
def renderLoop(scene):
    while True:     
        try:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return True
                scene.logic_scene.addToInputEventQueue(event)
            scene.render()
            pygame.display.flip()
        except Full:
            print('falling behind input queue, inputs lost')


if __name__ == '__main__':
    with Manager() as manager:
        logic_scene = LogicalScene()
        shared_dictionary = manager.dict() 
        shared_dictionary['scene'] = logic_scene
        render_map = manager.dict()
        input_queue = manager.Queue(100)
        audio_queue = manager.Queue(10)
        logic_scene.setInputQueue(input_queue)
        logic_scene.setAudioQueue(audio_queue)
        logic_scene.setRenderMap(render_map)
        p = Process(target=runGameLoop, args=(shared_dictionary, input_queue, audio_queue, render_map))

        os.environ['SDL_WINDOWS_DPI_AWARENESS'] = 'permonitorv2'
        pygame.init()
        pygame.display.set_mode((1600, 900), flags=pygame.OPENGL | pygame.DOUBLEBUF, vsync=True)
        scene = Scene(logic_scene)


        p.start()
        renderLoop(scene)
        p.terminate()