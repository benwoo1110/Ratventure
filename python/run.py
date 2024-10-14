######################################
# Import and initialize the librarys #
######################################
import os

##################
# Setup Settings #
##################
# Disable pygame message
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"


#############
# Load code #
#############
from code.api.core import log, screens
from code.screens import (
    alert, credit, end_game, game, leaderboard, mainmenu, new_game, saves, shop
) # Workaround for pyinstaller


#################
# Setup logging #
#################
filename = os.path.basename(__file__).split('.')[0]
logger = log.get_logger(filename)


##############
# Start Game #
##############
screens.mainloop(startScreen='mainmenu')
