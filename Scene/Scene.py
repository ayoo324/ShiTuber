import moderngl
import pygame
from Renderable.Geometry import Geometry
from Renderable.ImageTexture import ImageTexture
from Renderable.Renderable import Renderable
from concurrent.futures import *
import glm
import math
class Scene:
    depth = 1000.0
    render_map = {}
    def __init__(self, logic_scene):
        self.logic_scene = logic_scene
        self.fps = 0.0
        self.clock = pygame.time.Clock()
        self.ctx = moderngl.get_context()
        self.screen = self.ctx.texture(pygame.display.get_window_size(), 4)
        self.depth = self.ctx.depth_texture(pygame.display.get_window_size())

        v1 = open('shaders/vertex.glsl')
        f1 = open('shaders/fragment.glsl')
        self.programs = [self.ctx.program(
            v1.read(),
            f1.read()
        )]
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
        eye = (0.0, 0.0, -2.0)
        proj = glm.perspective(45.0, 1.0, 0.1, 1000.0)
        look = glm.lookAt(eye, (0.0, 0.0, 0.0), (0.0, 1.0, 0.0))
        return proj * look           

    def load(self, render_object):
        if render_object.mapped_object.id not in self.render_map:
            render_object.load(self.programs[render_object.mapped_object.program_id], self.textures[render_object.mapped_object.texture_id],self.geoemtries[render_object.mapped_object.geometry_id])
        self.render_map[render_object.mapped_object.id] = render_object
        self.render_array.append(render_object.mapped_object.id)

    def render(self):
        self.clock.tick()

        self.ctx.clear()

        self.ctx.enable(self.ctx.DEPTH_TEST)
        
        self.programs[0]['camera'].write(self.camera_matrix())

        self.load_render_queue()

        for id in self.render_array:
            self.render_map[id].render()

        self.ctx.screen.use()