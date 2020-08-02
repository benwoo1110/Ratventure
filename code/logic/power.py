######################################
# Import and initialize the librarys #
######################################
from code.api.core import os, log, screens
from code.logic.stats import stats
from code.logic.attack import attack


#################
# Setup logging #
#################
filename = os.path.basename(__file__).split('.')[0]
logger = log.get_logger(filename)
logger.info('Loading up {}...'.format(filename))


##################
# Gameplay logic #
##################
class power:
    row = -1
    column = -1

    @staticmethod
    def sense():
        if stats.power.hasOrb(): screens.game.in_open.sense_orb.switchState('Disabled', False)
        else: screens.game.in_open.sense_orb.switchState('', False)

    @staticmethod
    def initSurface():
        Grid = screens.game.map.grid.Grid
        # Unload previous selection screen
        screens.game.in_open.unload()

        # Check if hero is at orb location
        hero_r, hero_c = Grid.find('hero')

        # Orb is found
        if hero_r == power.row and hero_c == power.column:
            # Show orb in map
            Grid.tiles[power.row][power.column].sprites.insert(0, 'orb')

            screens.game.map.load(withItems=['grid'], refresh=True)
            screens.game.display(withSurfaces=['found_orb'])

        # Orb not found
        else:
            # Get direction
            direction = ''

            if power.row > hero_r: direction += 'south'
            elif power.row < hero_r: direction += 'north'

            if power.column > hero_c: direction += 'east'
            elif power.column < hero_c: direction += 'west'

            direction = direction.capitalize()

            # Set compass direction
            screens.game.no_orb.compass.switchState(direction, False)

            # Load screen
            screens.game.no_orb.display(withItems=['compass'], refresh=True)

        # Add a day
        stats.day.update()

    @staticmethod
    def take():
        Grid = screens.game.map.grid.Grid

        # Update stats upon taking orb
        stats.damage.update('info', 'stats', 5, 5, False)
        stats.defence.update('info', 'stats', 5)
        stats.power.take()

        # Disable sensing orb
        screens.game.in_open.sense_orb.switchState('Disabled', withDisplay=False)

        # Remove orb from map
        Grid.tiles[power.row][power.column].sprites.remove('orb')
        screens.game.map.display(withItems=['grid'], refresh=True)

        # Return to selection menu
        power.back()
    
    @staticmethod
    def back():
        # Unload orb screen
        if stats.power.hasOrb(): screens.game.found_orb.unload()
        else: screens.game.no_orb.unload()

        # Check for attack
        if attack.haveEnemy(): return

        # Load back selection screen
        screens.game.in_open.display()

