######################################
# Import and initialize the librarys #
######################################
from code.api.core import os, log, PgEss
from code.api.events import gameEvent
from code.api.objects import Screen, Frame
from code.api.actions import Runclass, Switchscreen, Alert, Info
from code.api.data.Text import Text, TextFormat
from code.api.data.Sprite import Sprite
from code.api.data.Grid import Grid
from code.logic.move import Move
from code.logic.playerData import PlayerData
from code.logic.rest import rest
from code.logic.orb import Orb
from code.logic.attack import Attack


#################
# Setup logging #
#################
filename = os.path.basename(__file__).split('.')[0]
logger = log.get_logger(filename)


############################
# Screen main action class #
############################
class game:

    @staticmethod
    def init():
        # Ensure game events are started
        gameEvent.stats.play()
        gameEvent.animate.play()
        gameEvent.orb_change.play()
    
    @staticmethod
    def run():
        # Get action
        event_result = game_screen.events.get()

        # No action
        if event_result == None: return
        # Quit program
        if event_result.contains('outcome', 'quit'): return 'quit'

    @staticmethod
    def end():
        # Pause all game events
        gameEvent.stats.pause()
        gameEvent.animate.pause()

    @staticmethod
    def clear_events():
        # Clear the game events
        gameEvent.stats.clearQueue()
        gameEvent.animate.clearQueue()
        gameEvent.orb_change.clearQueue()


