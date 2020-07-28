######################################
# Import and initialize the librarys #
######################################
from code.api.core import os, log, pg
from code.api.objects import screen, Frame
from code.api.data.Text import text, textFormat
from code.api.events import event, Runclass, Switchscreen


#################
# Setup logging #
#################
filename = os.path.basename(__file__).split('.')[0]
logger = log.get_logger(filename)
logger.info('Loading up {}...'.format(filename))
logger.debug('[config] {}'.format(pg.config))


############################
# Screen main action class #
############################
class new_game:

    @staticmethod
    def init():
        new_game_screen.display()
    
    @staticmethod
    def run():
        # Get action
        event_result = event(new_game_screen).get()

        # No action
        if event_result == None: return
        # Quit program
        if event_result.contains('outcome', 'quit'): return 'quit'


##################
# Screen objects #
##################
new_game_screen = screen (
    name = 'new_game',
    main = new_game,
    surfaces = {
        'options': {
            'frame': Frame(x=0, y=0, w=1800, h=1080),
            'nickname': {
                'type': 'text',
                'frame': Frame(x=760, y=347, w=987, h=140),
                'imageData': {'frame': Frame(x=760, y=347, w=987, h=140)},
                #'action': Runclass(run='info')
            },
            'difficulty': {
                'type': 'text',
                'frame': Frame(x=760, y=642, w=987, h=140),
                'imageData': {'frame': Frame(x=760, y=642, w=987, h=140)},
                #'action': Runclass(run='info')
            },
            'back': {
                'type': 'button',
                'frame': Frame(x=760, y=881, w=271, h=140),
                'imageData': {'frame': Frame(x=760, y=881, w=271, h=140)},
                'action': Switchscreen(type='back')
            },
            'play': {
                'type': 'button',
                'frame': Frame(x=1188, y=881, w=559, h=140),
                'imageData': {'frame': Frame(x=1188, y=881, w=559, h=140)},
                'action': Runclass(run='info')
            },
        },
    }
)