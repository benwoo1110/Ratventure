######################################
# Import and initialize the librarys #
######################################
import textwrap
import random
import math
import time
import re
import glob
from code.api.core import log, coreFunc, os, screens, pg, pygame, window
from code.api.events import runclass


#################
# Setup logging #
#################
filename = os.path.basename(__file__).split('.')[0]
logger = log.get_logger(filename)
logger.info('Loading up {}...'.format(filename))


class coord(coreFunc):
    def __init__(self, x:int = 0, y:int = 0, w:int = 0, h:int = 0):
        self.x:int = x
        self.y:int = y
        self.w:int = w
        self.h:int = h

    def size(self) -> tuple: return (self.w, self.h)

    def coord(self, surfaceCoord:tuple = (0, 0)) -> tuple: return (self.x + surfaceCoord[0], self.y + surfaceCoord[1])
    
    def rect(self): return (self.x, self.y, self.w, self.h)

    def move(self, x, y):
        self.x += x
        self.y += y

    def mouseIn(self, surfaceCoord:tuple = (0, 0)) -> bool:
        # Get current mouse position
        mousePos = pygame.mouse.get_pos()
        # Save surface coord to seperate variables
        s_x, s_y = surfaceCoord
        # Return if in box
        return self.x + s_x < mousePos[0] < self.x + self.w + s_x and self.y + s_y < mousePos[1] < self.y + self.h + s_y


class images(coreFunc):
    def __init__(self, imagePage:list, fileType:str = '.png'):
        self.imagePage = imagePage
        self.fileType = fileType

        self.containerList = []

        # Load the images
        image_dir_list = self.getFilesList()

        # get the image
        for image in image_dir_list:
            # Get name
            image_name = os.path.basename(image).split('.')[0]
            # Load image
            image_surface = pygame.image.load(image).convert_alpha()
            # Store image
            self.__dict__[image_name] = image_surface
            self.containerList.append(image_name)

    def getFilesList(self) -> list:
        # Define variables
        image_dir = os.path.join('surfaces', *self.imagePage, '*'+self.fileType)
        # Get list of image from dir
        return glob.glob(image_dir)


class screen(coreFunc):
    def __init__(self, name: str, surfaces:dict = {}, keyboard:dict = {}, addToScreens = True, bg_colour:tuple = None):
        self.name = name
        self.addToScreens = addToScreens
        self.bg_colour = bg_colour

        # Keyboard actions
        self.keyboard = keyboard
    
        # Store surfaces
        self.loaded = []
        self.containerList = []
        for name, surfaceData in surfaces.items():
            self.addSurface(name, surfaceData)

        # Adding to data of all screen
        if addToScreens: screens.add(self.name, self)

        # Setting up surface
        self.Surface = pygame.surface.Surface(pg.size())
        self.load()

        # Log the content of the screen
        logger.debug('[{}] {}'.format(self.name, self.__repr__()))

    def addSurface(self, name, surfaceData:dict = {}):
        self.__dict__[name] = surface(self, name, **surfaceData)
        self.containerList.append(name)

    def loadBackground(self):
        # Fill colour
        if self.bg_colour != None: self.Surface.fill(self.bg_colour)
        # Load image
        self.bg_image = images([self.name])
        self.Surface.blit(self.bg_image.background, (0, 0))

    def load(self, surfaces:list = None):
        # Load background
        self.loadBackground()

        # Load all surfaces defined
        if surfaces == None: toLoad = self.containerList
        else: toLoad = surfaces

        for surface in toLoad: self.__dict__[surface].load()

    def display(self, withLoad:bool = False):
        if withLoad: self.load()

        # Resize surface
        resizedSurface = pygame.transform.smoothscale(self.Surface, pg.scaled_size())
        
        # Output to screen
        window.blit(resizedSurface, (0, 0))

        pg.updateDisplay()


class surface(coreFunc):
    def __init__(self, screen, name, items:dict = {}, selectable:bool = True):
        self.screen = screen
        self.name = name
        self.selectable = selectable
        
        # Store items
        self.containerList = []
        for name, itemData in items.items():
            self.addItem(name, itemData)

    def addItem(self, name, itemData:dict):
        self.__dict__[name] = item(self, name, **itemData)
        self.containerList.append(name)


class item(coreFunc):
    def __init__(self, surface, name:str, type:str, frame:coord, data:dict = {}, selectable: bool = True,
    state:str = '', runclass:runclass = None, loadImages:bool = True):
        self.surface = surface
        self.name = name
        self.selectable = selectable
        self.type = str(type)
        self.frame = frame
        self.state = state
        self.runclass = runclass

        # load images
        if loadImages: 
            self.images = images(imagePage=[surface.screen.name, surface.name, name])
            self.load()
        # No images loaded
        else: 
            self.images = None
            logger.warn('[{}] No image found for {} item.'.format(self.surface.name, self.name))

        # Store data
        self.containerList = []
        for name, dataData in items.items():
            self.addData(name, dataData)

    def addData(self, name, dataData:dict):
        self.__dict__[name] = item(self, name, **dataData)
        self.containerList.append(name)

    def hasRunclass(self):
        return isinstance(self.runclass, runclass)
        
    def hasState(self, state:str): 
        # If not state define
        if state == None: return False
        # Check if state exist
        check = hasattr(self.images, self.type+state)
        if not check: logger.warn('[{}] {} does not have state "{}"'.format(self.surface.name, self.name, state))
        return check

    def switchState(self, toState:str, directToScreen:bool = False, withDisplay:bool = True):
        if self.state != toState and self.hasState(toState): 
            if withDisplay: self.display(withState=toState, directToScreen=directToScreen)
            else: self.load(withState=toState)