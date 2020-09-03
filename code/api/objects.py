######################################
# Import and initialize the librarys #
######################################
import concurrent.futures
from code.api.core import log, coreFunc, os, pygame, PgEss, screens, window
from code.api.events import Events
from code.api.actions import keyboardActions
from code.api.data.Frame import Frame
from code.api.data.Images import Images
from code.api.data.Sound import Sound


#################
# Setup logging #
#################
filename = os.path.basename(__file__).split('.')[0]
logger = log.get_logger(filename)


##################
# Object classes #
##################
class Screen(coreFunc):
    def __init__(self, name: str, main:any, surfaces:dict = None, keyboard:dict = None, bg_colour:tuple = None, 
    seperateBackground:bool = False, selectable:bool = True, firstLoad:list = 'all', alpha:bool = False):
        self.name = name
        self.main = main
        self.bg_colour = bg_colour
        self.selectable = selectable
        self.frame = Frame(x=window.x, y=window.y, w=window.width, h=window.height)
        self.alpha = alpha

        # Event setup
        self.events = Events(self)

        # Keyboard actions
        self.keyboard = keyboardActions(self, keyboard)

        # Setting up screen
        if self.alpha: self.Screen = pygame.surface.Surface(window.size(), pygame.SRCALPHA)
        else: self.Screen = pygame.surface.Surface(window.size())

        # Get background image
        self.seperateBackground = seperateBackground
        self.bg_image = Images([self.name], (0, 0))
        self.loadBackground()
    
        # Load surfaces
        self.loaded = []
        self.containerList = []

        if surfaces != None:
            for name, surfaceData in surfaces.items(): self.addSurface(name, surfaceData)

        self.load(withSurfaces=firstLoad, refresh=True)

        # Adding to data of all screen
        screens.add(self.name, self)

    def addSurface(self, name, surfaceData:dict = {}):
        setattr(self, name, Surface(screen=self, name=name, **surfaceData))
        self.containerList.append(name)

    def unload(self, withSurfaces:list = 'all'):
        # Get all surfaces defined
        if withSurfaces == 'all': toUnload = self.containerList
        else: toUnload = withSurfaces

        # Unload them
        for Surface in toUnload: 
            surface_toUnload = getattr(self, Surface)
            if surface_toUnload.loaded: surface_toUnload.unload()

    def load(self, withSurfaces:list, refresh:bool = False, withBackground:bool = False):
        # Display background on window
        if withBackground: self.loadBackground()
        
        # Get list of surface to load
        if withSurfaces == None: 
            logger.warn('[{}] No surfaces to load.'.format(self.name))
            return
        elif withSurfaces == 'all': toLoad = self.containerList
        else: toLoad = withSurfaces

        # Load all surfaces defined
        for Surface in toLoad: 
            if refresh: getattr(self, Surface).load(withItems='all', refresh=refresh)
            else: getattr(self, Surface).load()

    def loadBackground(self):
        if self.seperateBackground:
            # Create a seperate background surface
            self.background = pygame.surface.Surface(window.size(), pygame.SRCALPHA)

            # Fill colour
            if self.bg_colour != None: self.background.fill(self.bg_colour)
            
            # Load background image
            if 'background' in self.bg_image.containerList: 
                self.background.blit(self.bg_image.background, (0, 0))

        else:
            # Fill colour
            if self.bg_colour != None: self.Screen.fill(self.bg_colour)
            
            # Load background image
            if 'background' in self.bg_image.containerList: 
                self.Screen.blit(self.bg_image.background, (0, 0))

    def display(self, withSurfaces:list = None, refresh:bool = False, withBackground:bool = False):
        # Load surfaces
        if withSurfaces != None: self.load(withSurfaces, refresh, withBackground)
        
        # Trigger a window update
        if self.seperateBackground: screens.triggerUpdate(withBackground=withBackground)
        else: screens.triggerUpdate()


