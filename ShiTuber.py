from Scene.Scene import Scene
from Scene.LogicalScene import LogicalScene
import os
from multiprocessing import Manager, Process, Value
from queue import Full
import pygame
from GameLoop import runGameLoop
import traceback
def renderLoop(scene):
    while True:     
        try:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                scene.logic_scene.addToInputEventQueue(event)
                
            scene.logic_scene.publishEventQueue()
                # events.append(event)
            # result = scene.logic_scene.addToInputEventQueue(events)
            # if result:
            #     return result
            scene.render()
            pygame.display.flip()
        except Full:
            print('falling behind input queue, inputs lost')
        except Exception as e:
            print(traceback.format_exc())

if __name__ == '__main__':
    with Manager() as manager:
        logic_scene = LogicalScene()
        shared_dictionary = manager.dict() 
        shared_dictionary['scene'] = logic_scene
        input_queue = manager.Queue(100)
        render_queue = manager.Queue(100)
        audio_buffer = Value('f', 0.0)
        logic_scene.setInputQueue(input_queue)
        logic_scene.setRenderQueue(render_queue)
        logic_scene.setAudioBuffer(audio_buffer)
        


        
        p = Process(target=runGameLoop, args=(shared_dictionary, input_queue, render_queue, audio_buffer))

        os.environ['SDL_WINDOWS_DPI_AWARENESS'] = 'permonitorv2'


        p.start()
        pygame.init()
        pygame.display.set_mode((1600, 900), flags=pygame.OPENGL | pygame.DOUBLEBUF, vsync=True)
        scene = Scene(logic_scene)
        renderLoop(scene)
        p.terminate()