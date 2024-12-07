import pygame
from Renderable.Renderable import Renderable
from Helpers.database import db
class LogicalScene:
    displayables = {}
    actionMap = {}
    audio_buffer = []
    grabMouse = False
    focus = None
    lastAudioData = None
    input_queue = None
    render_queue = None
    transformedEvents = []
    def setInputQueue(self, input_queue):
        self.input_queue = input_queue
    def setRenderQueue(self, render_queue):
        self.render_queue = render_queue
    def setAudioBuffer(self, audio_buffer):
        self.audio_buffer = audio_buffer

    def submitToRenderQueue(self, renderable:Renderable):
        db.insert_renderable(renderable)
        self.render_queue.put(renderable.mapped_object)
    
    def addDisplayableToScene(self, displayable):
        self.displayables[displayable.uuid] = displayable

    def addAudioData(self, data):
        if self.audio_buffer is not None:
            self.audio_buffer.put(data)

    def tick(self):
        self.handleDownKeys()
        self.handleMouseMovement()

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

    def handleMouseMovement(self):
        if self.grabMouse:
            pygame.mouse.set_pos(tuple(element / 2 for element in pygame.display.get_window_size()))


    def handleAudioData(self):
        if self.audio_buffer is None or self.audio_buffer.empty():
            return
        self.lastAudioData = self.audio_buffer.get()

    def addToInputEventQueue(self, event):
        self.transformedEvents = []
        if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            self.transformedEvents.append({'type': event.type, 'key': event.key, 'unicode': event.unicode})
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.transformedEvents.append({'type': event.type, 'pos': pygame.mouse.get_pos()})
        return False
    def publishEventQueue(self):
        if len(self.transformedEvents) > 0:
            self.input_queue.put(self.transformedEvents)
    
    def handleEvents(self, events):
        for event in events:
            if event['type'] == pygame.KEYDOWN:
                if event['key'] == pygame.K_LSHIFT:
                    self.grabMouse = not self.grabMouse
                    pygame.event.set_grab(self.grabMouse)
                else:
                    self.actionMap[event['key']] = event
            elif event['type'] == pygame.KEYUP:
                self.actionMap[event['key']] = False
            elif event['type'] == pygame.MOUSEBUTTONDOWN:
                self.actionMap['last_click'] = event['pos']
    
    def fillActionMap(self):
        for i in range(0, 100):
            if self.input_queue.empty():
                break
            self.handleEvents(self.input_queue.get())