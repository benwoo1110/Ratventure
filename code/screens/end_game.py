######################################
# Import and initialize the librarys #
######################################
import time
from code.api.core import os, log, pg, pygame
from code.api.objects import screen, Frame
from code.api.actions import Runclass, Switchscreen, Info
from code.api.data.Text import Text, textFormat
from code.api.data.Sound import Sound
from code.logic.player import player
from code.logic.playerData import playerData
from code.logic.playerRank import playerRank


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
    # Textfield variabels
    time_pressed, repeat_interval = 0, 1.2

    @staticmethod
    def textfield_selected():
        end_game_screen.win.leaderboard.switchState('Selected')

    @staticmethod
    def rankColour() -> int:
        # Set cool colour for top 3
        ranking = playerRank.getPos()
        if ranking <= 3: end_game_screen.win.leaderboard.switchState(str(ranking))
        else: end_game_screen.win.leaderboard.switchState('')
        return ranking

    @staticmethod
    def run():
        if end_game_screen.win.loaded:
            nickname = end_game_screen.win.leaderboard

            if not end_game_screen.win.leaderboard.isState('Selected'): end_game.rankColour()

            if end_game_screen.win.leaderboard.isState('Selected'):
                pressed_key = None

                # Get most recent pressed char
                for char in pg.keypressed:
                    if nickname.nickname.validateChar(char.key): pressed_key = char

                # Engage key
                if pressed_key != None and time.time() - end_game.time_pressed >= end_game.repeat_interval:

                    # remove character
                    if pressed_key.key == 8: 
                        nickname.nickname.setText(nickname.nickname.text[:-1])
                        
                    # Add character
                    else: nickname.nickname.setText(nickname.nickname.text + pressed_key.unicode)

                    # Setup for next key repeat
                    end_game.time_pressed = time.time()
                    if end_game.repeat_interval > 0.025: end_game.repeat_interval /= 2.6

        # Get action
        event_result = end_game_screen.events.get()

        # No action
        if event_result == None: return

        if end_game_screen.win.loaded:
            # Reset key interval when key is released
            if event_result.didAction('keyup'): 
                end_game.time_pressed, end_game.repeat_interval = 0, 1.2

            # Exit for editing textfield when enter is pressed OR Clicked on other UI elements
            if (event_result.didAction('keydown') and event_result.keydown.isName(13)) or (event_result.didAction('click') and not event_result.click.isName('leaderboard')):
                # Apply teh new name to leaderboard data
                end_game_screen.win.leaderboard.rankid = playerRank.rename(
                    end_game_screen.win.leaderboard.nickname.text,
                    end_game_screen.win.leaderboard.rankid
                    )
                # Revert back to deselected state
                end_game.rankColour()

        # Quit program
        if event_result.contains('outcome', 'quit'): return 'quit'


##################
# Screen objects #
##################
end_game_screen = screen (
    name = 'end_game',
    main = end_game,
    # firstLoad = ['win'],
    
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
            'background': {
                'type': 'object',
                'frame': Frame(x=0, y=0, w=1800, h=1080),
                'action': Info(text='Deselect'),
                'clickSound': None
            },
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
            'leaderboard': {
                'type': 'object',
                'frame': Frame(x=462, y=443, w=876, h=111),
                'imageData': {'frame': Frame(x=462, y=443, w=876, h=111)},
                'action': Runclass(run=end_game.textfield_selected),
                'data': {
                    'rankid': '',
                    'postion': Text (
                        editable = False,
                        frame = Frame(x=465, y=443, w=105, h=111),
                        text = '1',
                        format = textFormat(fontSize=68, align='center', pos='center', colour=pg.colour.white)
                    ),
                    'nickname': Text (
                        frame = Frame(x=573, y=443, w=497, h=111),
                        text = 'Demo',
                        format = textFormat(fontSize=68, align='left', pos='center', colour=pg.colour.white)
                    ),
                    'days': Text (
                        editable = False,
                        frame = Frame(x=1073, y=443, w=236, h=111),
                        text = '100',
                        suffix = ' days',
                        format = textFormat(fontSize=68, align='right', pos='center', colour=pg.colour.white)
                    ),
                }
            }
        }
    }
)