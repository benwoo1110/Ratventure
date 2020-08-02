######################################
# Import and initialize the librarys #
######################################
import json
from datetime import datetime
import glob
import math
from code.api.core import os, log, screens
from code.logic.playerData import playerData


#################
# Setup logging #
#################
filename = os.path.basename(__file__).split('.')[0]
logger = log.get_logger(filename)
logger.info('Loading up {}...'.format(filename))


##################
# Gameplay logic #
##################
class playerSaves:

    @staticmethod
    def get() -> list:
        # Get all save files
        savefiles = glob.glob('./appdata/saves/*.json')
        savefiles.sort(key=os.path.getmtime, reverse=True)

        return savefiles
    
    @staticmethod
    def currentPage():
        return int(screens.saves.board.page_text.pages.prefix)

    @staticmethod
    def arrowsState():
        page_text = screens.saves.board.page_text
        board = screens.saves.board

        # On first page, i.e. no back
        if page_text.pages.prefix == '1': board.page_back.switchState('Disabled')
        else: board.page_back.switchState('')

        # On last page, i.e. no next
        if page_text.pages.prefix == page_text.pages.suffix: board.page_next.switchState('Disabled')
        else: board.page_next.switchState('')

    @staticmethod
    def showList(page:int = 1):
        # Unload first
        screens.saves.unload()

        # Reload the background
        screens.saves.loadBackground()

        # Get the savefiles
        savefiles = playerSaves.get()

        # Calcuate pages
        page_per_screen = 4
        number_of_files = len(savefiles)
        number_of_pages = math.ceil(number_of_files / page_per_screen)

        # Fallback to last page
        if page > number_of_pages: page = number_of_pages

        # Set pages
        screens.saves.board.page_text.pages.setText(prefix=str(page), suffix=str(number_of_pages), withDisplay=False)

        # load the board
        screens.saves.board.load(withItems='all', refresh=True)

        # Load up list
        for i in range(4):
            # Number of saves less than 1 page
            if (i + (page-1)*4) > number_of_files-1: break

            # Set list surface base on savefile data
            list_surface = screens.saves['list_{}'.format(i+1)]

            # Get savefile contents
            file_location = savefiles[(i + (page-1)*4)]
            with open(file_location, 'r') as savefile:
                raw_data = savefile.read()
            saveData = json.loads(raw_data)

            # Set nickname
            list_surface.file.nickname.setText(saveData['nickname'], withDisplay=False)
            
            # Set time of save
            save_time = datetime.fromtimestamp(os.path.getctime(savefiles[(i + (page-1)*4)]))
            list_surface.file.date.setText(save_time.strftime('%-d/%-m/%Y %-I:%M%p'), withDisplay=False)

            # Set file id
            list_surface.file.fileid = os.path.basename(file_location).split('.')[0]

            # load the list surface
            list_surface.load(withItems=['file'], refresh=True)

        playerSaves.arrowsState()

    @staticmethod
    def updateList(page:int):
        playerSaves.showList(int(playerSaves.currentPage()) + page)

    @staticmethod
    def playSaved(number:int):
        list_surface = screens.saves['list_{}'.format(number)]

        # Load the the game instance
        playerData.load(fileid=list_surface.file.fileid)

        # Switch to game screen
        screens.changeStack(type='load', screen='game')

    @staticmethod
    def deleteSaved(number:int):
        list_surface = screens.saves['list_{}'.format(number)]

        # get file to delete
        file_location = './appdata/saves/{}.json'.format(list_surface.file.fileid)
        
        # Delete the file
        try: os.remove(file_location)
        except Exception as e: logger.error(e, exc_info=True)
        else: logger.info('Deleted playerdata "{}"'.format(file_location))

        # Reload list view
        playerSaves.showList(int(playerSaves.currentPage()))