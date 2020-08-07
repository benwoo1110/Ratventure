######################################
# Import and initialize the librarys #
######################################
from random import randint
from code.api.core import os, log, screens
from code.api.events import gameEvent
from code.api.actions import Runclass
from code.logic.stats import stats
from code.logic.attack import attack
from code.logic.hero import hero
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
class power:
    row = -1
    column = -1
    orb_change = 5

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
    def changeLocation():
        # No change
        if power.orb_change == -1: return
        
        # Check if its day to change location
        if stats.day.get() % power.orb_change == 0:
            power.setLocation()
            story.change_orb.display()

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
            # Set story
            story.take_orb.display()

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

            # Set story
            story.sense_orb.display(direction)

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


# Add change orb to gameEvent queue
gameEvent.orb_change.addQueue(Runclass(run=power.changeLocation))