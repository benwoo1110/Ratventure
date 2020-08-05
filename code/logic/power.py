######################################
# Import and initialize the librarys #
######################################
from random import randint
from code.api.core import os, log, screens
from code.logic.stats import stats
from code.logic.attack import attack
from code.logic.hero import hero


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
    def location() -> tuple: return (power.row, power.column)

    @staticmethod
    def setLocation():
        Grid = screens.game.map.grid.Grid

        while True:
            row, column = randint(0, 7), randint(0, 7)

            # Ensure that pos is valid and in open
            if  (row >=4 or column >= 4) and (not Grid.tiles[row][column].hasSprite()):
                # Save orb pos
                power.row, power.column = row, column
                break

    @staticmethod
    def canSense():
        if stats.power.hasOrb(): screens.game.in_open.sense_orb.switchState('Disabled', False)
        else: screens.game.in_open.sense_orb.switchState('', False)

    @staticmethod
    def initSurface():
        Grid = screens.game.map.grid.Grid
        # Unload previous selection screen
        screens.game.in_open.unload()

        # Orb is found
        if hero.location() == power.location():
            # Show orb in map
            Grid.tiles[power.row][power.column].sprites.insert(0, 'orb')

            screens.game.map.load(withItems=['grid'], refresh=True)
            screens.game.display(withSurfaces=['found_orb'])

        # Orb not found
        else:
            # Get direction
            direction = ''

            if power.row > hero.row: direction += 'south'
            elif power.row < hero.row: direction += 'north'

            if power.column > hero.column: direction += 'east'
            elif power.column < hero.column: direction += 'west'

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
        stats.damage.update('info', 5, 5, False)
        stats.defence.update('info', 5)
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

