######################################
# Import and initialize the librarys #
######################################
import os
import logging
import sys
import glob
import traceback
import json
import pygame
from functools import wraps
from datetime import datetime
from code.config import config


#####################
# Core parent class #
#####################
class coreFunc:
    def __setitem__(self, name, value): self.__dict__[name] = value
    def __setattr__(self, name, value): self.__dict__[name] = value
    def __getitem__(self, name): return self.__dict__[name]
    def __str__(self): return '{}'.format(self.__dict__)
    def __repr__(self): return '{}'.format(self.__dict__)

    def __iter__(self):
        self.counter = 0
        return self

    def __next__(self):
        if self.counter >= len(self.containerList):
            self.counter = 0
            raise StopIteration

        current = getattr(self, self.containerList[self.counter])
        self.counter += 1
        return current


###################
# Common function #
###################
class pg:
    config = config.get()
    keypressed = []
    clock = pygame.time.Clock()
    tick = clock.tick_busy_loop if config.tick_busy else clock.tick

    class font:
        '''fonts found in fonts folder'''
        knigqst = './fonts/Knigqst.ttf'

    class colour:
        '''Common colour types in RGB tuple format'''
        black = (0, 0, 0)
        white = (255, 255, 255)
        red = (181, 23, 0)
        blue = (0, 77, 128)
        green = (1, 113, 0)
        purple = (97, 0, 188)

    @staticmethod
    def loadJson(filepath:str, default = None) -> dict:
        '''Loading of file from json'''
        try:
            with open(filepath, 'r') as datafile:
                data = json.load(datafile)

        except FileNotFoundError:
            # If no default set
            if default == None: print('{} file does not exist.')

            # Create file at filepath with the given default variable
            else: 
                pg.saveJson(filepath, default)
                return default

        except Exception as e: logger.error(e, exc_info=True)

        else: 
            logger.info('Loaded json file from {}'.format(filepath))
            return data

    @staticmethod
    def saveJson(filepath:str, data:dict):
        '''Saving file to json'''
        try:
            with open(filepath, 'w') as savefile:
                json.dump(data, savefile)

        except Exception as e: logger.error(e, exc_info=True)

        else: logger.info('Saved data to {}'.format(filepath))

    @staticmethod
    def createPath(path:str):
        if not os.path.isdir(path):
            # Create logs directory
            try: os.mkdir(path)
            except Exception as e: logger.error(e, exc_info=True)
            else: logger.info('Created {} directory'.format(path))


    @staticmethod
    def updateWindow():
        '''Displays screens/surfaces to pygame window'''
        pygame.display.update()
        pg.clock.tick(pg.config.framerate)

    @staticmethod
    def quit():
        '''Exit pygame program'''
        logger.info('Exiting program... Goodbye!')
        pygame.quit()


##########
# Window #
##########
class windowScreen(coreFunc):
    def __init__(self):
        # Set icon
        if os.path.isfile(pg.config.icon_file): 
            pygame.display.set_icon(pygame.image.load(pg.config.icon_file))

        elif pg.config.icon_file != '': 
            logger.warning('Error loading app icon image "{}"'.format(pg.config.icon_file))

        # Set title
        pygame.display.set_caption(pg.config.title)

        self.width = 1800
        self.height = 1080

        # Set display
        # Full screen mode
        if pg.config.fullscreen: 
            self.Window = pygame.display.set_mode(self.size(), pygame.FULLSCREEN)

            # Get fullscreen window size
            window_w, window_h = self.Window.get_size()
            
            # Set scaling
            self.scale = min(window_w / self.width, window_h / self.height)
            self.scaled_width = int(self.width * self.scale)
            self.scaled_height = int(self.height * self.scale)

            # Set coord to be center
            self.x = int((window_w - self.scaled_width) / 2)
            self.y = int((window_h - self.scaled_height) / 2)

        # Window mode, use scale
        else: 
            # Set scaling
            self.scale = pg.config.scale
            self.scaled_width = int(self.width * self.scale)
            self.scaled_height = int(self.height * self.scale)

            # Set coord
            self.x = 0
            self.y = 0

            self.Window = pygame.display.set_mode(self.scaled_size())

        # Show display information
        logger.debug(pygame.display.Info())

    def update(self):
        try:
            if screens.updateBackground:
                # Display background
                resizedSurface = pygame.transform.smoothscale(screens.getBackground(), self.scaled_size())
                self.Window.blit(resizedSurface, self.coord())

            # Display window
            resizedSurface = pygame.transform.smoothscale(screens.getScreen(), self.scaled_size())
            self.Window.blit(resizedSurface, self.coord())

            # Update
            pygame.display.update()
            pg.tick(pg.config.framerate)

        # Error
        except: logger.critical('Error updating pygame window!', exc_info=True)

        # Reset screen update trigger
        screens.updateBackground = False
        screens.update = False

    def size(self): return (self.width, self.height)

    def scaled_size(self): return (self.scaled_width, self.scaled_height)

    def coord(self): return (self.x, self.y)


