######################################
# Import and initialize the librarys #
######################################
from code.api.core import os, log, screens


#################
# Setup logging #
#################
filename = os.path.basename(__file__).split('.')[0]
logger = log.get_logger(filename)
logger.info('Loading up {}...'.format(filename))


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
        if not 0 <= hero_r-1 <= 7: move_surface.up.switchState('Disabled', withDisplay=False)
        if not 0 <= hero_r+1 <= 7: move_surface.down.switchState('Disabled', withDisplay=False)
        if not 0 <= hero_c-1 <= 7: move_surface.left.switchState('Disabled', withDisplay=False)
        if not 0 <= hero_c+1 <= 7: move_surface.right.switchState('Disabled', withDisplay=False)

        screens.game.move.display()

    @staticmethod
    def Move(direction:str):
        pass

    @staticmethod
    def back():
        Grid = screens.game.map.grid.Grid

        # Get hero's position
        hero_pos = Grid.find('hero')

        # Unload move
        screens.game.move.unload()

        # Check if hero in town or open
        if Grid.tiles[hero_pos[0]][hero_pos[1]].hasSprite('town'): screens.game.in_town.display()
        else: screens.game.in_open.display()