######################################
# Import and initialize the librarys #
######################################
from code.api.core import os, log, pg, pygame
from code.api.objects import screen, Frame
from code.api.events import event, runclass


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
class mainmenu:

    @staticmethod
    def init():
        mainmenu_screen.display()
    
    @staticmethod
    def run():
        # Get action
        event_result = event(mainmenu_screen).get()

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
                'action': runclass(action='info')
            },
            'load_saved': {
                'type': 'button',
                'frame': Frame(x=983, y=459, w=529, h=140),
                'imageData': {'frame': Frame(x=983, y=459, w=529, h=140)},
                'action': runclass(action='info')
            },
            'leaderboard':{ 
                'type': 'button',
                'frame': Frame(x=983, y=665, w=529, h=140),
                'imageData': {'frame': Frame(x=983, y=665, w=529, h=140)},
                'action': runclass(action='info')
            },
            'quit': {
                'type': 'button',
                'frame': Frame(x=983, y=870, w=529, h=140),
                'imageData': {'frame': Frame(x=983, y=870, w=529, h=140)},
                'action': runclass(action='info')
            },
        }
    }
)


'''
                'data': {
                    'testing': text(
                        frame = Frame(x=983, y=665, w=529, h=140),
                        text = 'Very cool',
                        format = textFormat (
                            fontSize = 56,
                            align = 'left',
                            pos = 'center',
                            warpText = 19,
                            lineSpacing=0.7
                        )
                    )
                },
''' 
