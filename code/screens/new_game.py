######################################
# Import and initialize the librarys #
######################################
import time
from code.api.core import os, log, pg
from code.api.objects import screen, Frame
from code.api.actions import Runclass, Switchscreen, Info
from code.api.data.Text import Text, textFormat, textValidate
from code.logic.playerData import playerData
from code.logic.difficulty import difficulty


#################
# Setup logging #
#################
filename = os.path.basename(__file__).split('.')[0]
logger = log.get_logger(filename)
logger.info('Loading up {}...'.format(filename))


############################
# Screen main action class #
############################
class new_game:
    # Textfield variabels
    time_pressed, repeat_interval = 0, 1.2

    @staticmethod
    def init():
        new_game_screen.options.nickname.switchState('', False)
        new_game_screen.options.nickname.text.setText('Player')

        difficulty.setName(0)

    @staticmethod
    def textfield_selected():
        new_game_screen.options.nickname.switchState('Selected')
    
    @staticmethod
    def run():
        nickname = new_game_screen.options.nickname

        if new_game_screen.options.nickname.isState('Selected'):
            pressed_key = None

            # Get most recent pressed char
            for char in pg.keypressed:
                if nickname.text.validateChar(char.key): pressed_key = char

            # Engage key
            if pressed_key != None and time.time() - new_game.time_pressed >= new_game.repeat_interval:

                # remove character
                if pressed_key.key == 8: 
                    nickname.text.setText(nickname.text.text[:-1])
                    
                # Add character
                else: nickname.text.setText(nickname.text.text + pressed_key.unicode)

                # Setup for next key repeat
                new_game.time_pressed = time.time()
                if new_game.repeat_interval > 0.025: new_game.repeat_interval /= 2.6

        # Get action
        event_result = new_game_screen.events.get()

        # No action
        if event_result == None: return

        # Reset key interval when key is released
        if event_result.didAction('keyup'): 
            new_game.time_pressed, new_game.repeat_interval = 0, 1.2

        # Exit for editing textfield when enter/esc is pressed
        if event_result.didAction('keydown') and event_result.keydown.isName(13):
             nickname.switchState('')

        # Clicked on other UI elements
        if event_result.didAction('click') and not event_result.click.isName('nickname'):
            nickname.switchState('')

        # Quit program
        if event_result.contains('outcome', 'quit'): return 'quit'


##################
# Screen objects #
##################
new_game_screen = screen (
    name = 'new_game',
    main = new_game,

    keyboard = {
        'back': {
            'keys': [27],
            'action': Switchscreen(type='back', screen='mainmenu')
        }
    },

    surfaces = {
        'options': {
            'frame': Frame(x=0, y=0, w=1800, h=1080),
            'background': {
                'type': 'object',
                'frame': Frame(x=0, y=0, w=1800, h=1080),
                'action': Info(text='Deselect')
            },
            'nickname': {
                'type': 'textfield',
                'frame': Frame(x=747, y=341, w=925, h=140),
                'imageData': {'frame': Frame(x=747, y=341, w=925, h=140)},
                'action': Runclass(run=new_game.textfield_selected),
                'data': {
                    'text': Text (
                        frame = Frame(x=747, y=341, w=925, h=140),
                        text = 'Benedict',
                        format = textFormat(fontSize=116, align='center', pos='center', colour=pg.colour.white),
                        validation = textValidate(regex='[\w\s]{1,16}', invalidPrompt='Player nickname should be between 1 and 16 character\'s long.')
                    ),
                },
            },
            'difficulty': {
                'type': 'text',
                'frame': Frame(x=1008, y=636, w=405, h=140),
                'imageData': {'frame': Frame(x=1008, y=636, w=405, h=140)},
                'selectable': False,
                'data': {
                    'index': 0,
                    'mode': Text (
                        frame = Frame(x=1008, y=636, w=405, h=140),
                        text = 'Easy',
                        format = textFormat(fontSize=116, align='center', pos='center', colour=pg.colour.white)
                    ),
                },
            },
            'back': {
                'type': 'button',
                'frame': Frame(x=747, y=875, w=271, h=140),
                'imageData': {'frame': Frame(x=747, y=875, w=271, h=140)},
                'action': Switchscreen(type='back', screen='mainmenu')
            },
            'play': {
                'type': 'button',
                'frame': Frame(x=1143, y=875, w=530, h=140),
                'imageData': {'frame': Frame(x=1143, y=875, w=530, h=140)},
                'action': Runclass(run=playerData.new)
            },
            'difficulty_back': {
                'type': 'button',
                'frame': Frame(x=916, y=660, w=92, h=92),
                'imageData': {'frame': Frame(x=747, y=636, w=260, h=92)},
                'action': Runclass(run=difficulty.updateName, parameters={'index': -1})
            },
            'difficulty_next': {
                'type': 'button',
                'frame': Frame(x=1412, y=660, w=92, h=92),
                'imageData': {'frame': Frame(x=1412, y=636, w=260, h=92)},
                'action': Runclass(run=difficulty.updateName, parameters={'index': 1})
            }
        },
    }
)