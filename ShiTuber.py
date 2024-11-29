from GLClasses.Scene import Scene
from Displayable.LogicalScene import LogicalScene
import os
from multiprocessing import Manager, Process, Queue
from queue import Full, Queue
import numpy as np 
import pygame
from AudioSettings import *
import pyaudio
from GameLoop import runGameLoop
def renderLoop(scene):
    while True:     
        try:
            result = scene.logic_scene.addToInputEventQueue([event for event in pygame.event.get()])
            if result:
                return result
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
        logic_scene.setInputQueue(input_queue)
        logic_scene.setRenderMap(render_map)
        
        def audio_callback(in_data, frame_count, time_info, status):
            data = np.frombuffer(in_data, dtype=np.int16)
            logic_scene.addAudioData(data)
            return (in_data, pyaudio.paContinue)

        p = pyaudio.PyAudio()

        streams = [p.open(format=pyaudio.paInt16,
                        channels=CHANNELS,
                        rate=rate,
                        input=True,
                        frames_per_buffer=CHUNK,
                        stream_callback=audio_callback) for rate in RATES
                    ]
        
        p = Process(target=runGameLoop, args=(shared_dictionary, input_queue, render_map))

        os.environ['SDL_WINDOWS_DPI_AWARENESS'] = 'permonitorv2'
        pygame.init()
        pygame.display.set_mode((1600, 900), flags=pygame.OPENGL | pygame.DOUBLEBUF, vsync=True)
        scene = Scene(logic_scene)


        for stream in streams:
            stream.start_stream()
        p.start()
        renderLoop(scene)
        p.terminate()