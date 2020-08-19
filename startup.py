######################################
# Import and initialize the librarys #
######################################
import os
import pkg_resources


##################
# Setup Settings #
##################
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
from code.api.core import log, screens, pg
from code.api.data.Sound import Sound
from code.screens import *


#################
# Setup logging #
#################
filename = os.path.basename(__file__).split('.')[0]
logger = log.get_logger(filename)
logger.info('Loading up {}...'.format(filename))


##############
# Start Game #
##############
if __name__ == '__main__':
    logger.info('Program started!')
    Sound.background.play(loops=-1, withVolume=pg.config.sound.background, fadetime=500)
    screens.mainloop(startScreen='mainmenu')