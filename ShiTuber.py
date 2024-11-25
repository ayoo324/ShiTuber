from GLClasses.Scene import Scene
import pygame
import os
import sys
import pyaudio
import time
import numpy as np
os.environ['SDL_WINDOWS_DPI_AWARENESS'] = 'permonitorv2'
pygame.init()
pygame.display.set_mode((1600, 900), flags=pygame.OPENGL | pygame.DOUBLEBUF, vsync=True)

scene = Scene()
from Overlay.Overlay import CHUNK, RATE, CHANNELS

p = pyaudio.PyAudio()

def callback(in_data, frame_count, time_info, status):
    # print(in_data)
    data = np.fromstring(in_data, dtype=np.int16)
    scene.addAudioData(data)
    return (in_data, pyaudio.paContinue)

# Notice the extra stream callback...
stream = p.open(format=pyaudio.paInt16,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK,
                stream_callback=callback)

stream.start_stream()


def __main__():
    runGameLoop()

def runGameLoop():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            scene.handleEvent(event)

        scene.render()

        pygame.display.flip()
        

__main__()