######################################
# Import and initialize the librarys #
######################################
import json
import uuid
import time
from code.api.core import os, log, screens, coreFunc
from code.logic.stats import stats
from code.logic.power import power
from code.logic.hero import hero
from code.logic.story import story


#################
# Setup logging #
#################
filename = os.path.basename(__file__).split('.')[0]
logger = log.get_logger(filename)
logger.info('Loading up {}...'.format(filename))


# Ensure that saves folder is created
filepath = './appdata/saves/'
if not os.path.isdir(filepath):
    # Create logs directory
    try: os.mkdir(filepath)
    except Exception as e: logger.error(e, exc_info=True)
    else: logger.info('Created {} directory'.format(filepath))


##################
# Gameplay logic #
##################
class player(coreFunc):
    def __init__(self, nickname:str = None, fileid:str = None, difficulty:str = None):
        self.nickname = nickname
        self.fileid = fileid
        self.difficulty = difficulty


class playerData:
    currentPlayer = player()

    @staticmethod
    def new():
        Grid = screens.game.map.grid.Grid

        # Unload previous state
        screens.game.unload()

        # reset currentPlayer 
        playerData.currentPlayer = player (
            nickname=screens.new_game.options.nickname.text.text,
            difficulty=screens.new_game.options.difficulty.level.text
            )
        
        # Create grid
        Grid.clear()

        # Set default hero, town and king
        Grid.tiles[0][0].sprites = ['town', 'hero']
        Grid.tiles[7][7].sprites = ['king']

        # Generate random towns 
        Grid.randomiseTowns()

        # Create new stats
        hero.resetStats()

        # Calculate orb postion
        power.setLocation()

        # Set if player can sense for orb
        power.canSense()

        # Set starting story
        story.in_town.display()

        # Load screen
        screens.game.map.load(withItems=['grid'])
        screens.game.info.load(withItems='all')
        screens.game.in_town.load()

        # Switch to game screen
        screens.changeStack(type='load', screen='game') 

        logger.info('Created new playerdata.')

    @staticmethod
    def load(fileid:str):
        Grid = screens.game.map.grid.Grid

        # Unload previous state
        screens.game.unload()
     
        # Get saved file data
        save_location = './appdata/saves/{}.json'.format(fileid)

        try:
            with open(save_location, 'r') as savefile:
                raw_data = savefile.read()
        
        except Exception as e: 
            logger.error(e, exc_info=True)
            return

        # Check that user did not edit save file
        checkid = str(uuid.uuid3(uuid.NAMESPACE_URL, raw_data))
        if fileid != checkid: 
            raise Exception('UUID mismatch for savefile "{}" Did you edit the file?'.format(save_location))

        savedData = json.loads(raw_data)

        # Store loaded player
        playerData.currentPlayer = player (fileid=fileid, **savedData['player'])

        # Map
        Grid.generate(savedData['grid'])

        # Load orb location
        power.row, power.column = savedData['orb']

        # Load stats
        hero.setStats(savedData['stats'])

        # Set if player can sense for orb
        power.canSense()

        # Set story saved
        story.setCurrent(savedData['story'])

        # Check if player in town
        if Grid.heroInTown(): screens.game.in_town.load()
        else: screens.game.in_open.load(withItems=['sense_orb'])

        # Display screen
        screens.game.map.load(withItems=['grid'])
        screens.game.info.load(withItems='all')

        logger.info('Loaded playerdata from "{}"'.format(save_location))

    @staticmethod
    def save():
        # Delete old save file if any
        playerData.delete()

        # Init dictionary to save
        savedData = {}

        # Save player
        player_data = playerData.currentPlayer.__dict__.copy()
        del player_data['fileid']

        savedData['player'] = player_data

        # Store save time
        savedData['time_saved'] = time.time()

        # Save map
        Grid = screens.game.map.grid.Grid
        savedData['grid'] = []

        for tile_row in Grid.tiles:
            savedData['grid'].append([])
            for tile in tile_row:
                savedData['grid'][-1].append(tile.sprites)

        # Save orb location
        savedData['orb'] = [power.row, power.column]

        # Stats
        savedData['stats'] = hero.getStats()

        # Save story
        savedData['story'] = story.getCurrent()

        # Generate json text data
        json_data = json.dumps(savedData)

        # Generate UUID
        fileid = str(uuid.uuid3(uuid.NAMESPACE_URL, json_data))

        # Save to file
        save_location = './appdata/saves/{}.json'.format(fileid)
        with open(save_location, 'w') as savefile:
            savefile.write(json_data)

        # Set new player fileid
        playerData.currentPlayer.fileid = fileid

        logger.info('Saved new playerdata to "{}"'.format(save_location))

    @staticmethod
    def delete():
        if playerData.currentPlayer.fileid != None: 
            # Get file location    
            file_location = './appdata/saves/{}.json'.format(playerData.currentPlayer.fileid)

            # Delete the file
            try: os.remove(file_location)
            except Exception as e: logger.error(e, exc_info=True)
            else: logger.info('Deleted old playerdata "{}"'.format(file_location))

        else: logger.info('Player does not have a save file.')