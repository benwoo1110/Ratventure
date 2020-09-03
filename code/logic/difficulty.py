######################################
# Import and initialize the librarys #
######################################
from code.api.core import os, log, screens, PgEss
from code.logic.attack import Enemy
from code.logic.orb import Orb
from code.logic.rest import rest
from code.logic.player import Player


#################
# Setup logging #
#################
filename = os.path.basename(__file__).split('.')[0]
logger = log.get_logger(filename)


class Difficulty:
    modes = PgEss.loadJson('./gamefiles/difficulty.json')

    @staticmethod
    def set(mode:str = None):
        # Get current difficulty
        current_mode = Difficulty.get(mode)

        # Settings for attack
        Enemy.enemies['run_chance'] = current_mode['run']
        Enemy.enemies['appear_chance'] = current_mode['enemy']
        Enemy.enemies['start_multiplier'] = current_mode['start_multiplier']
        Enemy.enemies['day_saturation'] = current_mode['day_saturation']

        for name, chance in current_mode['enemy_chance'].items():
            Enemy.enemies[name]['chance'] = chance

        # Settings for orb
        Orb.change = current_mode['orb_change']

        # Settings for rest
        rest.maxGain = current_mode['rest_gain']

    @staticmethod
    def get(mode = None) -> dict:
        # Gets the difficulty settings
        if mode == None: return Difficulty.modes[Player.difficulty]
        if type(mode) == int: return Difficulty.modes[Difficulty.getName(mode)]
        else: return Difficulty.modes[mode]

    @staticmethod
    def getName(index:int) -> str:
        # Gets the difficulty name
        return list(Difficulty.modes.keys())[index]
    
    @staticmethod
    def updateName(index:int):
        difficulty_item = screens.new_game.options.difficulty
       
        # Get name of mode
        difficulty_item.index = (difficulty_item.index + index) % len(Difficulty.modes)
        # Set mode text
        difficulty_item.mode.setText(Difficulty.getName(difficulty_item.index))

    @staticmethod
    def setName(index:int):
        difficulty_item = screens.new_game.options.difficulty

        # Get name of mode
        difficulty_item.index = index
        # Set mode text
        difficulty_item.mode.setText(Difficulty.getName(index))
