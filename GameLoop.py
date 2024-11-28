import time
import pygame
import pyaudio
import numpy as np 
from AudioSettings import *
from queue import Full


def runGameLoop(managed_dictionary, input_queue, audio_queue, render_map):
    clock = pygame.time.Clock()
    scene = managed_dictionary['scene']
    scene.setInputQueue(input_queue)
    scene.setAudioQueue(audio_queue)
    scene.setRenderMap(render_map)
    def audio_callback(in_data, frame_count, time_info, status):
        data = np.frombuffer(in_data, dtype=np.int16)
        try:
            scene.addAudioData(data)
        except Full:
            print('falling behind audio queue, audio lost')
        return (in_data, pyaudio.paContinue)

    p = pyaudio.PyAudio()

    streams = [p.open(format=pyaudio.paInt16,
                    channels=CHANNELS,
                    rate=rate,
                    input=True,
                    frames_per_buffer=CHUNK,
                    stream_callback=audio_callback) for rate in RATES
                ]
    for stream in streams:
        stream.start_stream()
    while True:     
        scene.tick()
        clock.tick()