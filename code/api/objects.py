######################################
# Import and initialize the librarys #
######################################
from code.api.core import log, coreFunc, os, pygame, pg, screens, window
from code.api.events import event
from code.api.data.Frame import Frame
from code.api.data.Images import Images


#################
# Setup logging #
#################
filename = os.path.basename(__file__).split('.')[0]
logger = log.get_logger(filename)
logger.info('Loading up {}...'.format(filename))


class screen(coreFunc):
    def __init__(self, name: str, main, surfaces:dict = {}, keyboard:dict = {}, 
    addToScreens = True, bg_colour:tuple = None, selectable:bool = True):
        self.name = name
        self.main = main
        self.addToScreens = addToScreens
        self.bg_colour = bg_colour
        self.selectable = selectable
        self.frame = Frame(x=0, y=0, w=pg.width, h=pg.height)

        # Event setup
        self.event = event(self)
        # Keyboard actions
        self.keyboard = keyboard
    
        # Store surfaces
        self.loaded = []
        self.containerList = []
        for name, surfaceData in surfaces.items():
            self.addSurface(name, surfaceData)

        # Adding to data of all screen
        if addToScreens: screens.add(self.name, self)

        # Setting up screen
        self.Surface = pygame.surface.Surface(pg.size())
        self.load()

        # Log the content of the screen
        logger.debug('[{}] {}'.format(self.name, self.__repr__()))

    def addSurface(self, name, surfaceData:dict = {}):
        self.__dict__[name] = surface(screen=self, name=name, **surfaceData)
        self.containerList.append(name)

    def loadBackground(self):
        # Fill colour
        if self.bg_colour != None: self.Surface.fill(self.bg_colour)
        # Load image
        self.bg_image = Images([self.name], frame=self.frame)
        if self.bg_image.containerList != []: self.Surface.blit(self.bg_image.background, (0, 0))

    def load(self, surfaces:list = None):
        # Load background
        self.loadBackground()

        # Load all surfaces defined
        if surfaces == None: toLoad = self.containerList
        else: toLoad = surfaces

        for surface in toLoad: self.__dict__[surface].load()

        self.loaded = toLoad

    def display(self, surfaces:list = None, withLoad:bool = False):
        if withLoad: self.load(surfaces)

        # Resize surface
        resizedSurface = pygame.transform.smoothscale(self.Surface, pg.scaled_size())
        
        # Output to screen
        window.blit(resizedSurface, (0, 0))


class surface(coreFunc):
    def __init__(self, screen, name, frame:Frame, selectable:bool = True, bg_colour:tuple = None, **items):
        self.screen = screen
        self.name = name
        self.frame = frame
        self.selectable = selectable
        self.bg_colour = bg_colour

        self.Surface = pygame.surface.Surface(self.frame.size())
        
        # Store items
        self.loaded = []
        self.containerList = []
        for name, itemData in items.items():
            self.addItem(name, itemData)

        # Setting up surface
        self.load()

    def addItem(self, name, itemData:dict):
        self.__dict__[name] = item(**itemData, surface=self, name=name)
        self.containerList.append(name)

    def loadBackground(self):
        # Fill colour
        if self.bg_colour != None: self.Surface.fill(self.bg_colour)
        # Load image
        self.bg_image = Images([self.screen.name, self.name], frame=self.frame)
        if self.bg_image.containerList != []: self.Surface.blit(self.bg_image.background, (0, 0))

    def load(self, items:list = None):
        # Load background
        self.loadBackground()

        # Load all surfaces defined
        if items == None: toLoad = self.containerList
        else: toLoad = items

        for item in toLoad: self.__dict__[item].load()

        self.loaded = toLoad

    def display(self, items:list = None, withLoad:bool = False):
        if withLoad: self.load(items)

        Surface = self.screen.Surface
        Surface.blit(self.Surface, self.frame.coord())
        self.screen.display()


class item(coreFunc):
    def __init__(self, surface, name:str, type:str, frame:Frame, imageData:dict, 
    data:dict = {}, selectable: bool = True, state:str = '', action:any = None):
        self.surface = surface
        self.name = name
        self.selectable = selectable
        self.type = str(type)
        self.frame = frame
        self.state = state
        self.action = action

        # Get images
        self.images = Images(**imageData, imagePage=[surface.screen.name, surface.name, name])
        # If no image loaded
        if self.images.containerList == []: 
            logger.warn('[{}] No image found for {} item.'.format(self.surface.name, self.name))
        
        # Store data
        self.loaded = []
        self.containerList = []
        for name, dataData in data.items():
            self.addData(name, dataData)

        self.load()

    def addData(self, name, dataData):
        dataData.name = name
        dataData.item = self
        self.__dict__[name] = dataData
        self.containerList.append(name)
        
    def hasState(self, state:str): 
        # If not state define
        if state == None: return False
        # Check if state exist
        check = hasattr(self.images, self.type+state)
        if not check: logger.warn('[{}] {} does not have state "{}"'.format(self.surface.name, self.name, state))
        return check

    def switchState(self, toState:str, withDisplay:bool = True):
        if self.state != toState and self.hasState(toState): 
            self.state = toState
            if withDisplay: self.display()
            else: self.load()

    def load(self, datas:list = None):
        # Get surface
        Surface = self.surface.Surface

        # Load image
        if self.images.containerList != []: 
            Surface.blit(self.images.__dict__[self.type+self.state], (self.images.frame.coord()))

        # Load all data defined
        if datas == None: toLoad = self.containerList
        else: toLoad = datas

        for data in self.containerList:
            if hasattr(self.__dict__[data], 'load'): self.__dict__[data].load()

        self.loaded = toLoad

    def display(self, datas:list = None):
        self.load(datas)
        self.surface.display()