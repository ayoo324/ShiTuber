import moderngl
import pygame
import math
import glm
from Displayable.Displayable import Displayable
from Helpers.asyncHelpers import execute_multiple_calls
class Scene:
    eyeY = 1
    eyeX = 0
    eyeZ = 0
    posX = 0
    posY = 0
    posZ = 0
    displayables = {}
    keyMap = {}
    speed = 0.02
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
        self.addDisplayableToScene(Displayable(self.program, 'Images/base.png', 'models/cube.obj'))
        self.addDisplayableToScene(Displayable(self.program, 'Images/head.png', 'models/cube.obj'))
        
    def addDisplayableToScene(self, displayable):
        self.displayables[displayable.uuid] = displayable

    def camera_matrix(self):
        eye = (self.eyeX, self.eyeY, self.eyeZ)
        pos = (self.posX, self.posY, self.posZ)
        proj = glm.perspective(45.0, 1.0, 0.1, 1000.0)
        look = glm.lookAt(eye, pos, (0.0, 0.0, 1.0))
        return proj * look

    def render(self):
        self.handleDownKeys()
        self.checkMouseMovement()
        camera = self.camera_matrix()

        self.ctx.clear()
        self.ctx.enable(self.ctx.DEPTH_TEST)

        self.program['camera'].write(camera)
        execute_multiple_calls(*[obj.render() for uuid, obj in self.displayables.items()])

    def handleDownKeys(self):
        for key, value in self.keyMap.items():
            if value == True:
                if key == pygame.K_a:
                    self.posX -= self.speed
                if key == pygame.K_d:
                    self.posX += self.speed
                if key == pygame.K_w:
                    self.posZ -= self.speed
                if key == pygame.K_s:
                    self.posZ += self.speed

    def handleEvent(self, event):
        if event.type == pygame.KEYDOWN:
            self.keyMap[event.key] = True
        if event.type == pygame.KEYUP:
            self.keyMap[event.key] = False

    def checkMouseMovement(self):
        mouseMovement = pygame.mouse.get_rel()
        self.eyeX += mouseMovement[0]
        self.eyeY += mouseMovement[1]
