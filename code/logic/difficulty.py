######################################
# Import and initialize the librarys #
######################################
from code.api.core import os, log, screens, pg
from code.logic.attack import enemy
from code.logic.orb import orb
from code.logic.rest import rest
from code.logic.player import player


#################
# Setup logging #
#################
filename = os.path.basename(__file__).split('.')[0]
logger = log.get_logger(filename)
logger.info('Loading up {}...'.format(filename))


class difficulty:
    modes = pg.loadJson('./gamefiles/difficulty.json')

    @staticmethod
    def set(mode:str = None):
        # Get current difficulty
        current_mode = difficulty.get(mode)

        # Settings for attack
        enemy.enemies['run_chance'] = current_mode['run']
        enemy.enemies['appear_chance'] = current_mode['enemy']
        enemy.enemies['multiplier'] = current_mode['multiplier']

        for name, chance in current_mode['enemy_chance'].items():
            enemy.enemies[name]['chance'] = chance

        # Settings for orb
        orb.change = current_mode['orb_change']

        # Settings for rest
        rest.maxGain = current_mode['rest_gain']

    @staticmethod
    def get(mode:str = None) -> dict:
        # Gets the difficulty settings
        if mode == None: return difficulty.modes[player.difficulty]
        else: return difficulty.modes[mode]
    
    @staticmethod
    def update(index:int):
        difficulty_item = screens.new_game.options.difficulty
       
        # Get name of mode
        all_modes = list(difficulty.modes.keys())
        difficulty_item.index = (difficulty_item.index + index) % len(all_modes)

        # Set mode text
        difficulty_item.mode.setText(all_modes[difficulty_item.index])