######################################
# Import and initialize the librarys #
######################################
from code.api.core import os, log, PgEss, screens
from code.api.objects import Screen, Frame
from code.api.actions import Runclass, Switchscreen, Info
from code.api.events import gameEvent
from code.api.data.Text import Text, TextFormat


#################
# Setup logging #
#################
filename = os.path.basename(__file__).split('.')[0]
logger = log.get_logger(filename)


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

        # Go back if clicked
        if event_result.contains('name', ['dismiss', 'no', 'yes', 'ok']):
            screens.changeStack(type='back')

        # Quit program
        if event_result.contains('outcome', 'quit'): return 'quit'


##################
# Screen objects #
##################
alert_screen = Screen (
    name = 'alert',
    main = alert,
    bg_colour = (0, 0, 0, 100),
    seperateBackground = True,
    alpha = True,
    firstLoad = [],

    keyboard = {
        'dismiss': {
            'keys': [27],
            'action': Info(text='dismissed')
        }
    },

    surfaces = {
        'back': {
            'frame': Frame(x=0, y=0, w=1800, h=1080),
            'alpha': True,
            'dismiss': {
                'type': 'object',
                'frame': Frame(x=0, y=0, w=1800, h=1080),
                'action': Info(text='dismissed'),
                'clickSound': None
            },
        },

        'confirm': {
            'frame': Frame(x=495, y=256, w=811, h=573),
            'alpha': True,
            'message': {
                'type': 'text',
                'frame': Frame(x=57, y=33, w=696, h=465),
                'imageData': {'frame': Frame(x=57, y=33, w=696, h=465)},
                'clickSound': None,
                'data': {
                    'title': Text (
                        frame = Frame(x=57, y=48, w=697, h=95),
                        text = 'Title Here',
                        format = TextFormat(fontSize=88, align='center', pos='center', colour=PgEss.colour.black)
                    ),
                    'content': Text (
                        frame = Frame(x=57, y=156, w=697, h=183),
                        text = 'Content of message here.',
                        format = TextFormat(fontSize=68, align='center', pos='center', warpText=24, lineSpacing=0.8, colour=PgEss.colour.black)
                    ),
                },
            },
            'no': {
                'type': 'button',
                'frame': Frame(x=92, y=371, w=285, h=95),
                'imageData': {'frame': Frame(x=92, y=371, w=285, h=95)},
                'action': Info(text='no')
            },
            'yes': {
                'type': 'button',
                'frame': Frame(x=433, y=371, w=285, h=95),
                'imageData': {'frame': Frame(x=433, y=371, w=285, h=95)},
                'action': Info(text='yes')
            },
        },

        'notify': {
            'frame': Frame(x=495, y=256, w=811, h=573),
            'alpha': True,
            'message': {
                'type': 'text',
                'frame': Frame(x=57, y=33, w=696, h=465),
                'imageData': {'frame': Frame(x=57, y=33, w=696, h=465)},
                'clickSound': None,
                'data': {
                    'title': Text (
                        frame = Frame(x=57, y=48, w=697, h=95),
                        text = 'Title Here',
                        format = TextFormat(fontSize=88, align='center', pos='center', colour=PgEss.colour.black)
                    ),
                    'content': Text (
                        frame = Frame(x=57, y=156, w=697, h=183),
                        text = 'Content of message here.',
                        format = TextFormat(fontSize=68, align='center', pos='center', warpText=24, lineSpacing=0.8, colour=PgEss.colour.black)
                    ),
                },
            },
            'ok': {
                'type': 'button',
                'frame': Frame(x=224, y=384, w=362, h=85),
                'imageData': {'frame': Frame(x=224, y=384, w=362, h=85)},
                'action': Info(text='no')
            },
        }
    }
)
