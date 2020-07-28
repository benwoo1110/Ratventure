######################################
# Import and initialize the librarys #
######################################
from code.api.core import pg, pygame
from code.api.objects import screen, Frame
from code.api.data.text import text, textFormat


mainmenu_screen = screen (
    name = 'mainmenu',
    surfaces = {
        'menu': {
            'frame': Frame(x=0, y=0, w=1800, h=1080),
            'new_game': {
                'type': 'button',
                'frame': Frame(x=983, y=253, w=529, h=140),
                'imageData': {'frame': Frame(x=983, y=253, w=529, h=140)}
            },
            'load_saved': {
                'type': 'button',
                'frame': Frame(x=983, y=459, w=529, h=140),
                'imageData': {'frame': Frame(x=983, y=459, w=529, h=140)}
            },
            'leaderboard':{ 
                'type': 'button',
                'frame': Frame(x=983, y=665, w=529, h=140),
                'imageData': {'frame': Frame(x=983, y=665, w=529, h=140)},
                'data': {
                    'testing': text(
                        frame = Frame(x=983, y=665, w=529, h=140),
                        text = 'Very cool',
                        format = textFormat (
                            fontSize = 56,
                            align = 'left',
                            pos = 'center',
                            warpText = 19,
                            lineSpacing=0.7
                        )
                    )
                },
            },
            'quit': {
                'type': 'button',
                'frame': Frame(x=983, y=870, w=529, h=140),
                'imageData': {'frame': Frame(x=983, y=870, w=529, h=140)}
            },
        }
    }
)


class mainmenu:

    def run():
        mainmenu_screen.menu.new_game.switchState('Hover')
        mainmenu_screen.display()

        mainmenu_screen.menu.leaderboard.testing.setText('This is a test to see. With more lines now')

        while True:
            pg.updateDisplay()
            for event in pygame.event.get():
                 if event.type == pygame.QUIT: 
                     return
        