class Surface(coreFunc):
    def __init__(self, screen, name, frame:Frame, selectable:bool = True, 
    bg_colour:tuple = None, directDisplay:bool = False, alpha:bool = False, **items):
        self.screen = screen
        self.name = name
        self.frame = frame
        self.selectable = selectable
        self.bg_colour = bg_colour
        self.directDisplay = directDisplay
        self.alpha = alpha

        # Create surface
        if self.alpha: self.Surface = pygame.surface.Surface(self.frame.size(), pygame.SRCALPHA)
        else: self.Surface = pygame.surface.Surface(self.frame.size())
        
        # Get background image
        self.bg_image = Images([self.screen.name, self.name], frame=self.frame, alpha=alpha)
        self.loadBackground()

        # Store items
        self.loaded = False
        self.containerList = []
        for name, itemData in items.items(): self.addItem(name, itemData)

    def addItem(self, name, itemData:dict):
        setattr(self, name, Item(surface=self, name=name, **itemData))
        self.containerList.append(name)

    def unload(self):
        if self.loaded: self.loaded = False
        else: logger.warn('Surface {} already unloaded.'.format(self.name))

    def load(self, withItems:list = None, refresh:bool = False):
        # Get item list to load
        if withItems == None: toLoad = []
        elif withItems == 'all': toLoad = self.containerList
        else: toLoad = withItems
        
        # Load all items defined
        for item in toLoad: 
            if refresh: getattr(self, item).load(withData='all')
            else: getattr(self, item).load()

        # Load to screen
        self.screen.Screen.blit(self.Surface, self.frame.coord())

        self.loaded = True

    def loadBackground(self):
        # Fill colour
        if self.bg_colour != None: self.Surface.fill(self.bg_colour)
        # Display to screen
        if 'background' in self.bg_image.containerList: 
            self.Surface.blit(self.bg_image.background, (0, 0))

    def display(self, withItems:list = None, refresh:bool = False):        
        # Load the surface with items
        self.load(withItems, refresh)

        # Directly display to window
        if self.directDisplay:
            # Resize surface
            resizedSurface = pygame.transform.smoothscale(self.Surface, self.frame.size(scale=window.scale))
            
            # Output to window
            window.Window.blit(resizedSurface, self.frame.coord(surfaceCoord=window.coord(), scale=window.scale))
            PgEss.updateWindow()
        
        else:
            # Load to screen
            self.screen.display()


class Item(coreFunc):
    def __init__(self, surface:Surface, name:str, type:str, frame:Frame, imageData:dict = None, overlayDataFrame:bool = False, data:dict = None, 
    selectable: bool = True, state:str = '', action:any = None, lock_state:bool = False, clickSound:Sound = Sound.button_click):
        self.surface = surface
        self.name = name
        self.selectable = selectable
        self.type = str(type)
        self.frame = frame
        self.state = state
        self.action = action
        self.lock_state = lock_state
        self.overlayDataFrame = overlayDataFrame
        self.clickSound = clickSound

        # Get images
        if imageData != None:
            self.images = Images(**imageData, imagePage=[surface.screen.name, surface.name, name])
            # If no image loaded
            if self.images.containerList == []: 
                logger.warn('[{}] No image found for {} item.'.format(self.surface.name, self.name))
        
        # No image defined for item
        else: self.images = None
        
        # Store data
        self.loaded = False
        self.containerList = []

        if data != None:
            for name, dataData in data.items(): self.addData(name, dataData)

    def addData(self, name, dataData):
        if hasattr(dataData, 'name'): dataData.name = name
        if hasattr(dataData, 'item'): dataData.item = self
        if hasattr(dataData, 'frame') and self.overlayDataFrame: dataData.frame.overlayCoord(self.frame.coord())
        setattr(self, name, dataData)
        self.containerList.append(name)

    def isState(self, state:str): return state == self.state
        
    def hasState(self, state:str): 
        # If not state define
        if state == None: return False
        # Check if state exist
        return hasattr(self.images, self.type+state)

    def switchState(self, toState:str, withLoad:bool = True, withDisplay:bool = True):
        # Change the state
        if self.state != toState and self.hasState(toState):
            # Ensure that item is not locked
            if not self.lock_state: self.state = toState
            else: return

            # Load/display to screen
            if withLoad:
                if withDisplay: self.display()
                else: self.load()

    def unload(self):
        if self.loaded: self.loaded = False
        else: logger.warn('Item {} already unloaded.'.format(self.name))

    def load(self, withData:list = 'all'):
        # Load image
        if self.images != None and self.images.containerList != []: 
            self.surface.Surface.blit(getattr(self.images, self.type+self.state), (self.images.frame.coord()))

        self.loaded = True

        # Load all data defined
        if withData == None: return
        elif withData == 'all': toLoad = self.containerList
        else: toLoad = withData

        for data in toLoad:
            data_object = getattr(self, data)
            if hasattr(data_object, 'load'): data_object.load()

    def display(self, withData:list = 'all'):
        # Load the item to surface
        self.load(withData)
        # Display to surface
        self.surface.display()