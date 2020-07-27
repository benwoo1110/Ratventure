######################################
# Import and initialize the librarys #
######################################
import os
import textwrap
import inspect
import random
import math
import time
import re


#################
# Setup logging #
#################
filename = os.path.basename(__file__).split('.')[0]
logger = log.get_logger(filename)
logger.info('Loading up {}...'.format(filename))


class objectFrame(coreFunc):
    def __init__(self, coords):
        self.__dict__.update(**coords)


class coord(coreFunc):
    def __init__(self, scale:bool = False, x:int = 0, y:int = 0, w:int = 0, h:int = 0):
        self.x:int = x
        self.y:int = y
        self.w:int = w
        self.h:int = h

    def __getattr__(self, name, scale:bool = False): 
        if scale: return int(self.__dict__[name] * config.scale_w())
        else: return int(self.__dict__[name])

    def size(self, scale:bool = False) -> tuple: return (self.__getattr__('w', scale), self.__getattr__('h', scale))

    def coord(self, surfaceCoord:tuple = (0, 0), scale:bool = False) -> tuple: return (self.__getattr__('x', scale) + surfaceCoord[0], self.__getattr__('y', scale) + surfaceCoord[1])
    
    def rect(self, scale:bool = False): return (self.__getattr__('x', scale), self.__getattr__('y', scale), self.__getattr__('w', scale), self.__getattr__('h', scale))

    def move(self, x, y):
        self.x += x
        self.y += y

    def mouseIn(self, surfaceCoord:tuple = (0, 0), scale:bool = True) -> bool:
        # Get current mouse position
        mousePos = pygame.mouse.get_pos()
        # Save surface coord to seperate variables
        scroll_x, scroll_y = surfaceCoord
        # Return if in box
        return self.__getattr__('x', scale) + scroll_x < mousePos[0] < self.__getattr__('x', scale) + self.__getattr__('w', scale) + scroll_x and self.__getattr__('y', scale) + scroll_y < mousePos[1] < self.__getattr__('y', scale) + self.__getattr__('h', scale) + scroll_y


class screen(coreFunc):
    def __init__(self, name: str, surfaceParameters:dict = {}, objectsParameters:dict = {}, keyboardParameters:dict = {}, actionParameters:dict = {}):
        self.name = name
        self.surface = surface(self, **surfaceParameters)
        self.objects = objects(self, objectsParameters)
        self.keyboardActions = keyboardActions(self, keyboardParameters)
        self.actions = actions(self, actionParameters)
        self.event = event(self)

        # Load the screen
        self.surface.load()

        logger.debug('[{}] {}'.format(self.name, self.__repr__()))


