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
    config = config.Config
    width = int(1800)
    height = int(1080)
    scaled_width = int(width * config.scale)
    scaled_height = int(height * config.scale)
    keypressed = []
    clock = pygame.time.Clock()

    class font:
        '''fonts found in fonts folder'''
        knigqst = './fonts/Knigqst.ttc'

    class colour:
        '''Common colour types in RGB tuple format'''
        black = (0, 0, 0)
        white = (255, 255, 255)
        red = (181, 23, 0)
        blue = (0, 77, 128)
        green = (1, 113, 0)
        purple = (97, 0, 188)

    @staticmethod
    def size(): return (pg.width, pg.height)

    @staticmethod
    def scaled_size(): return (pg.scaled_width, pg.scaled_height)

    @staticmethod
    def updateDisplay():
        pygame.display.update()
        pg.clock.tick(pg.config.framerate)

    @staticmethod
    def quit():
        logger.info('Exiting program... Goodbye!')
        pygame.quit()


##########
# Screen #
##########
class screens(coreFunc):
    screenList = {}
    loaded = []
    
    def add(name, screen):
        screens.screenList[name] = screen
        logger.debug('Added screen {}'.format(name))


###########
# Logging #
###########
# Ensure that logs folder is created
if not os.path.isdir('./logs'):
    # Create logs directory
    try: os.mkdir('logs')
    except: traceback.print_stack()
    else: print("Created ./logs directory")

# Keep only certain number of log files 
log_files = glob.glob("./logs/*.log")

for index in range(len(log_files) - max(0, pg.config.logging.keep_logs-1)): #log_files[:min(-1, -config.logging.keep_logs)]:
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


################
# Setup pygame #
################
'''Startup pygame window'''
pygame.init()

# Set icon
if os.path.isfile(pg.config.icon_file): 
    pygame.display.set_icon(pygame.image.load(pg.config.icon_file))

elif pg.config.icon_file != '': 
    logger.warn('Error loading app icon image "{}"'.format(pg.config.icon_file))

# Set title
pygame.display.set_caption(pg.config.title)

# Set display
window = pygame.display.set_mode(pg.scaled_size())

logger.debug(pygame.display.Info())