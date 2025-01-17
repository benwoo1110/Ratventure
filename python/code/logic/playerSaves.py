######################################
# Import and initialize the librarys #
######################################
import json
from datetime import datetime
import glob
from code.api.core import os, log, screens
from code.api.data.Sound import sound
from code.logic.playerData import PlayerData
from code.logic.board import Board


#################
# Setup logging #
#################
filename = os.path.basename(__file__).split('.')[0]
logger = log.get_logger(filename)


##################
# Gameplay logic #
##################
class PlayerSaves:

    @staticmethod
    def get() -> list:
        # Get all save files
        savefiles = glob.glob('./appdata/saves/*.json')
        savefiles.sort(key=os.path.getmtime, reverse=True)

        return savefiles

    @staticmethod
    @log.method(logger) # Sample usage
    def showList(page:int = 1):
        # Unload first
        screens.saves.unload()

        # Load the background
        screens.saves.loadBackground()

        # Get the savefiles
        savefiles = PlayerSaves.get()

        # Set board paging
        page = Board.setPage(screen='saves', number_of_files=len(savefiles), page=page)
        
        # Set board next and back arrows
        Board.arrowsState('saves')

        # Load up board
        screens.saves.board.load(withItems='all', refresh=True)

        # No save files
        if len(savefiles) == 0: 
            screens.saves.board.delete_all.switchState('Disabled', True, False)
            screens.saves.display(withSurfaces=['board'])
            return

        # Enable delete all
        screens.saves.board.delete_all.switchState('', True, False)

        # Load up list
        for i in range(4):
            # Number of saves less than 4 page
            if (i + (page-1)*4) > len(savefiles)-1: break

            # Set list surface base on savefile data
            list_surface = screens.saves['list_{}'.format(i+1)]

            # Get savefile contents
            file_location = savefiles[(i + (page-1)*4)]
            with open(file_location, 'r') as savefile:
                raw_data = savefile.read()
            saveData = json.loads(raw_data)

            # Set nickname
            list_surface.file.nickname.setText(saveData['player']['nickname'], withDisplay=False)
            
            # Set time of save
            saved_time = datetime.fromtimestamp(saveData['time_saved'])
            list_surface.file.date.setText(saved_time.strftime('%d/%m/%Y %I:%M%p'), withDisplay=False)

            # Set file id
            list_surface.file.fileid = os.path.basename(file_location).split('.')[0]

            # load the list surface
            list_surface.load(withItems=['file'], refresh=True)

        # Display new list
        screens.saves.display(withSurfaces=['board'])

    @staticmethod
    def updateList(page:int):
        PlayerSaves.showList(int(Board.currentPage('saves')) + page)

    @staticmethod
    def playSaved(number:int):
        # Get the save file's UUID
        fileid = screens.saves['list_{}'.format(number)].file.fileid

        # Load the the game instance
        PlayerData.load(fileid)

    @staticmethod
    def deleteSaved(number:int):
        list_surface = screens.saves['list_{}'.format(number)]

        # get file to delete
        file_location = './appdata/saves/{}.json'.format(list_surface.file.fileid)
        
        # Delete the file
        try: os.remove(file_location)
        except Exception as e: logger.error(e, exc_info=True)
        else: logger.info('Deleted playerdata "{}"'.format(file_location))

        # Trash sound
        sound.trash.play()

        # Reload list view
        PlayerSaves.showList(int(Board.currentPage('saves')))

    @staticmethod
    def deleteAll():
        # Get all save files
        files = glob.glob('./appdata/saves/*.json')

        # Delete the file
        for savefile in files:
            try: os.remove(savefile)
            except Exception as e: logger.error(e, exc_info=True)

        # Trash sound
        sound.trash_all.play()
        
        logger.info('Deleted all saved playerdata.')