######################################
# Import and initialize the librarys #
######################################
from code.api.core import os, log, screens
from code.logic.stats import stats


#################
# Setup logging #
#################
filename = os.path.basename(__file__).split('.')[0]
logger = log.get_logger(filename)
logger.info('Loading up {}...'.format(filename))


##################
# Gameplay logic #
##################
class rest:

    @staticmethod
    def initSurface():
        # Unload current selection
        screens.game.in_town.unload()

        # Set health that will be added
        current_health, max_health = stats.health.get('info', 'stats')
        add_health = max_health - current_health
        stats.health.setBonus('rest', 'stats', add_health, False)

        # Load the rest surface
        screens.game.rest.display(withLoad=True)
    
    @staticmethod
    def Rest():
        # Set health back to max
        _, max_health = stats.health.get('info', 'stats')
        stats.health.set('info', 'stats', max_health, max_health)

        # Next day
        stats.day.update()

        # Go back to selection menu
        rest.back()
    
    @staticmethod
    def back():
        # Unload rest surface
        screens.game.rest.unload()

        # Displau back town surface
        screens.game.in_town.display()