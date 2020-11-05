######################################
# Import and initialize the librarys #
######################################
import math
from code.api.core import os, log, screens


#################
# Setup logging #
#################
filename = os.path.basename(__file__).split('.')[0]
logger = log.get_logger(filename)


##################
# Gameplay logic #
##################
class Board:

    @staticmethod
    def currentPage(screen:str):
        return int(screens[screen].board.page_text.pages.prefix)

    @staticmethod
    def maxPage(screen:str):
        return int(screens[screen].board.page_text.pages.suffix)

    @staticmethod
    def arrowsState(screen:str):
        page_text = screens[screen].board.page_text
        board_surface = screens[screen].board

        # On first page, i.e. no back
        if int(page_text.pages.prefix) <= 1: board_surface.page_back.switchState('Disabled', False)
        else: board_surface.page_back.switchState('', False)

        # On last page, i.e. no next
        if int(page_text.pages.prefix) >= int(page_text.pages.suffix): board_surface.page_next.switchState('Disabled', False)
        else: board_surface.page_next.switchState('', False)

    @staticmethod
    def setPage(screen:str, number_of_files:int, page:int = 1, page_per_screen:int = 4):
        # Calcuate pages
        number_of_pages = math.ceil(number_of_files / page_per_screen)

        # Set pages
        # Fallback to last page
        if page > number_of_pages: page = number_of_pages
        # Fallback to first page
        elif page < 1: page = 1
        
        # Set pages text
        screens[screen].board.page_text.pages.setText(prefix=str(page), suffix=str(number_of_pages), withDisplay=False)

        return page