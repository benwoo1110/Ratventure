######################################
# Import and initialize the librarys #
######################################
from code.api.core import os, log, screens


#################
# Setup logging #
#################
filename = os.path.basename(__file__).split('.')[0]
logger = log.get_logger(filename)
logger.info('Loading up {}...'.format(filename))


class difficulty:
    modes = {
        'easy': {
            'run': 100,
            'enemy': 50,
            'multiplier': 1.0,
            'orb_change': -1,
            'rest_gain': -1,
            'town_number': 5,
            'town_space': 3,
        },
        'medium': {
            'run': 100,
            'enemy': 50,
            'multiplier': 1.0,
            'orb_change': -1,
            'rest_gain': -1,
            'town_number': 5,
            'town_space': 3,
        },
        'hard': {
            'run': 100,
            'enemy': 50,
            'multiplier': 1.0,
            'orb_change': -1,
            'rest_gain': -1,
            'town_number': 5,
            'town_space': 3,
        }
    }
    current = None

    @staticmethod
    def set(mode:str):
        pass

    def get() -> dict:
        pass
