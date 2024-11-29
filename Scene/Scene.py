import moderngl
import pygame
from Overlay.Overlay import Overlay

class Scene:
    depth = 1000.0
    def __init__(self, logic_scene):
        self.logic_scene = logic_scene
        self.fps = 0.0
        self.clock = pygame.time.Clock()
        self.ctx = moderngl.get_context()
        self.clear_colors = (0.2, 0.0, 0.2, 0.5, 0)
        self.overlay = Overlay()
        
    def render(self):
        self.clock.tick()
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

