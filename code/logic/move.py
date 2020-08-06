######################################
# Import and initialize the librarys #
######################################
from code.api.core import os, log, screens
from code.api.events import gameEvent
from code.logic.stats import stats
from code.logic.attack import attack
from code.logic.story import story
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
class move:
    new_r = -1
    new_c = -1

    @staticmethod
    def checkDirection():
        move_surface = screens.game.move
        # up
        if not 0 <= hero.row-1 <= 7: move_surface.up.switchState('Disabled', withDisplay=False)
        else: move_surface.up.switchState('', withDisplay=False)
        
        # down
        if not 0 <= hero.row+1 <= 7: move_surface.down.switchState('Disabled', withDisplay=False)
        else: move_surface.down.switchState('', withDisplay=False)
        
        # left
        if not 0 <= hero.column-1 <= 7: move_surface.left.switchState('Disabled', withDisplay=False)
        else: move_surface.left.switchState('', withDisplay=False)
        
        # right
        if not 0 <= hero.column+1 <= 7: move_surface.right.switchState('Disabled', withDisplay=False)
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
    def Move(counter, direction:str):
        Grid = screens.game.map.grid.Grid

        # Start of move
        if counter == 0:

            # Disable move
            screens.game.move.up.switchState('Disabled', withDisplay=False)
            screens.game.move.down.switchState('Disabled', withDisplay=False)
            screens.game.move.left.switchState('Disabled', withDisplay=False)
            screens.game.move.right.switchState('Disabled', withDisplay=False)
            screens.game.move.display(withItems=['up', 'down', 'left', 'right'], refresh=True)

            # Check for enemy to remove
            for enemy in attack.enemies:
                if enemy != 'king' and enemy in Grid.tiles[hero.row][hero.column].sprites:
                    Grid.tiles[hero.row][hero.column].sprites.remove(enemy)

            # Remove hero from current location
            Grid.tiles[hero.row][hero.column].sprites.remove('hero')

            # Change location
            move.new_r, move.new_c = hero.row, hero.column
            if direction == 'up' and move.new_r > 0: move.new_r -= 1
            elif direction == 'down' and move.new_r < 7: move.new_r += 1
            elif direction == 'left' and move.new_c > 0: move.new_c -= 1
            elif direction == 'right' and move.new_c < 7: move.new_c += 1

            print(move.new_r, move.new_c)

        # Run move animation
        elif counter < 35:
            Grid.move(counter, move.new_r, move.new_c)

        # Move is done
        elif counter >= 35:
            # Set new location
            hero.row, hero.column = move.new_r, move.new_c
            move.new_r, move.new_c = -1, -1

            # Add hero to new location
            Grid.tiles[hero.row][hero.column].sprites.append('hero')

            # Update map
            screens.game.map.display(withItems=['grid'], refresh=True)

            # Add a day
            stats.day.update()

            # Check for attack
            if attack.haveEnemy(): 
                # Unload move
                screens.game.move.unload()
                return True

            # Update story
            if Grid.heroInTown(): 
                story.in_town.display()
                # Show town selection
                move.back()
                return True

            else: story.in_open.display()

            # Disable arrows for impossible directions
            move.checkDirection()
            screens.game.move.display(withItems=['up', 'down', 'left', 'right'], refresh=True)

            return True

    @staticmethod
    def back():
        Grid = screens.game.map.grid.Grid

        # Unload move
        screens.game.move.unload()

        # Check if hero in town or open
        if Grid.heroInTown(): screens.game.in_town.display()
        else: screens.game.in_open.display()