import pygame
from Renderable.Renderable import Renderable
from Renderable.MappedObject import MappedObject
import pyaudio
import statistics
from AudioSettings import *
import numpy as np 

def runGameLoop(managed_dictionary, input_queue, render_queue, audio_buffer):
    clock = pygame.time.Clock()
    scene = managed_dictionary['scene']
    scene.setInputQueue(input_queue)
    scene.setRenderQueue(render_queue)
    scene.setAudioBuffer(audio_buffer)
    head = Renderable(
            MappedObject(
                position=(0.0, 0.0, 0.05),
                scale=0.2,
                geometry_id=0,
                texture_id=0,
                program_id=0,
                color=(1.0, 1.0, 1.0)
            )
        )
    body = Renderable(
            MappedObject(
                position=(0.0, 0.0, 0.3),
                scale=0.3,
                geometry_id=0,
                texture_id=1,
                program_id=1,
                color=(1.0, 1.0, 1.0)
            )
        )
    
    def audio_callback(in_data, frame_count, time_info, status):
        data = np.frombuffer(in_data, dtype=np.int16)
        val = np.abs(np.fft.fft(data))
        scene.setAudioData(statistics.fmean(val))
        return (in_data, pyaudio.paContinue)
    
    p = pyaudio.PyAudio()
    info = p.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')
    for i in range(0, numdevices):
        if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
            print("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))

    stream = p.open(
        format=pyaudio.paInt16,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK,
        stream_callback=audio_callback
    )

    stream.start_stream()

    scene.submitToRenderQueue(
        body
    )
    scene.submitToRenderQueue(
        head
    )
    while True:     
        scene.tick()
        clock.tick()