##################
# Screen objects #
##################
game_screen = Screen (
    name = 'game',
    main = game,

    keyboard = {
        'exit': {
            'keys': [27],
            'action': Alert (
                type='confirm', 
                title='Exit Game',
                content='Are you sure you want to exit to main menu?',
                yes= [
                    Runclass(run=game.clear_events),
                    Switchscreen(type='back', screen='mainmenu')
                ]
            ),
        }
    },

    surfaces = {
        'map': {
            'frame': Frame(x=0, y=0, w=1055, h=1080),
            'selectable': False,
            'grid': {
                'frame': Frame(x=115, y=125, w=830, h=830),
                'type': 'map',
                'imageData': {'frame': Frame(x=0, y=0, w=1055, h=1080)},
                'data': {
                    'Grid': Grid (
                        frame=Frame(x=115, y=125, w=830, h=830),
                        sprite=Sprite(spritePage=['game', 'map', 'sprites'], size=(101, 101)),
                        rows=8, columns=8
                        )
                }
            }
        },

        'info': {
            'frame': Frame(x=1060, y=0, w=740, h=520),
            'selectable': False,
            'days': { 
                'type': 'text',
                'frame': Frame(x=88, y=110, w=267, h=75),
                'imageData': {'frame': Frame(x=0, y=0, w=350, h=185)},
                'selectable': False,
                'data': {
                    'day': Text (
                        frame = Frame(x=88, y=110, w=267, h=75),
                        prefix = 'Day: ',
                        text = '1',
                        format = TextFormat(fontSize=68, align='left', pos='center')
                    )
                },
            },
            'hero': {
                'type': 'object',
                'frame': Frame(x=88, y=185, w=235, h=164),
                'imageData': {'frame': Frame(x=88, y=185, w=235, h=164)},
                'selectable': False,
                'data': {
                    'stats': Text (
                        frame = Frame(x=175, y=185, w=112, h=59),
                        text = '',
                        format = TextFormat(fontSize=52, align='left', pos='center', colour=PgEss.colour.red)
                    ),
                    'weapons': Grid (
                        frame=Frame(x=184, y=185, w=120, h=160),
                        sprite=Sprite(spritePage=['game', 'info', 'weapons'], size=(50, 50)),
                        rows=3, columns=2, spacing=2, size=50
                    ),
                }
            },
            'stats': { 
                'type': 'text',
                'frame': Frame(x=323, y=111, w=417, h=350),
                'imageData': {'frame': Frame(x=323, y=0, w=417, h=350)},
                'selectable': False,
                'data': {
                    'damage': Text (
                        frame = Frame(x=323, y=111, w=307, h=59),
                        prefix = 'Damage: ',
                        text = '2 - 4',
                        format = TextFormat(fontSize=52, align='right', pos='center', colour=PgEss.colour.red)
                    ),
                    'defence': Text (
                        frame = Frame(x=323, y=170, w=307, h=59),
                        prefix = 'Defence: ',
                        text = '1',
                        format = TextFormat(fontSize=52, align='right', pos='center', colour=PgEss.colour.blue)
                    ),
                    'health': Text (
                        frame = Frame(x=323, y=229, w=307, h=59),
                        prefix = 'Health: ',
                        text = '20/20',
                        format = TextFormat(fontSize=52, align='right', pos='center', colour=PgEss.colour.green)
                    ),
                    'elixir': Text (
                        frame = Frame(x=323, y=288, w=307, h=59),
                        prefix = 'Elixir: ',
                        text = '0',
                        format = TextFormat(fontSize=52, align='right', pos='center', colour=PgEss.colour.purple)
                    ),
                },
            },
            'story': { 
                'type': 'text',
                'frame': Frame(x=88, y=358, w=542, h=152),
                'imageData': {'frame': Frame(x=0, y=358, w=740, h=157)},
                'selectable': False,
                'data': {
                    'message': Text (
                        frame = Frame(x=88, y=358, w=542, h=152),
                        text = 'You are in a town.',
                        format = TextFormat(fontSize=56, align='left', pos='center', warpText=24, lineSpacing=0.7, colour=PgEss.colour.black)
                    ),
                },
            },
        },

        'in_town': {
            'frame': Frame(x=1060, y=520, w=740, h=560),
            'rest': {
                'type': 'button',
                'frame': Frame(x=118, y=40, w=218, h=167),
                'imageData': {'frame': Frame(x=118, y=40, w=218, h=167)},
                'action': Runclass(run=rest.initSurface)
            },
            'shop': {
                'type': 'button',
                'frame': Frame(x=375, y=40, w=218, h=167),
                'imageData': {'frame': Frame(x=375, y=40, w=218, h=167)},
                'action': Switchscreen(type='load', screen='shop')
            },
            'move': {
                'type': 'button',
                'frame': Frame(x=118, y=248, w=218, h=167),
                'imageData': {'frame': Frame(x=118, y=248, w=218, h=167)},
                'action': Runclass(run=Move.initSurface)
            },
            'save': {
                'type': 'button',
                'frame': Frame(x=375, y=248, w=218, h=167),
                'imageData': {'frame': Frame(x=375, y=248, w=218, h=167)},
                'action': Runclass(run=PlayerData.save),
            },
        },

        'in_open': {
            'frame': Frame(x=1060, y=520, w=740, h=560),
            'sense_orb': {
                'type': 'button',
                'frame': Frame(x=118, y=40, w=476, h=167),
                'imageData': {'frame': Frame(x=118, y=40, w=476, h=167)},
                'action': Runclass(run=Orb.initSurface)
            },
            'move': {
                'type': 'button',
                'frame': Frame(x=118, y=248, w=218, h=167),
                'imageData': {'frame': Frame(x=118, y=248, w=218, h=167)},
                'action': Runclass(run=Move.initSurface)
            },
            'save': {
                'type': 'button',
                'frame': Frame(x=375, y=248, w=218, h=167),
                'imageData': {'frame': Frame(x=375, y=248, w=218, h=167)},
                'action': Runclass(run=PlayerData.save),
            },
        },

        'rest': {
            'frame': Frame(x=1060, y=520, w=740, h=560),
            'stats': { 
                'type': 'text',
                'frame': Frame(x=323, y=108, w=307, h=59),
                'imageData': {'frame': Frame(x=323, y=108, w=307, h=59)},
                'selectable': False,
                'data': {
                    'health': Text (
                        frame = Frame(x=323, y=108, w=307, h=59),
                        prefix = 'Health: ',
                        text = '+ 0',
                        format = TextFormat(fontSize=52, align='left', pos='center', colour=PgEss.colour.green)
                    ),
                },
            },
            'back': {
                'type': 'button',
                'frame': Frame(x=88, y=318, w=173, h=98),
                'imageData': {'frame': Frame(x=88, y=318, w=173, h=98)},
                'action': Runclass(run=rest.back)
            },
            'sleep': {
                'type': 'button',
                'frame': Frame(x=295, y=318, w=335, h=98),
                'imageData': {'frame': Frame(x=295, y=318, w=335, h=98)},
                'action': Runclass(run=rest.Rest)
            },
        },

        'move': {
            'frame': Frame(x=1060, y=520, w=740, h=560),
            'up': {
                'type': 'button',
                'frame': Frame(x=304, y=33-13, w=104, h=94),
                'imageData': {'frame': Frame(x=304, y=33-13, w=104, h=94)},
                'action': Runclass(
                    run = gameEvent.animate.addQueue, 
                    parameters = {'Action': Runclass(run=Move.move, parameters={'direction': 'up'})}
                    )
            },
            'down': {
                'type': 'button',
                'frame': Frame(x=304, y=220-13, w=104, h=94),
                'imageData': {'frame': Frame(x=304, y=220-13, w=104, h=94)},
                'action': Runclass(
                    run = gameEvent.animate.addQueue, 
                    parameters = {'Action': Runclass(run=Move.move, parameters={'direction': 'down'})}
                    )
            },
            'left': {
                'type': 'button',
                'frame': Frame(x=200, y=126-13, w=104, h=94),
                'imageData': {'frame': Frame(x=200, y=126-13, w=104, h=94)},
                'action': Runclass(
                    run = gameEvent.animate.addQueue, 
                    parameters = {'Action': Runclass(run=Move.move, parameters={'direction': 'left'})}
                    )
            },
            'right': {
                'type': 'button',
                'frame': Frame(x=407, y=126-13, w=104, h=94),
                'imageData': {'frame': Frame(x=407, y=126-13, w=104, h=94)},
                'action': Runclass(
                    run = gameEvent.animate.addQueue, 
                    parameters = {'Action': Runclass(run=Move.move, parameters={'direction': 'right'})}
                    )
            },
            'back': {
                'type': 'button',
                'frame': Frame(x=166, y=377, w=378, h=75),
                'imageData': {'frame': Frame(x=166, y=377, w=378, h=75)},
                'action': Runclass(run=Move.back)
            },
        },

        'no_orb': {
            'frame': Frame(x=1060, y=520, w=740, h=560),
            'compass': {
                'type': 'point',
                'frame': Frame(x=0, y=0, w=740, h=560),
                'imageData': {'frame': Frame(x=0, y=0, w=740, h=560)},
                'selectable': False
            },
            'ok': {
                'type': 'button',
                'frame': Frame(x=166, y=364, w=378, h=75),
                'imageData': {'frame': Frame(x=166, y=364, w=378, h=75)},
                'action': Runclass(run=Orb.back)
            },
        },

        'found_orb': {
            'frame': Frame(x=1060, y=520, w=740, h=560),
            'stats': { 
                'type': 'text',
                'frame': Frame(x=323, y=79, w=307, h=236),
                'imageData': {'frame': Frame(x=323, y=79, w=307, h=236)},
                'selectable': False,
                'data': {
                    'damage': Text (
                        frame = Frame(x=323, y=79, w=307, h=59),
                        prefix = 'Damage: ',
                        text = '+ 5',
                        format = TextFormat(fontSize=52, align='left', pos='center', colour=PgEss.colour.red)
                    ),
                    'defence': Text (
                        frame = Frame(x=323, y=138, w=307, h=59),
                        prefix = 'Defence: ',
                        text = '+ 5',
                        format = TextFormat(fontSize=52, align='left', pos='center', colour=PgEss.colour.blue)
                    ),
                },
            },
            'take': {
                'type': 'button',
                'frame': Frame(x=88, y=318, w=542, h=98),
                'imageData': {'frame': Frame(x=88, y=318, w=542, h=98)},
                'action': Runclass(run=Orb.take)
            },
        },

        'attack': {
            'frame': Frame(x=1060, y=520, w=740, h=560),
            'enemy': {
                'type': 'object',
                'frame': Frame(x=88, y=15, w=207, h=217),
                'imageData': {'frame': Frame(x=88, y=15, w=207, h=217)},
                'selectable': False,
                'data': {
                    'stats': Text (
                        frame = Frame(x=172, y=17, w=112, h=59),
                        text = '',
                        format = TextFormat(fontSize=52, align='right', pos='center', colour=PgEss.colour.red)
                    ),
                }
            },
            'stats': { 
                'type': 'text',
                'frame': Frame(x=323, y=35, w=307, h=236),
                'imageData': {'frame': Frame(x=323, y=35, w=307, h=236)},
                'selectable': False,
                'data': {
                    'damage': Text (
                        frame = Frame(x=323, y=35, w=307, h=59),
                        prefix = 'Damage: ',
                        text = '1 - 3',
                        format = TextFormat(fontSize=52, align='left', pos='center', colour=PgEss.colour.red)
                    ),
                    'defence': Text (
                        frame = Frame(x=323, y=94, w=307, h=59),
                        prefix = 'Defence: ',
                        text = '2',
                        format = TextFormat(fontSize=52, align='left', pos='center', colour=PgEss.colour.blue)
                    ),
                    'health': Text (
                        frame = Frame(x=323, y=153, w=307, h=59),
                        prefix = 'Health: ',
                        text = '12',
                        format = TextFormat(fontSize=52, align='left', pos='center', colour=PgEss.colour.green)
                    ),
                },
            },
            'attack': {
                'type': 'button',
                'frame': Frame(x=88, y=302, w=251, h=104),
                'imageData': {'frame': Frame(x=88, y=302, w=251, h=104)},
                'action': Runclass(
                    run = gameEvent.animate.addQueue, 
                    parameters = {'Action': Runclass(run=Attack.attack)}
                    )
            },
            'run': {
                'type': 'button',
                'frame': Frame(x=380, y=302, w=251, h=104),
                'imageData': {'frame': Frame(x=380, y=302, w=251, h=104)},
                'action': Runclass(run=Attack.run)
            },
        }
        
    }
)