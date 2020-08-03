######################################
# Import and initialize the librarys #
######################################
import json
import time
import uuid
from code.api.core import os, log, screens
from code.logic.playerData import playerData
from code.logic.stats import stats
from code.logic.board import board


#################
# Setup logging #
#################
filename = os.path.basename(__file__).split('.')[0]
logger = log.get_logger(filename)
logger.info('Loading up {}...'.format(filename))


# Ensure that leaderboard file is created
filepath = './appdata/leaderboard.json'
if not os.path.isfile(filepath):
    # Create empty leaderboard file
    try:
        with open(filepath, 'w') as leaderboardfile:
            leaderboardfile.write(json.dumps(dict()))

    except Exception as e: logger.error(e, exc_info=True)
    else: logger.info('Created {} file'.format(filepath))


##################
# Gameplay logic #
##################
class rank:
    # Get leaderboard data
    try:
        with open(filepath, 'r') as leaderboardfile:
            rankData = json.loads(leaderboardfile.read())

    except Exception as e: logger.error(e, exc_info=True)

    @staticmethod
    def check():
        # Ensure that leaderboard data is not tempered with
        checkedData = rank.rankData.copy()
        missmatch = False

        for rankid, data in rank.rankData.items():
            # Generate json text data
            json_data = json.dumps(data)

            # Check UUID match
            checkid = str(uuid.uuid3(uuid.NAMESPACE_URL, json_data))
            if checkid != rankid: 
                del checkedData[rankid]
                missmatch = True
                logger.warn('Leaderboard data with rankid {} is tempered. Removing...'.format(rankid))

        # Reload data without those tempered with
        if missmatch:
            rank.rankData = checkedData
            rank.save()

    @staticmethod
    def save():
        # Create empty leaderboard file
        try:
            with open(filepath, 'w') as leaderboardfile:
                leaderboardfile.write(json.dumps(rank.rankData, indent=4))

        except Exception as e: logger.error(e, exc_info=True)
        else: logger.info('Save leaderboard data to {}'.format(filepath))

    @staticmethod
    def add() -> int:
        # Store data is dict
        win_data = {
            'nickname': playerData.currentPlayer.nickname,
            'win_time': time.time(),
            'days': stats.day.get()
            } 
        
        # Generate json text data
        json_data = json.dumps(win_data)

        # Generate UUID based on win data
        rankid = str(uuid.uuid3(uuid.NAMESPACE_URL, json_data))

        # Add to leaderboard data
        rank.rankData[rankid] = win_data

        # Sort the rank based on days
        rank.rankData = dict(sorted(rank.rankData.items(), key=lambda x: x[1]['days']))

        rank.save()

    @staticmethod
    def getPos() -> int:
        for postion, data in enumerate(rank.rankData.values(), 1):
            # Found postion in data
            if data['nickname'] == playerData.currentPlayer.nickname and data['days'] == stats.day.get():
                return postion

        # Not found
        return -1

    @staticmethod
    def showList(page:int = 1):
        # Unload first
        screens.leaderboard.unload()

        # Load the background
        screens.leaderboard.loadBackground()

        # Set board paging
        page = board.setPage(screen='leaderboard', number_of_files=len(rank.rankData), page=page)

        # Set board next and back arrows
        board.arrowsState('leaderboard')

        # Load up board
        screens.leaderboard.board.load(withItems='all', refresh=True)

        # No leaderboard
        if len(rank.rankData) == 0: 
            screens.leaderboard.display()
            return

        # Get data
        list_data = list(rank.rankData.values())

        # Load up list
        for i in range(4):
            current_postion = (i + (page-1)*4)
            # Number of leaderboard less than 4 page
            if current_postion > len(rank.rankData)-1: break

            # Set list surface base on savefile data
            list_surface = screens.leaderboard['list_{}'.format(i+1)]

            # Set state based on rank
            if current_postion+1 <= 3: list_surface.rank.switchState('Special', False)
            else: list_surface.rank.switchState('', False)

            # Update data
            list_surface.rank.postion.setText(str(current_postion+1), withDisplay=False)
            list_surface.rank.nickname.setText(str(list_data[current_postion]['nickname']), withDisplay=False)
            list_surface.rank.days.setText(str(list_data[current_postion]['days']), withDisplay=False)
            
            # load the list surface
            list_surface.load(withItems=['rank'], refresh=True)

        # Display new list
        screens.leaderboard.display()


    @staticmethod
    def updateList(page:int):
        rank.showList(int(board.currentPage('leaderboard')) + page)

# Check ranks for tempered in startup
rank.check()