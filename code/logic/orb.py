######################################
# Import and initialize the librarys #
######################################
from random import randint
from code.api.core import os, log, screens
from code.api.events import gameEvent
from code.api.actions import Runclass
from code.logic.stats import Bonus
from code.logic.player import player
from code.logic.attack import attack
from code.logic.story import story
from code.api.data.Sound import Sound


#################
# Setup logging #
#################
filename = os.path.basename(__file__).split('.')[0]
logger = log.get_logger(filename)


##################
# Gameplay logic #
##################
class orb:
    change = 5
    stats = Bonus (
        damage = [5, 5],
        defence = 5
    )

    @staticmethod
    def setLocation():
        Grid = screens.game.map.grid.Grid

        while True:
            row, column = randint(0, 7), randint(0, 7)

            # Ensure that pos is valid and in open
            if  (row >=4 or column >= 4) and (not Grid.tiles[row][column].hasSprite()):
                # Save orb pos
                player.orb.setNew([row, column])
                break

    @staticmethod
    def changeLocation():
        # No change
        if orb.change == -1 or player.weapon.have('orb'): return
        
        # Check if its day to change location
        if player.stats.day % orb.change == 0:
            orb.setLocation()
            story.change_orb.display()

    @staticmethod
    def canSense():
        if player.weapon.have('orb'): screens.game.in_open.sense_orb.switchState('Disabled', True, False)
        else: screens.game.in_open.sense_orb.switchState('', True, False)

    @staticmethod
    def initSurface():
        Grid = screens.game.map.grid.Grid

        # Unload previous selection screen
        screens.game.in_open.unload()

        # Orb is found
        if player.orb.pos() == player.hero.pos():
            # Set story
            story.take_orb.display()

            # Show orb in map
            Grid.tiles[player.orb.row][player.orb.column].sprites.insert(0, 'orb')

            screens.game.map.load(withItems=['grid'], refresh=True)
            screens.game.display(withSurfaces=['found_orb'])

        # Orb not found
        else:
            # Get direction
            direction = ''

            if player.orb.row > player.hero.row: direction += 'south'
            elif player.orb.row < player.hero.row: direction += 'north'

            if player.orb.column > player.hero.column: direction += 'east'
            elif player.orb.column < player.hero.column: direction += 'west'

            direction = direction.capitalize()

            # Set story
            story.sense_orb.display(direction)

            # Set compass direction
            screens.game.no_orb.compass.switchState(direction, False)

            # Load screen
            screens.game.no_orb.display(withItems=['compass'], refresh=True)

        # Add a day
        player.next_day()

    @staticmethod
    def take():
        Grid = screens.game.map.grid.Grid

        # Update stats upon taking orb
        player.stats.addBonus(orb.stats, screens.game.info.stats, True, screens.game.info.hero)
        player.weapon.add('orb')

        # Disable sensing orb
        screens.game.in_open.sense_orb.switchState('Disabled', withDisplay=False)

        # Remove orb from map
        Grid.tiles[player.orb.row][player.orb.column].sprites.remove('orb')
        screens.game.map.display(withItems=['grid'], refresh=True)

        # Play cool sound
        Sound.orb_take.play()

        # Return to selection menu
        orb.back()
    
    @staticmethod
    def back():
        # Unload orb screen
        if player.weapon.have('orb'): screens.game.found_orb.unload()
        else: screens.game.no_orb.unload()

        # Check for attack
        if attack.haveEnemy(): return

        # Load back selection screen
        screens.game.in_open.display()


# Add change orb to gameEvent queue
gameEvent.orb_change.addQueue(Runclass(run=orb.changeLocation))