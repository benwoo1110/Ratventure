######################################
# Import and initialize the librarys #
######################################
from code.api.core import os, log, pg, screens
from code.api.objects import screen, Frame
from code.api.actions import Runclass, Switchscreen, Info
from code.api.data.Text import Text, textFormat


#################
# Setup logging #
#################
filename = os.path.basename(__file__).split('.')[0]
logger = log.get_logger(filename)
logger.info('Loading up {}...'.format(filename))


############################
# Screen main action class #
############################
class leaderboard:

    @staticmethod
    def run():
        # Get action
        event_result = leaderboard_screen.events.get()

        # No action
        if event_result == None: return
        # Quit program
        if event_result.contains('outcome', 'quit'): return 'quit'


##################
# Screen objects #
##################
leaderboard_screen = screen (
    name = 'leaderboard',
    main = leaderboard,

    keyboard = {
        'back': {
            'keys': [27],
            'action': Switchscreen(type='back', screen='mainmenu')
        }
    },

    surfaces = {
        'board': {
            'frame': Frame(x=0, y=0, w=1800, h=1080),
            'back': {
                'type': 'button',
                'frame': Frame(x=141, y=58, w=132, h=103),
                'imageData': {'frame': Frame(x=141, y=58, w=132, h=103)},
                'action': Switchscreen(type='back')
            },
        },
    }
)