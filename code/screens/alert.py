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
class alert:

    @staticmethod
    def run():
        # Get action
        event_result = alert_screen.events.get()

        # No action
        if event_result == None: return
        # Quit program
        if event_result.contains('outcome', 'quit'): return 'quit'


##################
# Screen objects #
##################
alert_screen = screen (
    name = 'alert',
    main = alert,
    bg_colour = (0, 0, 0, 100),

    keyboard = {
        'back': {
            'keys': [27],
            'action': Switchscreen(type='back')
        }
    },

    surfaces = {
        'confirm': {
            'frame': Frame(x=495, y=253, w=811, h=573),
            'message': {
                'type': 'text',
                'frame': Frame(x=57, y=70, w=696, h=428),
                'imageData': {'frame': Frame(x=57, y=70, w=696, h=428)},
                'selectable': False,
                'data': {
                    'text': Text (
                        frame = Frame(x=57, y=70, w=697, h=250),
                        text = 'Are you sure you want to quit the game?',
                        format = textFormat(fontSize=88, align='center', pos='center', warpText=18, lineSpacing=0.8, colour=pg.colour.black)
                    ),
                },
            },
            'no': {
                'type': 'button',
                'frame': Frame(x=92, y=371, w=285, h=95),
                'imageData': {'frame': Frame(x=92, y=371, w=285, h=95)},
                'action': Info(text='difficulty')
            },
            'yes': {
                'type': 'button',
                'frame': Frame(x=433, y=371, w=285, h=95),
                'imageData': {'frame': Frame(x=433, y=371, w=285, h=95)},
                'action': Info(text='difficulty')
            },
        }
    }
)
