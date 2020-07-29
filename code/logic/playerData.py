######################################
# Import and initialize the librarys #
######################################
from random import randint
import json
from code.api.core import os, log, coreFunc, screens
from code.logic.stats import stats


#################
# Setup logging #
#################
filename = os.path.basename(__file__).split('.')[0]
logger = log.get_logger(filename)
logger.info('Loading up {}...'.format(filename))


# Ensure that saves folder is created
if not os.path.isdir('./appdata/saves'):
    # Create logs directory
    try: os.mkdir('./appdata/saves')
    except: traceback.print_stack()
    else: print("Created ./appdata/saves directory")


class playerData(coreFunc):
    
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
                    if 0 <= row+r <= 7 and 0 <= column+c <= 7 and (r, c) != (0, 0):
                        if Grid.tiles[row+r][column+c].hasSprite():
                            can_place = False 
                            break
                if not can_place: break
            
            # Place down the town if checks pass
            if can_place: 
                Grid.tiles[row][column].sprites = ['town']
                town_placed += 1

        # Create stats
        stats.damage.set('info', 'stats', 2, 4, False)
        stats.defence.set('info', 'stats', 1, False)
        stats.health.set('info', 'stats', 20, 20, False)
        stats.power.remove('info', 'stats', False)

        # Calculate orb postion
        while True:
            row = randint(0, 7)
            column = randint(0, 7)

            # Ensure that pos is not a town or king
            if  (row >=4 or column >= 4) and (not Grid.tiles[row][column].hasSprite()):
                # Save to grid for now
                Grid.tiles[row][column].sprites = ['orb']
                break

        # Display screen
        screens.game.display(surfaces=['map', 'info', 'in_town'], withLoad=True)

    @staticmethod
    def load():
        # Get saved file
        save_location = './appdata/saves/test.json'
        with open(save_location, 'r') as savefile:
            raw_data = savefile.read()
        
        savedData = json.loads(raw_data)

        # Map
        screens.game.map.grid.Grid.generate(savedData['grid'])

        # Stats
        stats.damage.set('info', 'stats', *savedData['stats']['damage'], False)
        stats.defence.set('info', 'stats', savedData['stats']['defence'], False)
        stats.health.set('info', 'stats', *savedData['stats']['health'], False)
        stats.power.set('info', 'stats', savedData['stats']['power'], False)

        # Display screen
        screens.game.display(surfaces=['map', 'info', 'in_town'], withLoad=True)

        logger.info('Loaded playerdata from "{}"'.format(save_location))

    @staticmethod
    def save():
        savedData = {}

        # Map
        Grid = screens.game.map.grid.Grid
        savedData['grid'] = []

        for tile_row in Grid.tiles:
            savedData['grid'].append([])
            for tile in tile_row:
                savedData['grid'][-1].append(tile.sprites)

        # Stats
        savedData['stats'] = {}

        savedData['stats']['damage'] = stats.damage.get('info', 'stats')
        savedData['stats']['defence'] = stats.defence.get('info', 'stats')
        savedData['stats']['health'] = stats.health.get('info', 'stats')
        savedData['stats']['power'] = stats.power.hasOrb('info', 'stats')

        # Save to file
        save_location = './appdata/saves/test.json'
        with open(save_location, 'w') as savefile:
            savefile.write(json.dumps(savedData))

        logger.info('Saved playerdata to "{}"'.format(save_location)) 