######################################
# Import and initialize the librarys #
######################################
from code.api.core import os, log, screens
from code.logic.stats import Bonus
from code.logic.player import player


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
    stats = Bonus(health=0)

    @staticmethod
    def initSurface():
        # Unload current selection
        screens.game.in_town.unload()

        # Set health that will be added
        current_health, max_health = player.stats.health
        add_health = max_health - current_health
        if rest.maxGain >= 0: add_health = min(rest.maxGain, add_health)       
        
        # Update health gained when rest on display
        rest.stats.set('health', [add_health, 0], screens.game.rest.stats)

        # Load the rest surface
        screens.game.rest.display(withItems=['stats'], refresh=True)
    
    @staticmethod
    def Rest():
        # Get health amount set to gain
        player.stats.addBonus(rest.stats, screens.game.info.stats, True)

        # Next day
        player.next_day()

        # Go back to selection menu
        rest.back()
    
    @staticmethod
    def back():
        # Unload rest surface
        screens.game.rest.unload()
        
        # Display back town surface
        screens.game.in_town.display()