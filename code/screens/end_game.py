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
    
    @staticmethod
    def init():
        # Remove save since game ended
        playerData.delete()

        # Stop game music
        # Play game background music
        if not Sound.background.isPlaying():
            pygame.mixer.fadeout(600)
            Sound.background.play(loops=-1, withVolume=0.12, fadetime=5000)

        # Check if win screen is the one loaded
        if end_game_screen.win.loaded:
            # Save to leaderboard
            playerRank.add()

            # Set cool colour for top 3
            ranking = playerRank.getPos()
            if ranking <= 3: end_game_screen.win.leaderboard.switchState(str(ranking), False)
            else: end_game_screen.win.leaderboard.switchState('', False)

            # Set player leaderboard on win screen
            end_game_screen.win.leaderboard.postion.setText(str(ranking), withDisplay=False)
            end_game_screen.win.leaderboard.nickname.setText(player.nickname, withDisplay=False)
            end_game_screen.win.leaderboard.days.setText(str(player.stats.day), withDisplay=False)

            # Load the changes
            end_game_screen.win.load(withItems=['leaderboard'], refresh=True)

            # Play win sound effect
            Sound.win.play()

        # Check if gameover screen is the one loaded
        elif end_game_screen.gameover.loaded:
            # Play gameover sound effect
            Sound.game_over.play()

    @staticmethod
    def run():
        # Get action
        event_result = end_game_screen.events.get()

        # No action
        if event_result == None: return
        # Quit program
        if event_result.contains('outcome', 'quit'): return 'quit'


##################
# Screen objects #
##################
end_game_screen = screen (
    name = 'end_game',
    main = end_game,
    
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
                'selectable': False,
                'data': {
                    'postion': Text (
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