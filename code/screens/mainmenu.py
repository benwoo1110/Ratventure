######################################
# Import and initialize the librarys #
######################################
from code.api.core import pg, pygame
from code.api.objects import screen


mainmenu_screen = screen (
    name = 'mainmenu',
)


class mainmenu:

    def run():
        mainmenu_screen.display()

        

        while True:
            pg.updateDisplay()
            for event in pygame.event.get():
                 if event.type == pygame.QUIT: 
                     return
        
