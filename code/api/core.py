######################################
# Import and initialize the librarys #
######################################
import os
import logging
import sys
import glob
import traceback
import pygame
from datetime import datetime
from code.config import config


#####################
# Core parent class #
#####################
class coreFunc:
    def __setitem__(self, name, value): self.__dict__[name] = value
    def __setattr__(self, name, value): self.__dict__[name] = value
    def __getitem__(self, name): return self.__dict__[name]
    def __repr__(self): return '{}'.format(self.__dict__)


###################
# Common function #
###################
class pg:
    config = config.get()
    keypressed = []
    clock = pygame.time.Clock()

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
        pygame.display.update()
        pg.clock.tick(pg.config.framerate)

    @staticmethod
    def quit():
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
            logger.warn('Error loading app icon image "{}"'.format(pg.config.icon_file))

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
    
    def add(self, name, screen):
        self.__dict__[name] = screen
        self.containerList.append(name)
        logger.debug('Added screen {}'.format(name))

    def changeStack(self, type:str, screen:str = None):
        # Skip if another changeStack() is happening
        if self.stackChange: 
            logger.warn('Another stack change is happening, skipping type:{} screen:{}'.format(type, screen))
            return
        
        self.stackChange = True

        # Go back to previous screen
        if str(type) == 'back':
            # Go back one screen
            if screen == None: self.screensStack.pop()
            # Go back to screen specified
            elif screen in self.containerList: 
                self.screensStack = self.screensStack[:self.screensStack.index(screen)+1]
            # Error
            else: logger.error('"{}" is not a screen.'.format(screen))
        
        # Load a new screen
        elif type == 'load':  
            if screen in self.containerList: self.screensStack.append(screen)
            # Error
            else: logger.error('"{}" is not a screen.'.format(screen))

        # Error
        else: logger.error('{} type not recognised.'.format(type))

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
            screen.display()

            # Log current screen stacks
            logger.debug('New screen stack of {}'.format(self.screensStack))
            
            # Main loop for top screen
            while not self.stackChange:
                screen_result = screen.main.run()

                if screen_result == 'quit':
                    return

            # When screen ends
            if hasattr(screen.main, 'end'): screen.main.end()
            self.stackChange = False


###########
# Logging #
###########
# Ensure that logs folder is created
filepath = './logs/'
if not os.path.isdir(filepath):
    # Create logs directory
    try: os.mkdir(filepath)
    except Exception as e: logger.error(e, exc_info=True)
    else: print('Created {} directory'.format(filepath))


# Keep only certain number of log files 
log_files = glob.glob("./logs/*.log")

for index in range(len(log_files) - max(0, pg.config.logging.keep_logs-1)):
    os.remove(log_files[index])

# setup log format and location
FORMATTER = logging.Formatter('[%(asctime)s %(levelname)s] [%(name)s] %(message)s', datefmt='%H:%M:%S')
LOG_FILE = datetime.now().strftime("./logs/%d-%m-%Y_%H-%M-%S.log")

class log:
    @staticmethod
    def get_console_handler():
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level=os.environ.get("LOGLEVEL", pg.config.logging.console_level.upper()))
        console_handler.setFormatter(FORMATTER)
        return console_handler

    @staticmethod
    def get_file_handler():
        file_handler = logging.FileHandler(LOG_FILE)
        file_handler.setLevel(level=os.environ.get("LOGLEVEL", pg.config.logging.file_level.upper()))
        file_handler.setFormatter(FORMATTER)
        return file_handler

    @staticmethod
    def get_logger(logger_name):
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(log.get_console_handler())
        logger.addHandler(log.get_file_handler())
        return logger


#################
# Setup logging #
#################
filename = os.path.basename(__file__).split('.')[0]
logger = log.get_logger(filename)
logger.info('Loading up {}...'.format(filename))
logger.debug('[config] {}'.format(pg.config))


# Ensure that appdata folder is created
filepath = './appdata/'
if not os.path.isdir(filepath):
    # Create logs directory
    try: os.mkdir(filepath)
    except Exception as e: logger.error(e, exc_info=True)
    else: logger.info('Created {} directory'.format(filepath))


################
# Setup pygame #
################
pygame.init()
window = windowScreen()
screens = Screens()