######################################
# Import and initialize the librarys #
######################################
from code.api.core import os, log, screens, pg
from code.logic.attack import attack
from code.logic.power import power
from code.logic.rest import rest


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
        attack.enemies['run_chance'] = current_mode['run']
        attack.enemies['appear_chance'] = current_mode['enemy']
        attack.enemies['multiplier'] = current_mode['multiplier']

        for enemy, chance in current_mode['enemy_chance'].items():
            attack.enemies[enemy]['chance'] = chance

        # Settings for orb
        power.orb_change = current_mode['orb_change']

        # Settings for rest
        rest.maxGain = current_mode['rest_gain']

    @staticmethod
    def get(mode:str = None) -> dict:
        # Gets the difficulty settings
        if mode == None: return difficulty.modes[screens.new_game.options.difficulty.mode.text]
        else: return difficulty.modes[mode]
    
    @staticmethod
    def update(index:int):
        difficulty_item = screens.new_game.options.difficulty
       
        # Get name of mode
        all_modes = list(difficulty.modes.keys())
        difficulty_item.index = (difficulty_item.index + index) % len(all_modes)

        # Set mode text
        difficulty_item.mode.setText(all_modes[difficulty_item.index])
        
        # Set the difficulty settings
        difficulty.set()