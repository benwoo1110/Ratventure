######################################
# Import and initialize the librarys #
######################################
import webbrowser
from code.api.core import os, log
from code.api.objects import screen, Frame
from code.api.actions import Runclass, Info, Switchscreen


#################
# Setup logging #
#################
filename = os.path.basename(__file__).split('.')[0]
logger = log.get_logger(filename)
logger.info('Loading up {}...'.format(filename))


############################
# Screen main action class #
############################
class credit:
    
    @staticmethod
    def run():
        # Get action
        event_result = credits_screen.events.get()

        # No action
        if event_result == None: return
        # Quit program
        if event_result.contains('outcome', 'quit'): return 'quit'


##################
# Screen objects #
##################
credits_screen = screen (
    name = 'credit',
    main = credit,
    surfaces = {
        'page': {
            'frame': Frame(x=0, y=0, w=1800, h=1080),
            'back': {
                'type': 'button',
                'frame': Frame(x=141, y=58, w=132, h=103),
                'imageData': {'frame': Frame(x=141, y=58, w=132, h=103)},
                'action': Switchscreen(type='back')
            },
            'github': {
                'type': 'button',
                'frame': Frame(x=421, y=797, w=650, h=123),
                'imageData': {'frame': Frame(x=0, y=710, w=1800, h=370)},
                'action': Runclass(run=webbrowser.open, parameters={'url': 'https://github.com/benwoo1110/Ratventure'})
            }
        }
    }
)