######################################
# Import and initialize the librarys #
######################################
from code.api.core import log, coreFunc, os, pygame, pg, window

#################
# Setup logging #
#################
filename = os.path.basename(__file__).split('.')[0]
logger = log.get_logger(filename)
logger.info('Loading up {}...'.format(filename))


class Frame(coreFunc):
    def __init__(self, x:int = 0, y:int = 0, w:int = 0, h:int = 0):
        self.x:int = x
        self.y:int = y
        self.w:int = w
        self.h:int = h

    def size(self, scale:int = 1) -> tuple:
        return (int(self.w * scale), int(self.h * scale))

    def coord(self, surfaceCoord:tuple = (0, 0), scale:int = 1) -> tuple: 
        return (int((self.x + surfaceCoord[0]) * scale), int((self.y + surfaceCoord[1]) * scale))
    
    def rect(self): return (self.x, self.y, self.w, self.h)

    def move(self, x, y):
        self.x += x
        self.y += y

    def mouseIn(self, surfaceCoord:tuple = (0, 0)) -> bool:
        # Get current mouse position
        mousePos = pygame.mouse.get_pos()
        # Save surface coord to seperate variables
        s_x, s_y = surfaceCoord
        scale = window.scale
        # Return if in box
        return int((self.x + s_x)*scale) < mousePos[0] < int((self.x + self.w + s_x)*scale) and int((self.y + s_y)*scale) < mousePos[1] < int((self.y + self.h + s_y)*scale)