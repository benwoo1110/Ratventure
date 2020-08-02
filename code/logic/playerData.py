######################################
# Import and initialize the librarys #
######################################
import json
import uuid
from random import randint
from code.api.core import os, log, screens, traceback
from code.logic.stats import stats
from code.logic.power import power


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
    except: traceback.print_stack()
    else: print('Created {} directory'.format(filepath))


##################
# Gameplay logic #
##################
class playerData:
    
    @staticmethod
    def new():
        # Create grid
        Grid = screens.game.map.grid.Grid

        Grid.clear()

        # Set default hero, town and king
        Grid.tiles[0][0].sprites = ['town', 'hero']
        Grid.tiles[7][7].sprites = ['king']

        # Generate random towns 
        town_placed = 0
        while town_placed < 4:
            row = randint(0, 7)
            column = randint(0, 7)

            # Ensure that pos isnt a town or at king's location
            if Grid.tiles[row][column].hasSprite('town'): continue

            # Check if town in within 3 pos
            can_place = True
            for c in range(-2, 3):
                for r in range(-(2-abs(c)), 2-abs(c)+1):
                    # Ensure there is such a tile and is not itself and not at king location
                    if 0 <= row+r <= 7 and 0 <= column+c <= 7 and (r, c) != (7, 7):
                        if Grid.tiles[row+r][column+c].hasSprite():
                            can_place = False 
                            break
                if not can_place: break
            
            # Place down the town if checks pass
            if can_place: 
                Grid.tiles[row][column].sprites.append('town')
                town_placed += 1

        # Create stats
        stats.day.set(1, False)
        stats.damage.set('info', 'stats', 2, 4, False)
        stats.defence.set('info', 'stats', 1, False)
        stats.health.set('info', 'stats', 20, 20, False)
        stats.power.set(False, False)

        # Calculate orb postion
        while True:
            row = randint(0, 7)
            column = randint(0, 7)

            # Ensure that pos is not a town or king
            if  (row >=4 or column >= 4) and (not Grid.tiles[row][column].hasSprite()):
                # Save orb pos
                power.row, power.column = row, column
                break

        # Set if player can sense for orb
        power.sense()

        # Load screen
        screens.game.map.load(withItems=['grid'])
        screens.game.info.load(withItems='all')
        screens.game.in_town.load()

        # Switch to game screen
        screens.changeStack(type='load', screen='game') 

        logger.info('Created new playdata.')

    @staticmethod
    def load(fileid:str):
        Grid = screens.game.map.grid.Grid
     
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

        # Map
        Grid.generate(savedData['grid'])

        # Load orb location
        power.row, power.column = savedData['orb']

        # Stats
        stats.day.set(savedData['stats']['day'], False)
        stats.damage.set('info', 'stats', *savedData['stats']['damage'], False)
        stats.defence.set('info', 'stats', savedData['stats']['defence'], False)
        stats.health.set('info', 'stats', *savedData['stats']['health'], False)
        stats.power.set(savedData['stats']['power'], False)

        # Set if player can sense for orb
        power.sense()

        # Check if player in town
        if Grid.heroInTown(): screens.game.in_town.load()
        else: screens.game.in_open.load(withItems=['sense_orb'])

        # Display screen
        screens.game.map.load(withItems=['grid'])
        screens.game.info.load(withItems='all')

        logger.info('Loaded playerdata from "{}"'.format(save_location))

    @staticmethod
    def save():
        savedData = {}

        # Save nickname
        nickname = screens.new_game.options.nickname.text.text
        savedData['nickname'] = nickname

        # Map
        Grid = screens.game.map.grid.Grid
        savedData['grid'] = []

        for tile_row in Grid.tiles:
            savedData['grid'].append([])
            for tile in tile_row:
                savedData['grid'][-1].append(tile.sprites)

        # Save orb location
        savedData['orb'] = [power.row, power.column]

        # Stats
        savedData['stats'] = {}

        savedData['stats']['day'] = stats.day.get()
        savedData['stats']['damage'] = stats.damage.get('info', 'stats')
        savedData['stats']['defence'] = stats.defence.get('info', 'stats')
        savedData['stats']['health'] = stats.health.get('info', 'stats')
        savedData['stats']['power'] = stats.power.hasOrb()

        # Generate json text data
        json_data = json.dumps(savedData)

        # Generate UUID
        fileid = uuid.uuid3(uuid.NAMESPACE_URL, json_data)

        # Save to file
        save_location = './appdata/saves/{}.json'.format(fileid)
        with open(save_location, 'w') as savefile:
            savefile.write(json_data)

        logger.info('Saved playerdata to "{}"'.format(save_location))