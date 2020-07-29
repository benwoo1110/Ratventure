######################################
# Import and initialize the librarys #
######################################
from code.api.core import os, log, pg, coreFunc, traceback, screens


#################
# Setup logging #
#################
filename = os.path.basename(__file__).split('.')[0]
logger = log.get_logger(filename)
logger.info('Loading up {}...'.format(filename))


# Ensure that saves folder is created
if not os.path.isdir('./appdata/saves'):
    # Create logs directory
    try: os.mkdir('./appdata/saves')
    except: traceback.print_stack()
    else: print("Created ./appdata/saves directory")


class playerData(coreFunc):
    
    @staticmethod
    def new():
        pass

    @staticmethod
    def load():
        pass
        # Map

        # Stats

    @staticmethod
    def save():
        pass
        # Map

        # Stats