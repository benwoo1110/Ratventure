######################################
# Import and initialize the librarys #
######################################
from code.api.core import os, log, screens
from code.api.data.Sound import Sound
from code.logic.stats import Bonus
from code.logic.player import player
from code.logic.story import story


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
        rest.stats.set('health', [add_health, 0], screens.game.rest.stats, index=0)

        # Load the rest surface
        screens.game.rest.display(withItems=['stats'], refresh=True)
    
    @staticmethod
    def Rest():
        # Get health amount set to gain
        player.stats.addBonus(rest.stats, screens.game.info.stats, True, screens.game.info.hero)

        # Heal sound
        Sound.heal.play(maxtime=1000, fadetime=100, withVolume=0.8)

        # Next day
        player.next_day()

        # Cool story
        if player.stats.isFullHealth(): story.rest_ful.display()
        else: story.rest_some.display(rest.stats.health[0])

        # Go back to selection menu
        rest.back()
    
    @staticmethod
    def back():
        # Unload rest surface
        screens.game.rest.unload()
        
        # Display back town surface
        screens.game.in_town.display()