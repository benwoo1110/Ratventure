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
    maxGain = 2

    @staticmethod
    def initSurface():
        # Unload current selection
        screens.game.in_town.unload()

        # Set health that will be added
        current_health, max_health = stats.health.get('info')
        add_health = max_health - current_health

        # Amount regain based on maxGain
        if rest.maxGain >= 0: add_health = min(rest.maxGain, add_health)
        
        # Update health gained when rest on display
        stats.health.setBonus('rest', add_health, False)

        # Load the rest surface
        screens.game.rest.display(withItems=['stats'], refresh=True)
    
    @staticmethod
    def Rest():
        # Get health amount set to gain
        health_to_regain = stats.health.getBonus('rest')
        stats.health.update('info', health_to_regain)

        # Next day
        stats.day.update()

        # Go back to selection menu
        rest.back()
    
    @staticmethod
    def back():
        # Unload rest surface
        screens.game.rest.unload()
        
        # Display back town surface
        screens.game.in_town.display()