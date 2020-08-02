######################################
# Import and initialize the librarys #
######################################
import time
from code.api.core import os, log, pg, screens
from code.api.objects import screen, Frame
from code.api.actions import Runclass, Switchscreen, Info
from code.logic.playerData import playerData


#################
# Setup logging #
#################
filename = os.path.basename(__file__).split('.')[0]
logger = log.get_logger(filename)
logger.info('Loading up {}...'.format(filename))


############################
# Screen main action class #
############################
class end_game:
    
    @staticmethod
    def run():
        # Get action
        event_result = end_game_screen.events.get()

        # No action
        if event_result == None: return
        # Quit program
        if event_result.contains('outcome', 'quit'): return 'quit'


##################
# Screen objects #
##################
end_game_screen = screen (
    name = 'end_game',
    main = end_game,
    surfaces = {
        'gameover': {
            'frame': Frame(x=0, y=0, w=1800, h=1080),
            'try_again': {
                'type': 'button',
                'frame': Frame(x=347, y=708, w=507, h=140),
                'imageData': {'frame': Frame(x=347, y=708, w=507, h=140)},
                'action': Runclass(run=playerData.new)
            },
            'mainmenu': {
                'type': 'button',
                'frame': Frame(x=946, y=708, w=507, h=140),
                'imageData': {'frame': Frame(x=946, y=708, w=507, h=140)},
                'action': Switchscreen(type='back', screen='mainmenu')
            },
        },
        'win': {
            'frame': Frame(x=0, y=0, w=1800, h=1080),
            'new_game': {
                'type': 'button',
                'frame': Frame(x=347, y=708, w=507, h=140),
                'imageData': {'frame': Frame(x=347, y=708, w=507, h=140)},
                'action': Switchscreen(type='load', screen='new_game')
            },
            'mainmenu': {
                'type': 'button',
                'frame': Frame(x=946, y=708, w=507, h=140),
                'imageData': {'frame': Frame(x=946, y=708, w=507, h=140)},
                'action': Switchscreen(type='back', screen='mainmenu')
            },
        }
    }
)