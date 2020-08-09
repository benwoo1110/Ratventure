######################################
# Import and initialize the librarys #
######################################
from code.api.core import os, log, pg, screens
from code.api.objects import screen, Frame
from code.api.actions import Runclass, Switchscreen, Info
from code.api.data.Text import Text, textFormat
from code.logic.player import player
from code.logic.store import store


#################
# Setup logging #
#################
filename = os.path.basename(__file__).split('.')[0]
logger = log.get_logger(filename)
logger.info('Loading up {}...'.format(filename))


############################
# Screen main action class #
############################
class shop:

    @staticmethod
    def init():
        # Set player stats
        player.stats.display('damage', shop_screen.store.stats)
        player.stats.display('defence', shop_screen.store.stats)
        player.stats.display('health', shop_screen.store.stats)
        player.stats.display('elixir', shop_screen.store.stats)

        shop_screen.store.load(withItems=['stats'], refresh=True)

    @staticmethod
    def run():
        # Get action
        event_result = shop_screen.events.get()

        # No action
        if event_result == None: return
        # Quit program
        if event_result.contains('outcome', 'quit'): return 'quit'

    @staticmethod
    def end():
        # Set player stats for game screen
        player.stats.display('damage', screens.game.info.stats)
        player.stats.display('defence', screens.game.info.stats)
        player.stats.display('health', screens.game.info.stats)
        player.stats.display('elixir', screens.game.info.stats)

        screens.game.info.load(withItems=['stats'], refresh=True)