class surface(coreFunc):
    def __init__(self, screen, frame:coord = coord(), bgColour:tuple = pg_ess.colour.orange, isAlpha:bool = False, scroll:bool = True):
        self.__screen__ = screen
        self.frame = frame
        self.bgColour = bgColour
        self.isAlpha = isAlpha
        self.scroll = scroll
        
        self.frame.scale = True

        # Create surface
        self.create()
    
    def create(self):
        # Create window based on if is alpha
        if self.isAlpha: Surface = pygame.surface.Surface(self.frame.size(), pygame.SRCALPHA)
        else: Surface = pygame.surface.Surface(self.frame.size())
        # set background color
        if self.bgColour != None: Surface.fill(self.bgColour)
        # Save Surface to class
        self.Surface = Surface

    def load(self): self.__screen__.objects.load()

    def display(self, withLoad:bool = False, resetSurface:bool = False, animate:bool = False):
        # Use a new surface
        if resetSurface: self.create()
        # Update to latest state of objects
        if withLoad: self.load()

        # Animation
        speed = 0.4
        move_per_frame = int(config.screen.width // (config.framerate * speed))
        if animate:
            for x in range(config.screen.width, 0, -move_per_frame):
                window.blit(self.Surface, (x, self.frame.y))
                self.__screen__.event.actions()

        # Resize surface
        resizedSurface = pygame.transform.smoothscale(self.Surface, self.frame.size(scale=True))

        # Output to screen
        window.blit(resizedSurface, self.frame.coord())
        


class actions(coreFunc):
    def __init__(self, screen:screen, actionsMethods:dict = {}):
        self.__screen__ = screen
        # Add run actions
        for name,action_method in actionsMethods.items():
            if callable(action_method): self.add(name, action_method)
            else: logger.warn('[{}] Action method {} not callable. Skipping..'.format(self.__screen__.name, name))

    def add(self, name, data):
        self.__dict__[name] = data


class keyboardActions(coreFunc):
    def __init__(self, screen:screen, actions:dict):
        self.__screen__ = screen
        # Add keyboard actions
        for name,action_data in actions.items():
            self.add(name, action_data)

    def add(self, name, data):
        self.__dict__[name] = key(self.__screen__, name, **data)


class key(coreFunc):
    def __init__(self, screen, name, keys:set, onKey:str = 'down', useAscii:bool = True, runclass:runclass = None):
        self.__screen__ = screen
        self.name = name
        self.keys = keys
        self.onKey = onKey
        self.useAscii = useAscii
        self.runclass = runclass


class objects(coreFunc):
    def __init__(self, screen:screen, items:dict):
        self.__screen__ = screen
        # Add objects
        for name,item_data in items.items():
            self.add(name, item_data)

    def add(self, name, item_data):
        self.__dict__[name] = item(self.__screen__, name, **item_data)

    def getObjects(self, withItems:list = ['__all__'], excludeItems:list = []):
        items_to_load = []
        
        # Get included items items
        if withItems == ['__all__']: items_to_load = list(self.__dict__.keys())[1:]
        else: 
            for includeItem in withItems:
                if self.__dict__.get(includeItem) != None: items_to_load.append(includeItem)
                else: logger.warn('[{}] Unable to include {}. Item not in objects...'.format(self.__screen__.name, includeItem))

        # Remove the ones stated to exclude
        for excludeItem in excludeItems:
            try: items_to_load.remove(excludeItem)
            except ValueError: logger.warn('[{}] Unable to exclude {}. Item not in objects...'.format(self.__screen__.name, excludeItem))

        return items_to_load

    def load(self, withItems:list = ['__all__'], excludeItems:list = [], withState:str = None):
        # Calculate items to load
        items_to_load = self.getObjects(withItems, excludeItems)
        # Load items defined
        for name in items_to_load: self.__dict__[name].load(withState)

    def display(self, withItems:list = ['__all__'], excludeItems:list = [], withState:str = None, directToScreen:bool = False):
        # Load items directly to screen
        if directToScreen:
            # Calculate items to load
            items_to_load = self.getObjects(withItems, excludeItems)
            for name in items_to_load: self.__dict__[name].display(withState, directToScreen)

        # Load items defined to surface
        else: 
            self.load(withItems, excludeItems, withState)
            self.__screen__.surface.display()


class item(coreFunc):
    types = ('object', 'background', 'button', 'text', 'textfield')

    def __init__(self, screen, name:str, type:str, frame:dict, data:any = None, dataAddSelf:bool = False, 
    state:str = '', runclass:runclass = None, loadImages:bool = True, isAlpha: bool = False):
        self.__screen__ = screen
        self.name = name
        self.type = str(type)
        self.frame = objectFrame(frame)
        self.data = data
        self.dataAddSelf = dataAddSelf
        self.state = state
        self.runclass = runclass
        self.isAlpha = isAlpha

        # Add self to data
        if dataAddSelf and data != None: data['item'] = self
        
        # load images
        if loadImages: 
            self.images = images(imagePage=[screen.name, name], isAlpha=isAlpha)
            self.load()
        # No images loaded
        else: 
            self.images = None
            logger.warn('[{}] No image found for {} item.'.format(self.__screen__.name, self.name))

    def hasRunclass(self):
        return isinstance(self.runclass, runclass)
        
    def hasState(self, state:str): 
        # If not state define
        if state == None: return False
        # Check if state exist
        check = hasattr(self.images, self.type+state)
        if not check: logger.warn('[{}] {} does not have state "{}"'.format(self.__screen__.name, self.name, state))
        return check

    def switchState(self, toState:str, directToScreen:bool = False, withDisplay:bool = True):
        if self.state != toState and self.hasState(toState): 
            if withDisplay: self.display(withState=toState, directToScreen=directToScreen)
            else: self.load(withState=toState)

    def load(self, withState:str = None, withData:bool = True):
        # Set state if needed
        if self.hasState(withState): self.state = withState
        # Load item to surface
        Surface = self.__screen__.surface.Surface
        if images != None: Surface.blit(self.images.__dict__[self.type+self.state], (self.frame.image.coord()))
        # Load data
        if hasattr(self.data, 'load') and withData: self.data.load()

    def display(self, withState:str = None, withData:bool = True, directToScreen:bool = False):
        # Output item to screen
        if directToScreen: 
            # Set state
            if self.hasState(withState): self.state = withState
            # Display to screen
            if images != None: window.blit(self.images.__dict__[self.type+self.state], (self.frame.image.coord(self.__screen__.surface.frame.coord())))
            # Display data
            if hasattr(self.data, 'display') and withData: self.data.display(directToScreen=True)
            

        # Display to surface
        else: 
            self.load(withState)
            self.__screen__.surface.display()


class images(coreFunc):
    def __init__(self, imagePage:list, fileType:str = '.png', isAlpha:bool = False):
        self.imagePage = imagePage
        self.fileType = fileType
        self.isAlpha = isAlpha

        # Load the images
        image_dir_list = self.getFilesList()

        # get the image
        for image in image_dir_list:
            # Get name
            image_name = os.path.basename(image).split('.')[0]
            # Load image
            image_surface = pygame.image.load(image).convert_alpha() if isAlpha else pygame.image.load(image).convert()
            # Store image
            self.__dict__[image_name] = image_surface

    def getFilesList(self) -> list:
        # Define variables
        image_dir = os.path.join('surfaces', *self.imagePage, '*'+self.fileType)
        # If in code directory and not root, go back a step
        if os.path.basename(os.getcwd()) == 'code': image_dir = '../' + image_dir
        # Get list of image from dir
        return glob.glob(image_dir)


class textFormat(coreFunc):
    def __init__(self, fontType:str = None, fontSize:int = 36, colour:tuple = pg_ess.colour.white, 
    warpText:int = None, align:str = 'left', lineSpacing:int = 1):
        self.fontType = fontType
        self.fontSize = fontSize
        self.colour = colour
        self.warpText = warpText
        self.align = align
        self.lineSpacing = lineSpacing
        self.font = pygame.font.Font(self.fontType, self.fontSize)


class textValidate(coreFunc):
    def __init__(self, charsAllowed:list = list(range(32,65)) + list(range(91,127)) + [8], 
    inAscii:bool = True, regex:str = '[\w\D.]+', defaultText:str = 'default', customMethod:any = None):
        self.charsAllowed = charsAllowed
        self.inAscii = inAscii
        self.regex = re.compile(regex)
        self.defaultText = defaultText
        self.customMethod = customMethod

class text(coreFunc):
    def __init__(self, text:str = '', prefix:str = '', suffix:str = '', 
    format:textFormat = textFormat(), validation:textValidate = textValidate(), editable:bool = True):
        self.text = text
        self.prefix = prefix
        self.suffix = suffix
        self.format = format
        self.validation = validation
        self.editable = editable

    def validateChar(self, char, inAscii = True):
        if self.validation.inAscii and not inAscii: char = ord(char)
        elif not self.validation.inAscii and inAscii: char = chr(char)

        return char in self.validation.charsAllowed

    def validateText(self):
        valid = self.validation
        regexTexts = valid.regex.findall(self.text)

        if regexTexts == []: 
            self.text = valid.defaultText
            return False

        if len(regexTexts) > 1: 
            self.text = regexTexts[0]
            return False

        if regexTexts[0] == self.text: 
            if callable(valid.customMethod): return valid.customMethod(self.text)
            return True

    def getText(self):
        if self.item.state == 'Selected' and self.editable: return self.prefix+self.text+'_'+self.suffix
        else: return self.prefix+self.text+self.suffix

    def setText(self, text:str = None, prefix:str = None, suffix:str = None, withDisplay: bool = True):
        if text != None: self.text = text
        if prefix != None: self.prefix = prefix
        if suffix != None: self.suffix = suffix

        if withDisplay: self.item.display()
        else: self.item.load()

    def renderText(self):
        # Generate surface for text
        text_surface = pygame.surface.Surface(self.item.frame.text.size(), pygame.SRCALPHA)
        # Get text with prefix and suffix
        text = self.getText()
        
        # No warpText
        if self.format.warpText == None:
            text_surface.blit(self.format.font.render(text, True, self.format.colour), (0, 0))

        # Output multi-line text
        else:
            # Warp the text
            warpped_text = textwrap.wrap(text, width=self.format.warpText)
            # Print text to surface
            h = 0
            for line in warpped_text:
                # Render the text line and store to text surface
                rendered_text = self.format.font.render(line, True, self.format.colour)
                text_surface.blit(rendered_text, (0, h))
                # Set hight of next line
                h += self.format.font.size(line)[1] * self.format.lineSpacing
            
        return text_surface

    def load(self):
        # Get the text
        text_surface = self.renderText()
        # Output to surface
        Surface = self.item.__screen__.surface.Surface
        Surface.blit(text_surface, self.item.frame.text.coord())

    def display(self, directToScreen:bool = False):
        if directToScreen:
            # Get the text
            text_surface = self.renderText()
            # Output to screen
            window.blit(text_surface, self.item.frame.text.coord(self.item.__screen__.surface.frame.coord()))
        
        else:
            self.load()
            self.item.__screen__.surface.display()