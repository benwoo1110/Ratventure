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
from code.config import Config


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
class PgEss:
    config = Config.get()
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
    def updateWindow():
        '''Displays screens/surfaces to pygame window'''
        pygame.display.update()
        PgEss.clock.tick(PgEss.config.framerate)

    @staticmethod
    def quit():
        '''Exit pygame program'''
        logger.info('Exiting program... Goodbye!')
        pygame.quit()


###########
# File IO #
###########
class File(coreFunc):
    def __init__(self, fileName):
        self.fileName = fileName

    def createPath(self) -> bool:
        if os.path.isdir(self.fileName): return False
        try:
            os.mkdir(self.fileName)
        except FileExistsError:
            logger.info(f"Folder '{self.fileName}' already exist!")
        except Exception as e:
            logger.error(e, exc_info=True)
            return False
        return True

    def writeJson(self, data) -> bool:
        try:
            with open(self.fileName, 'w') as datafile:
                json.dump(data, datafile)
        except Exception as e:
            logger.error(e, exc_info=True)
            return False
        return True

    def readJson(self, default = None) -> dict:
        data = None
        try:
            with open(self.fileName, 'r') as datafile:
                data = json.load(datafile)
        except FileNotFoundError as _:
            if default != None:
                self.writeJson(default)
                data = default
            else:
                logger.error(f"File '{self.fileName}' is not found!")
        except Exception as e:
            logger.error(e, exc_info=True)
        return data


##########
# Window #
##########
class windowScreen(coreFunc):
    def __init__(self):
        # Set icon
        try: pygame.display.set_icon(pygame.image.load(PgEss.config.icon_file))
        except FileNotFoundError: logger.error('No app icon image found at {}'.format(PgEss.config.icon_file))
        except Exception: logger.error('Error loading app icon image {}!'.format(PgEss.config.icon_file), exc_info=True)

        # Set title
        try: pygame.display.set_caption(PgEss.config.title)
        except Exception: logger.error('Unable set display caption!', exc_info=True)

        # Set default screen size
        self.width = 1800
        self.height = 1080

        # Set display
        # Full screen mode
        if PgEss.config.fullscreen: 
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
            self.scale = PgEss.config.scale
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
            PgEss.tick(PgEss.config.framerate)

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
                    PgEss.quit()
                    return

            # When screen ends
            if hasattr(screen.main, 'end'): screen.main.end()
            self.stackChange = False


###########
# Logging #
###########
File('./logs/').createPath()

# Keep only certain number of log files 
log_files = glob.glob("./logs/*.log")
log_files.sort(key=os.path.getmtime)

for index in range(len(log_files) - max(0, PgEss.config.logging.keep_logs-1)):
    os.remove(log_files[index])

# Setup log format and location
FORMATTER = logging.Formatter('[%(asctime)s %(levelname)s] [%(name)s] %(message)s', datefmt='%H:%M:%S')
LOG_FILE = datetime.now().strftime("./logs/%d-%m-%Y_%H-%M-%S.log")

# Console logging
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(level=os.environ.get("LOGLEVEL", PgEss.config.logging.console_level.upper()))
console_handler.setFormatter(FORMATTER)

# Logging to log file
file_handler = logging.FileHandler(LOG_FILE)
file_handler.setLevel(level=os.environ.get("LOGLEVEL", PgEss.config.logging.file_level.upper()))
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
logger.debug('[config] {}'.format(PgEss.config))


################
# Setup pygame #
################
File('./appdata/').createPath()
pygame.init()
window = windowScreen()
screens = Screens()