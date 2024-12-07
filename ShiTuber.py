from Scene.Scene import Scene
from Scene.LogicalScene import LogicalScene
import os
from multiprocessing import Manager, Process
from queue import Full
import numpy as np 
import pygame
from AudioSettings import *
import pyaudio
from GameLoop import runGameLoop
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
            print(e)

if __name__ == '__main__':
    with Manager() as manager:
        logic_scene = LogicalScene()
        shared_dictionary = manager.dict() 
        shared_dictionary['scene'] = logic_scene
        input_queue = manager.Queue(100)
        render_queue = manager.Queue(100)
        audio_buffer = manager.Queue(100)
        logic_scene.setInputQueue(input_queue)
        logic_scene.setRenderQueue(render_queue)
        logic_scene.setAudioBuffer(audio_buffer)
        
        # def audio_callback(in_data, frame_count, time_info, status):
        #     data = np.frombuffer(in_data, dtype=np.int16)
        #     logic_scene.addAudioData(data)
        #     return (in_data, pyaudio.paContinue)

        # p = pyaudio.PyAudio()

        # streams = [p.open(format=pyaudio.paInt16,
        #                 channels=CHANNELS,
        #                 rate=rate,
        #                 input=True,
        #                 frames_per_buffer=CHUNK,
        #                 stream_callback=audio_callback) for rate in RATES
        #             ]
        
        p = Process(target=runGameLoop, args=(shared_dictionary, input_queue, render_queue, audio_buffer))

        os.environ['SDL_WINDOWS_DPI_AWARENESS'] = 'permonitorv2'


        # for stream in streams:
        #     stream.start_stream()
        p.start()
        pygame.init()
        pygame.display.set_mode((1600, 900), flags=pygame.OPENGL | pygame.DOUBLEBUF, vsync=True)
        scene = Scene(logic_scene)
        renderLoop(scene)
        p.terminate()