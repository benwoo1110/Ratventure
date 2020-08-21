######################################
# Import and initialize the librarys #
######################################
from code.api.core import os, log, pg, screens
from code.api.objects import screen, Frame
from code.api.actions import Runclass, Switchscreen, Info
from code.api.data.Text import Text, textFormat
from code.logic.playerRank import playerRank


#################
# Setup logging #
#################
filename = os.path.basename(__file__).split('.')[0]
logger = log.get_logger(filename)


############################
# Screen main action class #
############################
class leaderboard:

    @staticmethod
    def init():
        playerRank.showList()

    @staticmethod
    def run():
        # Get action
        event_result = leaderboard_screen.events.get()

        # No action
        if event_result == None: return
        # Quit program
        if event_result.contains('outcome', 'quit'): return 'quit'


##################
# Screen objects #
##################
leaderboard_screen = screen (
    name = 'leaderboard',
    main = leaderboard,
    firstLoad=[],

    keyboard = {
        'back': {
            'keys': [27],
            'action': Switchscreen(type='back', screen='mainmenu')
        },
        'page_back': {
            'keys': [1073741904],
            'action': Runclass(run=playerRank.updateList, parameters={'page': -1})
        },
        'page_next': {
            'keys': [1073741903],
            'action': Runclass(run=playerRank.updateList, parameters={'page': 1})
        },
    },

    surfaces = {
        'board': {
            'frame': Frame(x=0, y=0, w=1800, h=1080),
            'alpha': True,
            'back': {
                'type': 'button',
                'frame': Frame(x=141, y=58, w=132, h=103),
                'imageData': {'frame': Frame(x=141, y=58, w=132, h=103)},
                'action': Switchscreen(type='back')
            },
            'page_text': {
                'type': 'text',
                'frame': Frame(x=769, y=974, w=262, h=75),
                'imageData': {'frame': Frame(x=769, y=974, w=262, h=106)},
                'selectable': False,
                    'data': {
                    'pages': Text (
                        frame = Frame(x=769, y=974, w=262, h=75),
                        prefix = '1', text = ' / ', suffix = '10',
                        format = textFormat(fontSize=68, align='center', pos='center', colour=pg.colour.white)
                    ),
                }
            },
            'page_back': {
                'type': 'button',
                'frame': Frame(x=729, y=984, w=57, h=40),
                'imageData': {'frame': Frame(x=729, y=984, w=96, h=40)},
                'action': Runclass(run=playerRank.updateList, parameters={'page': -1})
            },
            'page_next': {
                'type': 'button',
                'frame': Frame(x=1031, y=984, w=57, h=40),
                'imageData': {'frame': Frame(x=1031, y=984, w=96, h=40)},
                'action': Runclass(run=playerRank.updateList, parameters={'page': 1})
            },
        },

        'list_1': {
            'frame':  Frame(x=0, y=220, w=1800, h=168),
            'rank': {
                'type': 'object',
                'frame':  Frame(x=141, y=3, w=1519, h=140),
                'imageData': {'frame': Frame(x=141, y=3, w=1519, h=140)},
                'selectable': False,
                'data': {
                    'postion': Text (
                        frame = Frame(x=149, y=3, w=142, h=140),
                        text = '1',
                        format = textFormat(fontSize=96, align='center', pos='center', colour=pg.colour.white)
                    ),
                    'nickname': Text (
                        frame = Frame(x=316, y=3, w=670, h=140),
                        text = 'Demo',
                        format = textFormat(fontSize=96, align='left', pos='center', colour=pg.colour.white)
                    ),
                    'days': Text (
                        frame = Frame(x=1210, y=3, w=379, h=140),
                        text = '100',
                        suffix = ' days',
                        format = textFormat(fontSize=96, align='right', pos='center', colour=pg.colour.white)
                    ),
                }
            },
        },

        'list_2': {
            'frame':  Frame(x=0, y=404, w=1800, h=168),
            'rank': {
                'type': 'object',
                'frame':  Frame(x=141, y=3, w=1519, h=140),
                'imageData': {'frame': Frame(x=141, y=3, w=1519, h=140)},
                'selectable': False,
                'data': {
                    'postion': Text (
                        frame = Frame(x=149, y=3, w=142, h=140),
                        text = '1',
                        format = textFormat(fontSize=96, align='center', pos='center', colour=pg.colour.white)
                    ),
                    'nickname': Text (
                        frame = Frame(x=316, y=3, w=670, h=140),
                        text = 'Demo',
                        format = textFormat(fontSize=96, align='left', pos='center', colour=pg.colour.white)
                    ),
                    'days': Text (
                        frame = Frame(x=1210, y=3, w=379, h=140),
                        text = '100',
                        suffix = ' days',
                        format = textFormat(fontSize=96, align='right', pos='center', colour=pg.colour.white)
                    ),
                }
            },
        },

        'list_3': {
            'frame':  Frame(x=0, y=588, w=1800, h=168),
            'rank': {
                'type': 'object',
                'frame':  Frame(x=141, y=3, w=1519, h=140),
                'imageData': {'frame': Frame(x=141, y=3, w=1519, h=140)},
                'selectable': False,
                'data': {
                    'postion': Text (
                        frame = Frame(x=149, y=3, w=142, h=140),
                        text = '1',
                        format = textFormat(fontSize=96, align='center', pos='center', colour=pg.colour.white)
                    ),
                    'nickname': Text (
                        frame = Frame(x=316, y=3, w=670, h=140),
                        text = 'Demo',
                        format = textFormat(fontSize=96, align='left', pos='center', colour=pg.colour.white)
                    ),
                    'days': Text (
                        frame = Frame(x=1210, y=3, w=379, h=140),
                        text = '100',
                        suffix = ' days',
                        format = textFormat(fontSize=96, align='right', pos='center', colour=pg.colour.white)
                    ),
                }
            },
        },

        'list_4': {
            'frame':  Frame(x=0, y=772, w=1800, h=168),
            'rank': {
                'type': 'object',
                'frame':  Frame(x=141, y=3, w=1519, h=140),
                'imageData': {'frame': Frame(x=141, y=3, w=1519, h=140)},
                'selectable': False,
                'data': {
                    'postion': Text (
                        frame = Frame(x=149, y=3, w=142, h=140),
                        text = '1',
                        format = textFormat(fontSize=96, align='center', pos='center', colour=pg.colour.white)
                    ),
                    'nickname': Text (
                        frame = Frame(x=316, y=3, w=670, h=140),
                        text = 'Demo',
                        format = textFormat(fontSize=96, align='left', pos='center', colour=pg.colour.white)
                    ),
                    'days': Text (
                        frame = Frame(x=1210, y=3, w=379, h=140),
                        text = '100',
                        suffix = ' days',
                        format = textFormat(fontSize=96, align='right', pos='center', colour=pg.colour.white)
                    ),
                }
            },
        },

    }
)