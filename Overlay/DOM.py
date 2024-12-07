class DOM():

    def __init__(self):
        self.canvas_map = {}
        self.focus = None
        self.overlay_map = {}

    def addComponent(self, component):
        for curX in range(component.pos_x, component.pos_x + component.width):
            if curX not in self.canvas_map:
                self.canvas_map[curX] = {}
            for curY in range(component.pos_y, component.pos_y + component.height):
                self.canvas_map[curX][curY] = component.identifier
        self.overlay_map[component.identifier] = component

    def removeComponent(self, component):
        for curX in range(component.pos_x, component.pos_x + component.width):
            for curY in range(component.pos_y, component.pos_y + component.height):
                del self.canvas_map[curX][curY]
        del self.overlay_map[component.identifier]

    def click(self, x, y):
        if x in self.canvas_map and y in self.canvas_map[x]:
            identifier = self.canvas_map[x][y]
            self.focus = self.overlay_map[identifier]
            self.focus.click()
        else:
            self.focus = None
    
    def getComponentById(self, identifier):
        return self.overlay_map[identifier]
