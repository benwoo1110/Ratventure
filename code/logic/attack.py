######################################
# Import and initialize the librarys #
######################################
from random import randint
from code.api.core import os, log, screens, pg
from code.api.data.Sound import Sound
from code.logic.stats import Stats
from code.logic.story import story
from code.logic.player import player


#################
# Setup logging #
#################
filename = os.path.basename(__file__).split('.')[0]
logger = log.get_logger(filename)
logger.info('Loading up {}...'.format(filename))


##################
# Gameplay logic #
##################
class enemy:
    enemies = pg.loadJson('./gamefiles/enemies.json')
    stats = None
    name = None
    Enemy = dict()

    @staticmethod
    def load(name:str):
        enemy.name = name
        enemy.Enemy = enemy.enemies[name].copy()
        enemy.stats = Stats (
            damage = enemy.Enemy['stats']['damage'].copy(),
            defence = enemy.Enemy['stats']['defence'],
            health = enemy.Enemy['stats']['health'].copy()
        )

        # Set multiplier
        if enemy.enemies['day_saturation'] == -1: saturation = 0
        else: saturation = ((player.stats.day // enemy.enemies['day_saturation']) * 0.15)

        enemy.stats.multiply(enemy.enemies['start_multiplier'] + saturation)

    @staticmethod
    def reset():
        enemy.stats = None
        enemy.name = None
        enemy.Enemy = dict()


class attack:
    
    @staticmethod
    def haveEnemy():
        Grid = screens.game.map.grid.Grid
        
        # Reset
        enemy.reset()

        # Not attack if hero is in town
        if Grid.heroInTown(): return False

        # Detect enemy present in grid
        for name in enemy.enemies['list']:
            if name in Grid.tiles[player.hero.row][player.hero.column].sprites:
                enemy.load(name)
                # Load attack screen
                attack.initSurface()
                return True

        # Calculate enemy appearing
        chance_number = randint(1, 100)
        if chance_number > enemy.enemies['appear_chance']: return False

        # Get new enemy based on chance
        base = 0
        new_enemy = False
        chance_number = randint(1, 100)
        
        for name in enemy.enemies['list']:
            if base < chance_number <= enemy.enemies[name]['chance']+base:
                print(enemy.enemies[name])
                enemy.load(name)
                new_enemy = True

            base += enemy.enemies[name]['chance']
        
        # Add enemy to grid
        if new_enemy:
            Grid.tiles[player.hero.row][player.hero.column].sprites.insert(0, enemy.name)
            # Show attack screen if there is an enemy
            attack.initSurface()
            return True

        return False

    @staticmethod
    def runChance():
        # Get chance of whether player can run from enemy
        chance_number = randint(1, 100)

        # Player able to run
        if chance_number <= enemy.enemies['run_chance']:
            screens.game.attack.run.lock_state = False
            screens.game.attack.run.switchState('', False)
            
        # Player unable to run
        else: 
            screens.game.attack.run.switchState('Disabled', False)
            screens.game.attack.run.lock_state = True


    @staticmethod
    def initSurface():
        # Set enemy image
        screens.game.attack.enemy.switchState(enemy.name.capitalize(), False)
        
        # Set enemy stats
        enemy.stats.display('damage', screens.game.attack.stats, False)
        enemy.stats.display('defence', screens.game.attack.stats, False)
        enemy.stats.display('health', screens.game.attack.stats, False)

        # Show enemy in grid
        screens.game.map.load(withItems=['grid'], refresh=True)

        # Enable buttons
        screens.game.attack.attack.switchState('', False)
        screens.game.attack.run.switchState('', False)

        # See chance of run
        attack.runChance()

        # Show message
        if enemy.name == 'king': story.encounter_king.display()
        else: story.encounter_wild.display(enemy.name.capitalize())

        # Cool sword sound
        Sound.encounter.play()

        # Load attack surface
        screens.game.attack.load(withItems='all', refresh=True)
        
        # Display new screen
        screens.game.display()

    @staticmethod
    def run():
        # Add run story
        story.run.display()

        # Show back in open
        screens.game.attack.unload()
        screens.game.in_open.display()

    @staticmethod
    def Attack(counter:int):
        # Start of attack
        if counter == 0: 

            # Disable buttons
            screens.game.attack.attack.switchState('Disabled')
            screens.game.attack.run.switchState('Disabled')

            # Cool sword battle effect
            Sound.battle.play(maxtime=3000, withVolume=0.24)

            # Enemy is immune without orb of power
            if enemy.Enemy['needOrb'] and not player.weapon.have('orb'):
                # Hero cannot attack
                hero_damage = 0
                story.immune.display()
            
            # Hero attacks
            else:
                hero_damage = player.stats.calDamage(enemy.stats.defence)
                story.hero_attack.display(hero_damage, enemy.name)

            enemy.stats.update('health', [-hero_damage, 0], screens.game.attack.stats, True, screens.game.attack.enemy)            

        # Next move
        elif counter == 130: 

            # Enemy is dead
            if enemy.stats.health[0] <= 0:
                # Stop battle sound
                Sound.battle.stop()

                # Show defeat message
                story.enemy_defeated.display(enemy.name)

                # Remove enemy from grid
                screens.game.map.grid.Grid.tiles[player.hero.row][player.hero.column].sprites.pop(0)
                
                # Cool win sound
                Sound.attack_win.play()

            # Enemy attacks
            else:
                enemy_damage = enemy.stats.calDamage(player.stats.defence)
                story.enemy_attack.display(enemy.name, enemy_damage)

                player.stats.update('health', [-enemy_damage, 0], screens.game.info.stats, True, screens.game.info.hero)

        # Next move
        elif counter == 260:

            # If player is dead, player loses
            if player.stats.health[0] <= 0:
                story.hero_defeated.display()

            # Enemy is dead
            elif enemy.stats.health[0] <= 0:

                # If king is defeated, player wins
                if enemy.name == 'king':
                    story.win.display()

                # Just a wild enemy
                else:
                    # Gains from defeat
                    elixir_gained = randint(*enemy.Enemy['gains'])
                    player.stats.update('elixir', elixir_gained, screens.game.info.stats, True, screens.game.info.hero)
                    story.gain_elixir.display(elixir_gained)

                    # Cool coin sound
                    Sound.gain_elixir.play()

            # Both player and enemy is still alive
            else: 
                if screens.game.attack.run.lock_state: story.attack_norun.display()
                else: story.attack_run.display()
                
                # Enable buttons for another attack/run
                screens.game.attack.attack.switchState('')
                screens.game.attack.run.switchState('')
                return True

        # End attack sequence
        elif counter >= 390:

            # Player is dead, load game over screen
            if player.stats.health[0] <= 0:
                screens.end_game.unload()
                screens.end_game.gameover.load()
                screens.changeStack(type='load', screen='end_game')
                return True

            # Enemy is dead
            elif enemy.stats.health[0] <= 0:
                # If king is defeated, load win screen
                if enemy.name == 'king':
                    # Player won
                    screens.end_game.unload()
                    screens.end_game.win.load()
                    screens.changeStack(type='load', screen='end_game')
                    return True
                
                else:
                    # Return to selection screen
                    screens.game.attack.unload()
                    screens.game.map.load(withItems=['grid'], refresh=True)
                    screens.game.info.load(withItems=['stats'], refresh=True)
                    screens.game.in_open.load()
                    screens.game.display()
                    return True
