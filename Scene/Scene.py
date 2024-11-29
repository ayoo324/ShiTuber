import moderngl
import pygame
from Overlay.Overlay import Overlay
from Renderable.Geometry import Geometry
from Renderable.ImageTexture import ImageTexture
from concurrent.futures import *
import multiprocessing as mp
from ctypes import *
class Scene:
    depth = 1000.0
    render_map = {}
    def __init__(self, logic_scene):
        self.logic_scene = logic_scene
        self.fps = 0.0
        self.clock = pygame.time.Clock()
        self.ctx = moderngl.get_context()
        self.clear_colors = (0.2, 0.0, 0.2, 0.5, 0)
        self.overlay = Overlay()
        self.programs = [self.ctx.program(
            open('shaders/vertex.glsl').read(),
            open('shaders/fragment.glsl').read()
        )]
        self.geoemtries = [
            Geometry('models/cube.obj')
        ]
        self.textures = [
            ImageTexture('images/base.png')
        ]
        self.executor = ThreadPoolExecutor(max_workers=4)
        # self.render_array = mp.Array(0, lock=False)
        self.render_array = []
    def load_render_queue(self):
        if not self.logic_scene.render_queue.empty():
            render_object = self.logic_scene.render_queue.get()
            # self.executor.submit(self.load, render_object)
            self.load(render_object)
            

    def load(self, render_object):
        render_object.load(self.programs[render_object.mapped_object.program_id], self.textures[render_object.mapped_object.texture_id],self.geoemtries[render_object.mapped_object.geometry_id])
        self.render_map[render_object.mapped_object.id] = render_object
        self.render_array.append(render_object.mapped_object.id)

    def render(self):
        self.clock.tick()
        self.load_render_queue()
        for id in self.render_array:
            self.render_map[id].render()


        self.handleOverlay()
        self.ctx.clear(
            self.clear_colors[0],
            self.clear_colors[1], 
            self.clear_colors[2], 
            self.clear_colors[3], 
            self.clear_colors[4]
        )
        self.ctx.screen.use()
        self.overlay.render()
            
    def handleOverlay(self):
        pygame.event.set_grab(self.logic_scene.grabMouse)
        self.logic_scene.handleAudioData()
        if len(self.logic_scene.lastAudioData) > 0:
            self.overlay.handleAudioData(self.logic_scene.lastAudioData)
        self.logic_scene.fillActionMap()
        if not self.logic_scene.grabMouse:
            for key, value in self.logic_scene.actionMap.items():
                if not value == False:
                    if key == 'last_click' :
                        self.overlay.click(value)
                    elif self.overlay.hasFocus():
                        self.overlay.handleKey(value)

                    self.logic_scene.actionMap[key] = False

