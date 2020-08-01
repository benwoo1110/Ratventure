######################################
# Import and initialize the librarys #
######################################
from random import randint
import json
from code.api.core import os, log, coreFunc, screens, traceback
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
        stats.day.set(1, False)
        stats.damage.set('info', 'stats', 2, 4, False)
        stats.defence.set('info', 'stats', 1, False)
        stats.health.set('info', 'stats', 10, 20, False)
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

        # Display screen
        screens.game.map.load(withItems=['grid'])
        screens.game.info.load(withItems='all')
        screens.game.in_town.load()
        screens.game.display()

        logger.info('Created new playdata.')

    @staticmethod
    def load():
        Grid = screens.game.map.grid.Grid
        # Get saved file
        save_location = './appdata/saves/test.json'
        with open(save_location, 'r') as savefile:
            raw_data = savefile.read()
        
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
        screens.game.display()

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

        # Save to file
        save_location = './appdata/saves/{}.json'.format(nickname)
        with open(save_location, 'w') as savefile:
            savefile.write(json.dumps(savedData))

        logger.info('Saved playerdata to "{}"'.format(save_location)) 