import moderngl
from GLClasses.ImageTexture import ImageTexture
from GLClasses.Mesh import Mesh
from GLClasses.ModelGeometry import ModelGeometry
import pygame
import math
import glm
class Scene:
    def __init__(self):
        self.ctx = moderngl.get_context()
        vertexShader = open("shaders/vertex.glsl", "r")
        fragmentShader = open("shaders/fragment.glsl", "r")
        self.program = self.ctx.program(
            vertex_shader=vertexShader.read(),
            fragment_shader=fragmentShader.read(),
        )
        vertexShader.close()
        fragmentShader.close()

        self.textureForBase = ImageTexture('Images/base.png')
        self.textureForHead = ImageTexture('Images/head.png')
        self.cube_geometry = ModelGeometry('models/cube.obj')
        self.base = Mesh(self.program, self.cube_geometry, self.textureForBase)
        self.head = Mesh(self.program, self.cube_geometry, self.textureForHead)
        
    def camera_matrix(self):
        now = pygame.time.get_ticks() / 1000.0
        eye = (0, 0, 0.5)
        proj = glm.perspective(45.0, 1.0, 0.1, 1000.0)
        look = glm.lookAt(eye, (0.0, 0.0, 0.0), (0.0, 0.0, 1.0))
        return proj * look

    def render(self):
        camera = self.camera_matrix()

        self.ctx.clear()
        self.ctx.enable(self.ctx.DEPTH_TEST)

        self.program['camera'].write(camera)

        self.base.render((-0.4, 0.0, 0.0), (1.0, 0.0, 0.0), 0.2)
        self.head.render((0.0, 0.0, 0.0), (1.0, 1.0, 1.0), 0.2)
