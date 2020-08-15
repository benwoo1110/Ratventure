######################################
# Import and initialize the librarys #
######################################
from code.api.core import os, log, pygame, pg
from code.api.objects import screen, Frame
from code.api.actions import Runclass, Switchscreen, Info, Alert
from code.api.data.Sound import Sound


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
    def init():
        # Play game background music
        if not Sound.background.isPlaying():
            pygame.mixer.fadeout(600)
            Sound.background.play(loops=-1, withVolume=pg.config.sound.background, fadetime=3000)
    
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
                'frame': Frame(x=878, y=266, w=652, h=134),
                'imageData': {'frame': Frame(x=878, y=266, w=652, h=134)},
                'action': Switchscreen(type='load', screen='new_game')
            },
            'load_saved': {
                'type': 'button',
                'frame': Frame(x=878, y=469, w=652, h=134),
                'imageData': {'frame': Frame(x=878, y=469, w=652, h=134)},
                'action': Switchscreen(type='load', screen='saves')
            },
            'leaderboard': { 
                'type': 'button',
                'frame': Frame(x=878, y=672, w=652, h=134),
                'imageData': {'frame': Frame(x=878, y=672, w=652, h=134)},
                'action': Switchscreen(type='load', screen='leaderboard')
            },
            'credits': { 
                'type': 'button',
                'frame': Frame(x=878, y=875, w=652, h=134),
                'imageData': {'frame': Frame(x=878, y=875, w=652, h=134)},
                'action': Switchscreen(type='load', screen='credit')
            },
            'quit': {
                'type': 'button',
                'frame': Frame(x=1705, y=986, w=84, h=84),
                'imageData': {'frame': Frame(x=1690, y=975, w=110, h=105)},
                'action': Alert (
                    type='confirm', 
                    title='Quit Game',
                    content='Are you sure you want to quit?',
                    yes=Info(text='quit')
                ),
            },
        }
    }
)