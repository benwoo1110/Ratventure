######################################
# Import and initialize the librarys #
######################################
import json
import time
import uuid
from code.api.core import os, log, screens, pg
from code.logic.player import player
from code.logic.board import board


#################
# Setup logging #
#################
filename = os.path.basename(__file__).split('.')[0]
logger = log.get_logger(filename)
logger.info('Loading up {}...'.format(filename))


# Location of leaderboard data
filepath = './appdata/leaderboard.json'


##################
# Gameplay logic #
##################
class playerRank:
    # Get leaderboard data
    rankData = pg.loadJson(filepath, dict())

    @staticmethod
    def check():
        # Ensure that leaderboard data is not tempered with
        checkedData = playerRank.rankData.copy()
        missmatch = False

        for rankid, data in playerRank.rankData.items():
            # Generate json text data
            json_data = json.dumps(data)

            # Check UUID match
            checkid = str(uuid.uuid3(uuid.NAMESPACE_URL, json_data))
            if checkid != rankid: 
                del checkedData[rankid]
                missmatch = True
                logger.warning('Leaderboard data with rankid {} is tempered. Removing...'.format(rankid))

        # Reload data without those tempered with
        if missmatch:
            playerRank.rankData = checkedData
            pg.saveJson(filepath, playerRank.rankData)

    @staticmethod
    def add() -> int:
        # Store data is dict
        win_data = {
            'nickname': player.nickname,
            'win_time': time.time(),
            'difficulty': player.difficulty,
            'days': player.stats.day
            } 
        
        # Generate json text data
        json_data = json.dumps(win_data)

        # Generate UUID based on win data
        rankid = str(uuid.uuid3(uuid.NAMESPACE_URL, json_data))

        # Add to leaderboard data
        playerRank.rankData[rankid] = win_data

        # Sort the rank based on days
        playerRank.rankData = dict(sorted(playerRank.rankData.items(), key=lambda x: x[1]['days']))

        # playerRank.save()
        # Save updated back to file
        pg.saveJson(filepath, playerRank.rankData)

        return rankid

    @staticmethod
    def rename(newname, rankid) -> str:
        # Remove the rank with old name
        update_rank = playerRank.rankData[rankid].copy()
        del playerRank.rankData[rankid]

        # Change name and add back rank
        update_rank['nickname'] = newname
        player.nickname = newname
        new_rankid = str(uuid.uuid3(uuid.NAMESPACE_URL, json.dumps(update_rank)))
        playerRank.rankData[new_rankid] = update_rank

        # Sort the rank based on days
        playerRank.rankData = dict(sorted(playerRank.rankData.items(), key=lambda x: x[1]['days']))

        # Save the updated nickname data
        pg.saveJson(filepath, playerRank.rankData)

        return new_rankid

    @staticmethod
    def getPos() -> int:
        for postion, data in enumerate(playerRank.rankData.values(), 1):
            # Found postion in data
            if data['nickname'] == player.nickname and data['days'] == player.stats.day:
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
        page = board.setPage(screen='leaderboard', number_of_files=len(playerRank.rankData), page=page)

        # Set board next and back arrows
        board.arrowsState('leaderboard')

        # Load up board
        screens.leaderboard.board.load(withItems='all', refresh=True)

        # No leaderboard
        if len(playerRank.rankData) == 0: 
            screens.leaderboard.display()
            return

        # Get data
        list_data = list(playerRank.rankData.values())

        # Load up list
        for i in range(4):
            current_postion = (i + (page-1)*4)
            # Number of leaderboard less than 4 page
            if current_postion > len(playerRank.rankData)-1: break

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
        playerRank.showList(int(board.currentPage('leaderboard')) + page)

# Check ranks for tempered in startup
playerRank.check()