######################################
# Import and initialize the librarys #
######################################
from code.api.core import os, log, screens
from code.logic.attack import Attack, Enemy
from code.logic.story import story
from code.logic.player import Player
from code.api.data.Sound import sound


#################
# Setup logging #
#################
filename = os.path.basename(__file__).split('.')[0]
logger = log.get_logger(filename)


##################
# Gameplay logic #
##################
class Move:
    new_r = -1
    new_c = -1

    @staticmethod
    def checkDirection():
        move_surface = screens.game.move
        # up
        if not 0 <= Player.hero.row-1 <= 7: move_surface.up.switchState('Disabled', withDisplay=False)
        else: move_surface.up.switchState('', withDisplay=False)
        
        # down
        if not 0 <= Player.hero.row+1 <= 7: move_surface.down.switchState('Disabled', withDisplay=False)
        else: move_surface.down.switchState('', withDisplay=False)
        
        # left
        if not 0 <= Player.hero.column-1 <= 7: move_surface.left.switchState('Disabled', withDisplay=False)
        else: move_surface.left.switchState('', withDisplay=False)
        
        # right
        if not 0 <= Player.hero.column+1 <= 7: move_surface.right.switchState('Disabled', withDisplay=False)
        else: move_surface.right.switchState('', withDisplay=False)
    
    @staticmethod
    def initSurface():
        Grid = screens.game.map.grid.Grid

        # Check if hero in town or open
        if Grid.heroInTown(): screens.game.in_town.unload()
        else: screens.game.in_open.unload()

        # Disable arrows for impossible directions
        Move.checkDirection()

        # Display to screen
        screens.game.move.back.switchState('', withDisplay=False)
        screens.game.move.display()


    @staticmethod
    def move(counter, direction:str):
        Grid = screens.game.map.grid.Grid

        # Start of move
        if counter == 0:

            # Disable move
            screens.game.move.up.switchState('Disabled', withDisplay=False)
            screens.game.move.down.switchState('Disabled', withDisplay=False)
            screens.game.move.left.switchState('Disabled', withDisplay=False)
            screens.game.move.right.switchState('Disabled', withDisplay=False)
            screens.game.move.back.switchState('Disabled', withDisplay=False)
            screens.game.move.display(withItems=['up', 'down', 'left', 'right'], refresh=True)

            # Check for enemy to remove
            for name in Enemy.enemies:
                if name != 'king' and name in Grid.tiles[Player.hero.row][Player.hero.column].sprites:
                    Grid.tiles[Player.hero.row][Player.hero.column].sprites.remove(Enemy.name)

            # Remove hero from current location
            Grid.tiles[Player.hero.row][Player.hero.column].sprites.remove('hero')

            # Change location
            Move.new_r, Move.new_c = Player.hero.row, Player.hero.column
            if direction == 'up' and Move.new_r > 0: Move.new_r -= 1
            elif direction == 'down' and Move.new_r < 7: Move.new_r += 1
            elif direction == 'left' and Move.new_c > 0: Move.new_c -= 1
            elif direction == 'right' and Move.new_c < 7: Move.new_c += 1

            # Foot steps
            sound.walk.play(maxtime=860)

        # Run move animation
        elif counter <= 50:
            Grid.move(counter, Move.new_r, Move.new_c)

        # Move is done
        elif counter > 50:
            # Set new location
            Player.hero.setNew((Move.new_r, Move.new_c))
            Move.new_r, Move.new_c = -1, -1

            # Add hero to new location
            Grid.tiles[Player.hero.row][Player.hero.column].sprites.append('hero')

            # Update map
            screens.game.map.display(withItems=['grid'], refresh=True)

            # Add a day
            Player.next_day()
            
            # Check for attack
            if Attack.haveEnemy(): 
                # Unload move
                screens.game.move.unload()
                return True

            # Update story
            if Grid.heroInTown(): 
                story.in_town.display()
                # Show town selection
                Move.back()
                return True

            else: story.in_open.display()
            
            # Disable arrows for impossible directions
            Move.checkDirection()
            screens.game.move.back.switchState('', withDisplay=False)
            screens.game.move.display(withItems=['up', 'down', 'left', 'right', 'back'], refresh=True)

            return True

    @staticmethod
    def back():
        Grid = screens.game.map.grid.Grid

        # Unload move
        screens.game.move.unload()

        # Check if hero in town or open
        if Grid.heroInTown(): screens.game.in_town.display()
        else: screens.game.in_open.display()