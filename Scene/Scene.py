import moderngl
import pygame
from Overlay.Overlay import Overlay
from Renderable.Geometry import Geometry
from Renderable.ImageTexture import ImageTexture
from Renderable.Renderable import Renderable
from concurrent.futures import *
import glm
class Scene:
    depth = 1000.0
    render_map = {}
    def __init__(self, logic_scene):
        self.logic_scene = logic_scene
        self.overlay = Overlay()
        self.fps = 0.0
        self.clock = pygame.time.Clock()
        self.ctx = moderngl.get_context()
        self.screen = self.ctx.texture(pygame.display.get_window_size(), 4)
        self.depth = self.ctx.depth_texture(pygame.display.get_window_size())

        v1 = open('shaders/vertex.glsl')
        f1 = open('shaders/fragment.glsl')
        vert1 = v1.read()
        frag1 = f1.read()
        self.program = self.ctx.program(
            vert1,
            frag1
        )
        v1.close()
        f1.close()
        self.geoemtries = [
            Geometry('models/cube.obj')
        ]
        self.textures = [
            ImageTexture('images/head.png'),
            ImageTexture('images/base.png')
        ]
        self.render_array = []

    def load_render_queue(self):
        if not self.logic_scene.render_queue.empty():
            render_object = self.logic_scene.render_queue.get()
            self.load(Renderable(render_object))
    def camera_matrix(self):
        eye = (0.0, 0.0, 2.0)
        proj = glm.perspective(45.0, 1.0, 0.1, 1000.0)
        look = glm.lookAt(eye, (0.0, 0.0, 0.0), (0.0, -1.0, 0.0))
        return proj * look           

    def load(self, render_object):
        if render_object.mapped_object.id not in self.render_map:
            render_object.load(self.program, self.textures[render_object.mapped_object.texture_id],self.geoemtries[render_object.mapped_object.geometry_id])
            self.render_map[render_object.mapped_object.id] = render_object
            self.render_array.append(render_object.mapped_object.id)
        else:
            self.render_map[render_object.mapped_object.id].mapped_object = render_object.mapped_object
    previous_data = 0.0
    max_reduction = 50.0
    def render(self):
        self.load_render_queue()

        self.ctx.clear()

        self.ctx.enable(self.ctx.DEPTH_TEST)
        audio_data = self.logic_scene.lastAudioData.value
        if self.previous_data > audio_data:
            audio_data = self.previous_data - self.max_reduction

        self.program['camera'].write(self.camera_matrix())
        ms = self.clock.tick()
        # self.program['time_since_last_frame'] = ms

        for id in self.render_array:
            if id == 1:
                self.program['audio_data'] = audio_data + 1
                # self.program['previous_audio'] = self.previous_data + 1
                self.render_map[id].render()
                self.program['audio_data'] = 0.0
                # self.program['previous_audio'] = 0.0
            else:
                self.render_map[id].render()

        self.previous_data = audio_data
        self.overlay.audio_level.value = str((audio_data + 1))
        self.overlay.time_since_last_frame.value = str(ms)
        self.overlay.audio_bar.base.height = int((audio_data + 1))
        self.overlay.render()
        self.ctx.screen.use()