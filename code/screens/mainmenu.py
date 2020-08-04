######################################
# Import and initialize the librarys #
######################################
from code.api.core import os, log, pg, screens
from code.api.objects import screen, Frame
from code.api.actions import Runclass, Switchscreen, Info
from code.api.data.Text import Text, textFormat
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
class mainmenu:
    
    @staticmethod
    def run():
        # Get action
        event_result = mainmenu_screen.events.get()

        # No action
        if event_result == None: return
        # Quit program
        if event_result.contains('outcome', 'quit'): return 'quit'


##################
# Screen objects #
##################
mainmenu_screen = screen (
    name = 'mainmenu',
    main = mainmenu,
    surfaces = {
        'menu': {
            'frame': Frame(x=0, y=0, w=1800, h=1080),
            'new_game': {
                'type': 'button',
                'frame': Frame(x=983, y=253, w=529, h=140),
                'imageData': {'frame': Frame(x=983, y=253, w=529, h=140)},
                'action': Switchscreen(type='load', screen='new_game')
            },
            'load_saved': {
                'type': 'button',
                'frame': Frame(x=983, y=459, w=529, h=140),
                'imageData': {'frame': Frame(x=983, y=459, w=529, h=140)},
                'action': Switchscreen(type='load', screen='saves') # Runclass(run=mainmenu.loadSave) 
            },
            'leaderboard':{ 
                'type': 'button',
                'frame': Frame(x=983, y=665, w=529, h=140),
                'imageData': {'frame': Frame(x=983, y=665, w=529, h=140)},
                'action': Switchscreen(type='load', screen='leaderboard')
            },
            'quit': {
                'type': 'button',
                'frame': Frame(x=983, y=870, w=529, h=140),
                'imageData': {'frame': Frame(x=983, y=870, w=529, h=140)},
                'action': Info(text='quit') # Switchscreen(type='load', screen='alert')
            },
        }
    }
)