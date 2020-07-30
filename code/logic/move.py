######################################
# Import and initialize the librarys #
######################################
from code.api.core import os, log, screens
from code.logic.stats import stats


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
    def initSurface():
        move_surface = screens.game.move
        Grid = screens.game.map.grid.Grid
        
        # Get hero's position
        hero_r, hero_c = Grid.find('hero')

        # Check if hero in town or open
        if Grid.tiles[hero_r][hero_c].hasSprite('town'): screens.game.in_town.unload()
        else: screens.game.in_open.unload()

        # Disable arrows for impossible directions
        if not 0 <= hero_r-1 <= 7: move_surface.up.switchState('Disabled', withLoad=False)
        else: move_surface.up.switchState('', withLoad=False)

        if not 0 <= hero_r+1 <= 7: move_surface.down.switchState('Disabled', withLoad=False)
        else: move_surface.down.switchState('', withLoad=False)

        if not 0 <= hero_c-1 <= 7: move_surface.left.switchState('Disabled', withLoad=False)
        else: move_surface.left.switchState('', withLoad=False)

        if not 0 <= hero_c+1 <= 7: move_surface.right.switchState('Disabled', withLoad=False)
        else: move_surface.right.switchState('', withLoad=False)

        # Display to screen
        screens.game.move.display(withLoad=True)

    @staticmethod
    def Move(direction:str):
        Grid = screens.game.map.grid.Grid

        # Get hero's position
        hero_r, hero_c = Grid.find('hero')

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
        screens.game.map.display(withLoad=True)

        # Add a day
        stats.day.update()

        # Go make to selection menu
        move.back()

    @staticmethod
    def back():
        Grid = screens.game.map.grid.Grid

        # Unload move
        screens.game.move.unload()

        # Check if hero in town or open
        if Grid.heroInTown(): screens.game.in_town.display()
        else: screens.game.in_open.display()