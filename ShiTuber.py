from GLClasses.Scene import Scene
import pygame
import os
import sys
os.environ['SDL_WINDOWS_DPI_AWARENESS'] = 'permonitorv2'
pygame.init()
pygame.display.set_mode((1600, 900), flags=pygame.OPENGL | pygame.DOUBLEBUF, vsync=True)

scene = Scene()

    
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