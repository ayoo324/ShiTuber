import pygame
class LogicalScene:
    displayables = {}
    actionMap = {}
    audioBuffer = []
    grabMouse = False
    focus = None
    lastAudioData = []
    input_queue = None
    audio_queue = None
    render_map = None
    def setInputQueue(self, input_queue):
        self.input_queue = input_queue
    def setRenderMap(self, render_map):
        self.render_map = render_map
    
    def addDisplayableToScene(self, displayable):
        self.displayables[displayable.uuid] = displayable

    def addAudioData(self, data):
        self.audioBuffer.append(data)

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
        if len(self.audioBuffer) > 0:
            self.lastAudioData = self.audioBuffer.pop(0)
            self.audioBuffer = self.audioBuffer[:5]

    def addToInputEventQueue(self, events):
        transformedEvents = []
        for event in events:
            if event.type == pygame.QUIT:
                    pygame.quit()
                    return True
            else:

                if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                    transformedEvents.append({'type': event.type, 'key': event.key, 'unicode': event.unicode})
                if event.type == pygame.MOUSEBUTTONDOWN:
                    transformedEvents.append({'type': event.type, 'pos': pygame.mouse.get_pos()})
        self.input_queue.put(transformedEvents)
        return False
    
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