##################
# Screen objects #
##################
shop_screen = screen (
    name = 'shop',
    main = shop,

    keyboard = {
        'back': {
            'keys': [27],
            'action': Switchscreen(type='back')
        }
    },

    surfaces = {
        'store': {
            'frame': Frame(x=0, y=0, w=1800, h=1080),
            'back': {
                'type': 'button',
                'frame': Frame(x=70, y=50, w=132, h=103),
                'imageData': {'frame': Frame(x=70, y=50, w=132, h=103)},
                'action': Switchscreen(type='back')
            },
            'stats': {
                'type': 'text',
                'frame': Frame(x=1075, y=0, w=725, h=270),
                'imageData': {'frame': Frame(x=1075, y=0, w=725, h=270)},
                'data': {
                    'damage': Text (
                        frame = Frame(x=1414, y=81, w=307, h=59),
                        prefix = 'Damage: ',
                        text = '2 - 4',
                        format = textFormat(fontSize=52, align='left', pos='center', colour=pg.colour.red)
                    ),
                    'defence': Text (
                        frame = Frame(x=1414, y=140, w=307, h=59),
                        prefix = 'Defence: ',
                        text = '1',
                        format = textFormat(fontSize=52, align='left', pos='center', colour=pg.colour.blue)
                    ),
                    'health': Text (
                        frame = Frame(x=1099, y=81, w=307, h=59),
                        prefix = 'Health: ',
                        text = '20/20',
                        format = textFormat(fontSize=52, align='left', pos='center', colour=pg.colour.green)
                    ),
                    'elixir': Text (
                        frame = Frame(x=1099, y=140, w=307, h=59),
                        prefix = 'Elixir: ',
                        text = '10',
                        format = textFormat(fontSize=52, align='left', pos='center', colour=pg.colour.purple)
                    ),
                },
            },
            'shield': {
                'type': 'button',
                'frame': Frame(x=609, y=301, w=527, h=300),
                'imageData': {'frame': Frame(x=609, y=301, w=527, h=300)},
                'overlayDataFrame': True,
                'action': Runclass(run=store.checkBuy, parameters={'weapon': 'shield'}),
                'data': {
                    'object': Text (
                        frame = Frame(x=120, y=25, w=237, h=83),
                        text = 'Shield',
                        format = textFormat(fontSize=76, align='left', pos='center', colour=pg.colour.white)
                    ),
                    'price': Text (
                        frame = Frame(x=357, y=33, w=83, h=69),
                        text = '20',
                        format = textFormat(fontSize=62, align='right', pos='center', colour=pg.colour.purple)
                    ),
                    'gain_1': Text (
                        frame = Frame(x=25, y=112, w=349, h=75),
                        prefix = 'Defence: ', text = '+ 2',
                        format = textFormat(fontSize=68, align='left', pos='center', colour=pg.colour.blue)
                    ),
                    'gain_2': Text (
                        frame = Frame(x=25, y=185, w=349, h=75),
                        prefix = 'Damage: ', text = '+ 1',
                        format = textFormat(fontSize=68, align='left', pos='center', colour=pg.colour.red)
                    ),
                }
            },
            'sword': {
                'type': 'button',
                'frame': Frame(x=1194, y=301, w=527, h=300),
                'imageData': {'frame': Frame(x=1194, y=301, w=527, h=300)},
                'overlayDataFrame': True,
                'action': Runclass(run=store.checkBuy, parameters={'weapon': 'sword'}),
                'data': {
                    'object': Text (
                        frame = Frame(x=120, y=25, w=237, h=83),
                        text = 'Sword',
                        format = textFormat(fontSize=76, align='left', pos='center', colour=pg.colour.white)
                    ),
                    'price': Text (
                        frame = Frame(x=357, y=33, w=83, h=69),
                        text = '20',
                        format = textFormat(fontSize=62, align='right', pos='center', colour=pg.colour.purple)
                    ),
                    'gain_1': Text (
                        frame = Frame(x=25, y=112, w=349, h=75),
                        prefix = 'Defence: ', text = '+ 2',
                        format = textFormat(fontSize=68, align='left', pos='center', colour=pg.colour.blue)
                    ),
                    'gain_2': Text (
                        frame = Frame(x=25, y=185, w=349, h=75),
                        prefix = 'Damage: ', text = '+ 1',
                        format = textFormat(fontSize=68, align='left', pos='center', colour=pg.colour.red)
                    ),
                }
            },
            'armour': {
                'type': 'button',
                'frame': Frame(x=609, y=666, w=527, h=300),
                'imageData': {'frame': Frame(x=609, y=666, w=527, h=300)},
                'overlayDataFrame': True,
                'action': Runclass(run=store.checkBuy, parameters={'weapon': 'armour'}),
                'data': {
                    'object': Text (
                        frame = Frame(x=120, y=25, w=237, h=83),
                        text = 'Armour',
                        format = textFormat(fontSize=76, align='left', pos='center', colour=pg.colour.white)
                    ),
                    'price': Text (
                        frame = Frame(x=357, y=33, w=83, h=69),
                        text = '20',
                        format = textFormat(fontSize=62, align='right', pos='center', colour=pg.colour.purple)
                    ),
                    'gain_1': Text (
                        frame = Frame(x=25, y=112, w=349, h=75),
                        prefix = 'Defence: ', text = '+ 2',
                        format = textFormat(fontSize=68, align='left', pos='center', colour=pg.colour.blue)
                    ),
                    'gain_2': Text (
                        frame = Frame(x=25, y=185, w=349, h=75),
                        prefix = 'Damage: ', text = '+ 1',
                        format = textFormat(fontSize=68, align='left', pos='center', colour=pg.colour.red)
                    ),
                }
            },
            'potion': {
                'type': 'button',
                'frame': Frame(x=1194, y=666, w=527, h=300),
                'imageData': {'frame': Frame(x=1194, y=666, w=527, h=300)},
                'overlayDataFrame': True,
                'action': Runclass(run=store.checkBuy, parameters={'weapon': 'potion'}),
                'data': {
                    'object': Text (
                        frame = Frame(x=120, y=25, w=237, h=83),
                        text = 'Potion',
                        format = textFormat(fontSize=76, align='left', pos='center', colour=pg.colour.white)
                    ),
                    'price': Text (
                        frame = Frame(x=357, y=33, w=83, h=69),
                        text = '20',
                        format = textFormat(fontSize=62, align='right', pos='center', colour=pg.colour.purple)
                    ),
                    'gain_1': Text (
                        frame = Frame(x=25, y=112, w=349, h=75),
                        prefix = 'Defence: ', text = '+ 2',
                        format = textFormat(fontSize=68, align='left', pos='center', colour=pg.colour.blue)
                    ),
                    'gain_2': Text (
                        frame = Frame(x=25, y=185, w=349, h=75),
                        prefix = 'Damage: ', text = '+ 1',
                        format = textFormat(fontSize=68, align='left', pos='center', colour=pg.colour.red)
                    ),
                }
            },
        }
    }
)