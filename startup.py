######################################
# Import and initialize the librarys #
######################################
import os
import pkg_resources


########################
# Environment Settings #
########################
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"


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


###############
# Import code #
###############
from code.api.core import log, pg, screens
import code.screens.mainmenu
import code.screens.new_game


#################
# Setup logging #
#################
filename = os.path.basename(__file__).split('.')[0]
logger = log.get_logger(filename)
logger.info('Loading up {}...'.format(filename))
logger.debug('[config] {}'.format(pg.config))


##############
# Start Game #
##############
screens.mainloop(startScreen='new_game')

# End program
pg.quit()