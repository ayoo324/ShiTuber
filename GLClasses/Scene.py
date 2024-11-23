import moderngl
import pygame
import math
import glm
from GLClasses.Overlay import Overlay
from Displayable.Displayable import Displayable
from Helpers.asyncHelpers import execute_multiple_calls
from Helpers.glmHelpers import getRotationMatrices
class Scene:
    depth = 1000.0
    displayables = {}
    actionMap = {}
    grabMouse = False
    focus = None
    def __init__(self):
        self.fps = 0.0
        self.clock = pygame.time.Clock()
        self.ctx = moderngl.get_context()
        self.overlay = Overlay(pygame.display.get_window_size())
        pygame.event.set_grab(self.grabMouse)

    def addDisplayableToScene(self, displayable):
        self.displayables[displayable.uuid] = displayable

    def render(self):
        self.clock.tick()

        self.handleDownKeys()
        if self.grabMouse:
            self.checkMouseMovement()

        self.ctx.clear()
        self.ctx.screen.use()
        self.overlay.render()

    def handleDownKeys(self):
        if self.grabMouse:
            for key, value in self.actionMap.items():
                if not value == False:
                    if key == pygame.K_a:
                        self.posX -= self.speed
                    if key == pygame.K_d:
                        self.posX += self.speed
                    if key == pygame.K_w:
                        self.posZ += self.speed
                    if key == pygame.K_s:
                        self.posZ -= self.speed
        else:
            for key, value in self.actionMap.items():
                if not value == False:
                    if self.overlay.hasFocus():
                        self.overlay.handleKey(value)

                    self.actionMap[key] = False


    def handleEvent(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LSHIFT:
                self.grabMouse = not self.grabMouse
                pygame.event.set_grab(self.grabMouse)
            else:
                self.actionMap[event.key] = event
        elif event.type == pygame.KEYUP:
            self.actionMap[event.key] = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.overlay.click(pygame.mouse.get_pos())


    def checkMouseMovement(self):

        if self.grabMouse:
            pygame.mouse.set_pos(tuple(element / 2 for element in pygame.display.get_window_size()))