##########
# Screen #
##########
class Screens(coreFunc):

    def __init__(self):
        self.containerList = []
        self.screensStack = []
        self.stackChange = False
        self.update = False
        self.updateBackground = True
    
    def add(self, name, screen):
        self.__dict__[name] = screen
        self.containerList.append(name)
        logger.debug('Added screen {}'.format(name))

    def getScreen(self): return getattr(self, self.screensStack[-1]).Screen

    def getBackground(self): return getattr(self, self.screensStack[-1]).background

    def triggerUpdate(self, withBackground:bool = False):
        self.update = True
        self.updateBackground = withBackground

    def changeStack(self, type:str, screen:str = None):
        # Notify another changeStack() is happening
        if self.stackChange: 
            logger.warning('Another stack change is happening as well, this may cause issues.')
        
        self.stackChange = True

        # Go back to previous screen
        if str(type) == 'back':
            # Go back one screen
            if screen == None: self.screensStack.pop()
            # Go back to screen specified
            elif screen in self.containerList: self.screensStack = self.screensStack[:self.screensStack.index(screen)+1]
            # Error
            else:
                logger.error('"{}" is not a screen.'.format(screen))
                return
        
        # Load a new screen
        elif type == 'load':  
            if screen in self.containerList: self.screensStack.append(screen)
            # Error
            else:
                logger.error('"{}" is not a screen.'.format(screen))
                return

        # Error
        else: 
            logger.error('{} type not recognised.'.format(type))
            return
        
        # Log change
        logger.debug('Change stack completed with type:{} screen:{}'.format(type, screen))
            
        return True

    def mainloop(self, startScreen:str):
        # Start with startScreen
        self.screensStack.append(startScreen)

        while True:
            # fallback to startScreen
            if self.screensStack == []: 
                self.screensStack.append(startScreen)
                logger.error('No screen in stack, falling back to startScreen.')

            # Get screen
            screen = getattr(self, self.screensStack[-1])

            # Run init code exist
            if hasattr(screen.main, 'init'): screen.main.init()

            # Display the screen
            screen.display(withBackground=True)

            # Log current screen stacks
            logger.debug('New screen stack of {}'.format(self.screensStack))
            
            # Main loop for top screen
            while not self.stackChange:

                # Check for updates wanted to screen
                if self.update: window.update()

                # Get result of screen actions
                screen_result = screen.main.run()

                # End program
                if screen_result == 'quit':
                    pygame.mixer.fadeout(500)
                    pg.quit()
                    return

            # When screen ends
            if hasattr(screen.main, 'end'): screen.main.end()
            self.stackChange = False


###########
# Logging #
###########
pg.createPath('./logs/')

# Keep only certain number of log files 
log_files = glob.glob("./logs/*.log")
log_files.sort(key=os.path.getmtime)

for index in range(len(log_files) - max(0, pg.config.logging.keep_logs-1)):
    os.remove(log_files[index])

# Setup log format and location
FORMATTER = logging.Formatter('[%(asctime)s %(levelname)s] [%(name)s] %(message)s', datefmt='%H:%M:%S')
LOG_FILE = datetime.now().strftime("./logs/%d-%m-%Y_%H-%M-%S.log")

# Console logging
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(level=os.environ.get("LOGLEVEL", pg.config.logging.console_level.upper()))
console_handler.setFormatter(FORMATTER)

# Logging to log file
file_handler = logging.FileHandler(LOG_FILE)
file_handler.setLevel(level=os.environ.get("LOGLEVEL", pg.config.logging.file_level.upper()))
file_handler.setFormatter(FORMATTER)

# Create log handlers
class log:

    @staticmethod
    def get_logger(logger_name):
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

        logger.info('Loading up {}...'.format(logger_name))

        return logger

    @staticmethod
    def method(logger):
        '''Decorator to log all parameters pass through a given function'''
        def inner_function(func):
            @wraps(func)
            def log_method(*args, **kwargs):
                logger.debug('Running {} with arguments {} {}'.format(func.__name__, args, kwargs))
                return func(*args, **kwargs)
            return log_method
        return inner_function


#################
# Setup logging #
#################
filename = os.path.basename(__file__).split('.')[0]
logger = log.get_logger(filename)
logger.debug('[config] {}'.format(pg.config))


################
# Setup pygame #
################
pg.createPath('./appdata/')
pygame.init()
window = windowScreen()
screens = Screens()