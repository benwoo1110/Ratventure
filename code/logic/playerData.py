######################################
# Import and initialize the librarys #
######################################
import json
import uuid
import time
from code.api.core import os, log, screens, pg, pygame
from code.api.actions import Alert
from code.api.data.Sound import Sound
from code.logic.player import player
from code.logic.orb import orb
from code.logic.story import story
from code.logic.difficulty import difficulty
from code.logic.store import store


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


class playerData:

    @staticmethod
    def new():
        Grid = screens.game.map.grid.Grid

        # Check if nickname is valid
        if not screens.new_game.options.nickname.text.validateText(): return

        # Unload previous states
        screens.game.unload()

        # reset player
        player.reset()

        # Set difficulty settings
        difficulty.set()

        # Set grid to default hero, town and king
        Grid.clear()
        Grid.tiles[0][0].sprites = ['town', 'hero']
        Grid.tiles[7][7].sprites = ['king']

        # Generate random towns
        town_settings = difficulty.get()
        Grid.randomiseTowns(town_settings['town_number'], town_settings['town_space'])

        # Calculate orb postion
        orb.setLocation()
        orb.canSense()

        # Set up store
        store.setWeapons()

        # Set starting story
        story.in_town.display()

        # Set player stats for game screen
        player.stats.display('day', screens.game.info.days)
        player.stats.display('damage', screens.game.info.stats)
        player.stats.display('defence', screens.game.info.stats)
        player.stats.display('health', screens.game.info.stats)
        player.stats.display('elixir', screens.game.info.stats)

        # Reset stats update
        screens.game.info.hero.stats.setText('', withDisplay=False)

        # Load screen
        screens.game.map.load(withItems=['grid'])
        screens.game.info.load(withItems='all')
        screens.game.in_town.load()

        # Switch to game screen
        screens.changeStack(type='load', screen='game')

        # Play game background music
        pygame.mixer.fadeout(600)
        Sound.game_background.play(loops=-1, withVolume=0.12, fadetime=10000)

        logger.info('Created new playerdata.')

    @staticmethod
    def load(fileid:str):
        Grid = screens.game.map.grid.Grid

        # Unload previous state
        screens.game.unload()
     
        # Get saved file data
        save_location = './appdata/saves/{}.json'.format(fileid)
        try:
            with open(save_location, 'r') as savefile: raw_data = savefile.read()
        
        except Exception as e: 
            logger.error(e, exc_info=True)
            return

        # Check that user did not edit save file
        checkid = str(uuid.uuid3(uuid.NAMESPACE_URL, raw_data))
        if fileid != checkid: 
            # Error sound
            Sound.error.play()

            # Tell user issue with file
            Alert (
                type='notify', 
                title='Error',
                content='UUID mismatch for savefile. Did you edit the file?',
            ).do()

            logger.error('UUID mismatch for savefile {}'.format(save_location))
            return

        # Get the data
        savedData = json.loads(raw_data)

        # Loaded stored player
        savedData['player']['fileid'] = fileid
        player.load(savedData['player'])

        # Set player stats for game screen
        player.stats.display('day', screens.game.info.days)
        player.stats.display('damage', screens.game.info.stats)
        player.stats.display('defence', screens.game.info.stats)
        player.stats.display('health', screens.game.info.stats)
        player.stats.display('elixir', screens.game.info.stats)

        # Set difficulty settings
        difficulty.set(player.difficulty)

        # Set weapons
        store.setWeapons()

        # Map
        Grid.generate(savedData['grid'])

        # Set if player can sense for orb
        orb.canSense()

        # Set story saved
        story.setCurrent(savedData['story'])

        # Check if player in town
        if Grid.heroInTown(): screens.game.in_town.load()
        else: screens.game.in_open.load(withItems=['sense_orb'])

        # Load game screen
        screens.game.map.load(withItems=['grid'])
        screens.game.info.load(withItems='all')

        # Switch to game screen
        screens.changeStack(type='load', screen='game')

        # Play game background music
        pygame.mixer.fadeout(600)
        Sound.game_background.play(loops=-1, withVolume=0.12, fadetime=10000)

        logger.info('Loaded playerdata from "{}"'.format(save_location))

    @staticmethod
    def save():
        # Delete old save file if any
        playerData.delete()

        # Init dictionary to save
        savedData = dict()

        # Save player
        savedData['player'] = player.get()

        # Store save time
        savedData['time_saved'] = time.time()

        # Save map
        savedData['grid'] = screens.game.map.grid.Grid.get()

        # Save story
        savedData['story'] = story.getCurrent()

        # Generate json text data
        json_data = json.dumps(savedData)

        # Generate and set UUID
        fileid = str(uuid.uuid3(uuid.NAMESPACE_URL, json_data))
        player.fileid = fileid

        # Save to file
        pg.saveJson('./appdata/saves/{}.json'.format(fileid), savedData)

        # Cool beep
        Sound.saved.play(withVolume=0.5)

        # Tell user game is saved
        Alert(type='notify', title='Game Saved', content='You have saved the game.').do()

    @staticmethod
    def delete():
        if player.fileid != None: 
            # Get file location    
            file_location = './appdata/saves/{}.json'.format(player.fileid)

            # Delete the file
            try: os.remove(file_location)
            except FileNotFoundError: logger.warning('Looks like {} is already deleted!'.format(player.fileid))
            except Exception as e: logger.error(e, exc_info=True)
            else: logger.info('Deleted old playerdata at {}'.format(file_location))

        else: logger.info('Player does not have a save file.')