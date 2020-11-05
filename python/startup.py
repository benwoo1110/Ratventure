######################################
# Import and initialize the librarys #
######################################
import os
import time
import pkg_resources


##################
# Setup Settings #
##################
start = time.perf_counter()

# Disable pygame message
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

# Set program path to current file so code import works
myPath = os.path.dirname(os.path.abspath(__file__))
os.chdir(myPath)


##########################
# Check for dependencies #
##########################
with open('requirements.txt', 'r') as requirements:
    # Getting dependencies list needed
    dependencies = requirements.read().split('\n')

    for dependency in dependencies:
        # Check if dependencies meets the requirements
        try: pkg_resources.require(dependency)

        # If dependencies out of date
        except pkg_resources.VersionConflict:
            print('Dependency {} outdated. Attempting to update now...'.format(dependency))
            os.system('pip3 install --no-cache-dir {}'.format(dependency))

        # If dependencies is not found/installed.
        except pkg_resources.DistributionNotFound:
            print('Dependency {} not found. Attempting to install now...'.format(dependency))
            os.system('pip3 install --no-cache-dir {}'.format(dependency))


#############
# Load code #
#############
from code.api.core import log, screens
from code.screens import *


#################
# Setup logging #
#################
filename = os.path.basename(__file__).split('.')[0]
logger = log.get_logger(filename)


##############
# Start Game #
##############
end = time.perf_counter()
logger.info('Program started in {:.3f} seconds!'.format(end-start))
screens.mainloop(startScreen='mainmenu')