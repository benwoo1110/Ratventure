######################################
# Import and initialize the librarys #
######################################
from code.api.core import os, log, pg
from code.api.objects import screen, Frame
from code.api.actions import Runclass, Switchscreen, Alert
from code.api.data.Text import Text, textFormat
from code.logic.playerSaves import playerSaves


#################
# Setup logging #
#################
filename = os.path.basename(__file__).split('.')[0]
logger = log.get_logger(filename)
logger.info('Loading up {}...'.format(filename))


############################
# Screen main action class #
############################
class saves:

    @staticmethod
    def init():
        playerSaves.showList()

    @staticmethod
    def run():
        # Get action
        event_result = saves_screen.events.get()

        # No action
        if event_result == None: return
        # Quit program
        if event_result.contains('outcome', 'quit'): return 'quit'


##################
# Screen objects #
##################
saves_screen = screen (
    name = 'saves',
    main = saves,

    keyboard = {
        'back': {
            'keys': [27],
            'action': Switchscreen(type='back', screen='mainmenu')
        },
        'page_back': {
            'keys': [1073741904],
            'action': Runclass(run=playerSaves.updateList, parameters={'page': -1})
        },
        'page_next': {
            'keys': [1073741903],
            'action': Runclass(run=playerSaves.updateList, parameters={'page': 1})
        },
    },

    surfaces = {
        'board': {
            'frame': Frame(x=0, y=0, w=1800, h=1080),
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
                'action': Runclass(run=playerSaves.updateList, parameters={'page': -1})
            },
            'page_next': {
                'type': 'button',
                'frame': Frame(x=1031, y=984, w=57, h=40),
                'imageData': {'frame': Frame(x=1031, y=984, w=96, h=40)},
                'action': Runclass(run=playerSaves.updateList, parameters={'page': 1})
            },
            'delete_all': {
                'type': 'button',
                'frame': Frame(x=1528, y=58, w=132, h=103),
                'imageData': {'frame': Frame(x=1528, y=58, w=132, h=103)},
                'action': Alert (
                    type='confirm', 
                    title='Delete All',
                    content='Are you sure you want to delete all saves?',
                    yes=Runclass(run=playerSaves.deleteAll)
                ),
            }
        },

        'list_1': {
            'frame':  Frame(x=0, y=220, w=1800, h=168),
            'file': {
                'type': 'text',
                'frame':  Frame(x=181, y=3, w=660, h=140),
                'imageData': {'frame': Frame(x=181, y=3, w=660, h=140)},
                'selectable': False,
                'data': {
                    'fileid': '',
                    'nickname': Text (
                        frame = Frame(x=181, y=3, w=576, h=140),
                        text = 'Ben 10',
                        format = textFormat(fontSize=96, align='left', pos='center', colour=pg.colour.white)
                    ),
                    'date': Text (
                        frame = Frame(x=794, y=3, w=576, h=140),
                        text = '20/12/2020 10:23pm',
                        format = textFormat(fontSize=62, align='right', pos='center', colour=pg.colour.white)
                    ),
                }
            },
            'delete': {
                'type': 'button',
                'frame': Frame(x=1429, y=22, w=100, h=100),
                'imageData': {'frame': Frame(x=1429, y=3, w=100, h=100)},
                'action': Alert (
                    type='confirm', 
                    title='Deleted Saved',
                    content='Are you sure you want to delete the savefile?',
                    yes=Runclass(run=playerSaves.deleteSaved, parameters={'number': 1})
                ),
            },
            'play': {
                'type': 'button',
                'frame': Frame(x=1532, y=22, w=100, h=100),
                'imageData': {'frame': Frame(x=1532, y=3, w=100, h=100)},
                'action': Runclass(run=playerSaves.playSaved, parameters={'number': 1})
            },
        },

        'list_2': {
            'frame':  Frame(x=0, y=404, w=1800, h=168),
            'file': {
                'type': 'text',
                'frame':  Frame(x=181, y=3, w=660, h=140),
                'imageData': {'frame': Frame(x=181, y=3, w=660, h=140)},
                'selectable': False,
                'data': {
                    'fileid': '',
                    'nickname': Text (
                        frame = Frame(x=181, y=3, w=576, h=140),
                        text = 'Ben 10',
                        format = textFormat(fontSize=96, align='left', pos='center', colour=pg.colour.white)
                    ),
                    'date': Text (
                        frame = Frame(x=794, y=3, w=576, h=140),
                        text = '20/12/2020 10:23pm',
                        format = textFormat(fontSize=62, align='right', pos='center', colour=pg.colour.white)
                    ),
                }
            },
            'delete': {
                'type': 'button',
                'frame': Frame(x=1429, y=22, w=100, h=100),
                'imageData': {'frame': Frame(x=1429, y=3, w=100, h=100)},
                'action': Alert (
                    type='confirm', 
                    title='Deleted Saved',
                    content='Are you sure you want to delete the savefile?',
                    yes=Runclass(run=playerSaves.deleteSaved, parameters={'number': 2})
                ),
            },
            'play': {
                'type': 'button',
                'frame': Frame(x=1532, y=22, w=100, h=100),
                'imageData': {'frame': Frame(x=1532, y=3, w=100, h=100)},
                'action': Runclass(run=playerSaves.playSaved, parameters={'number': 2})
            },
        },

        'list_3': {
            'frame':  Frame(x=0, y=588, w=1800, h=168),
            'file': {
                'type': 'text',
                'frame':  Frame(x=181, y=3, w=660, h=140),
                'imageData': {'frame': Frame(x=181, y=3, w=660, h=140)},
                'selectable': False,
                'data': {
                    'fileid': '',
                    'nickname': Text (
                        frame = Frame(x=181, y=3, w=576, h=140),
                        text = 'Ben 10',
                        format = textFormat(fontSize=96, align='left', pos='center', colour=pg.colour.white)
                    ),
                    'date': Text (
                        frame = Frame(x=794, y=3, w=576, h=140),
                        text = '20/12/2020 10:23pm',
                        format = textFormat(fontSize=62, align='right', pos='center', colour=pg.colour.white)
                    ),
                }
            },
            'delete': {
                'type': 'button',
                'frame': Frame(x=1429, y=22, w=100, h=100),
                'imageData': {'frame': Frame(x=1429, y=3, w=100, h=100)},
                'action': Alert (
                    type='confirm', 
                    title='Deleted Saved',
                    content='Are you sure you want to delete the savefile?',
                    yes=Runclass(run=playerSaves.deleteSaved, parameters={'number': 3})
                ),
            },
            'play': {
                'type': 'button',
                'frame': Frame(x=1532, y=22, w=100, h=100),
                'imageData': {'frame': Frame(x=1532, y=3, w=100, h=100)},
                'action': Runclass(run=playerSaves.playSaved, parameters={'number': 3})
            },
        },

        'list_4': {
            'frame':  Frame(x=0, y=772, w=1800, h=168),
            'file': {
                'type': 'text',
                'frame':  Frame(x=181, y=3, w=660, h=140),
                'imageData': {'frame': Frame(x=181, y=3, w=660, h=140)},
                'selectable': False,
                'data': {
                    'fileid': '',
                    'nickname': Text (
                        frame = Frame(x=181, y=3, w=576, h=140),
                        text = 'Ben 10',
                        format = textFormat(fontSize=96, align='left', pos='center', colour=pg.colour.white)
                    ),
                    'date': Text (
                        frame = Frame(x=794, y=3, w=576, h=140),
                        text = '20/12/2020 10:23pm',
                        format = textFormat(fontSize=62, align='right', pos='center', colour=pg.colour.white)
                    ),
                }
            },
            'delete': {
                'type': 'button',
                'frame': Frame(x=1429, y=22, w=100, h=100),
                'imageData': {'frame': Frame(x=1429, y=3, w=100, h=100)},
                'action': Alert (
                    type='confirm', 
                    title='Deleted Saved',
                    content='Are you sure you want to delete the savefile?',
                    yes=Runclass(run=playerSaves.deleteSaved, parameters={'number': 4})
                ),
            },
            'play': {
                'type': 'button',
                'frame': Frame(x=1532, y=22, w=100, h=100),
                'imageData': {'frame': Frame(x=1532, y=3, w=100, h=100)},
                'action':  Runclass(run=playerSaves.playSaved, parameters={'number': 4})
            },
        },
    }
)