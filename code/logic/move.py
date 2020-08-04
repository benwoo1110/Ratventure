######################################
# Import and initialize the librarys #
######################################
from code.api.core import os, log, screens
from code.logic.stats import stats
from code.logic.attack import attack
from code.logic.story import story


#################
# Setup logging #
#################
filename = os.path.basename(__file__).split('.')[0]
logger = log.get_logger(filename)
logger.info('Loading up {}...'.format(filename))


##################
# Gameplay logic #
##################
class move:

    @staticmethod
    def checkDirection():
        Grid = screens.game.map.grid.Grid
        move_surface = screens.game.move

        # Get hero's position
        hero_r, hero_c = Grid.find('hero')
        
        # up
        if not 0 <= hero_r-1 <= 7: move_surface.up.switchState('Disabled', withDisplay=False)
        else: move_surface.up.switchState('', withDisplay=False)
        
        # down
        if not 0 <= hero_r+1 <= 7: move_surface.down.switchState('Disabled', withDisplay=False)
        else: move_surface.down.switchState('', withDisplay=False)
        
        # left
        if not 0 <= hero_c-1 <= 7: move_surface.left.switchState('Disabled', withDisplay=False)
        else: move_surface.left.switchState('', withDisplay=False)
        
        # right
        if not 0 <= hero_c+1 <= 7: move_surface.right.switchState('Disabled', withDisplay=False)
        else: move_surface.right.switchState('', withDisplay=False)
    
    @staticmethod
    def initSurface():
        Grid = screens.game.map.grid.Grid

        # Check if hero in town or open
        if Grid.heroInTown(): screens.game.in_town.unload()
        else: screens.game.in_open.unload()

        # Disable arrows for impossible directions
        move.checkDirection()

        # Display to screen
        screens.game.move.display()

    @staticmethod
    def Move(direction:str):
        Grid = screens.game.map.grid.Grid

        # Get hero's position
        hero_r, hero_c = Grid.find('hero')

        # Check for enemy to remove
        for enemy in attack.enemies:
            if enemy != 'king' and enemy in Grid.tiles[hero_r][hero_c].sprites:
                Grid.tiles[hero_r][hero_c].sprites.remove(enemy)

        # Remove hero from current location
        Grid.tiles[hero_r][hero_c].sprites.remove('hero')

        # Change location
        if direction == 'up': hero_r -= 1
        elif direction == 'down': hero_r += 1
        elif direction == 'left': hero_c -= 1
        elif direction == 'right': hero_c += 1

        # Add hero to new location
        Grid.tiles[hero_r][hero_c].sprites.append('hero')

        # Update map
        screens.game.map.display(withItems=['grid'], refresh=True)

        # Add a day
        stats.day.update()

        # Check for attack
        if attack.haveEnemy(): 
            # Unload move
            screens.game.move.unload()
            return

        # Update story
        if Grid.heroInTown(): story.in_town.display()
        else: story.in_open.display()

        # Disable arrows for impossible directions
        move.checkDirection()
        screens.game.move.display(withItems=['up', 'down', 'left', 'right'], refresh=True)

    @staticmethod
    def back():
        Grid = screens.game.map.grid.Grid

        # Unload move
        screens.game.move.unload()

        # Check if hero in town or open
        if Grid.heroInTown(): screens.game.in_town.display()
        else: screens.game.in_open.display()