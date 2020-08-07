######################################
# Import and initialize the librarys #
######################################
from random import randint
from code.api.core import os, log, screens
from code.api.events import gameEvent
from code.logic.stats import stats
from code.api.data.Grid import Sprite
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
class attack:
    enemies = {
        'appear_chance': 0,
        'run_chance': 20,
        'multiplier': 1.2,
        'list': ['rat', 'moth', 'roach', 'king'],
        'rat': {
            'chance': 10,
            'needOrb': False,
            'stats': {
                'damage': [2, 3],
                'defence': 1,
                'health': [8, 8]
            },
            'gains': [5, 10]
        },
        'moth': {
            'chance': 30,
            'needOrb': False,
            'stats': {
                'damage': [1, 2],
                'defence': 2,
                'health': [10, 10]
            },
            'gains': [5, 10]
        },
        'roach': {
            'chance': 60,
            'needOrb': False,
            'stats': {
                'damage': [1, 2],
                'defence': 2,
                'health': [10, 10]
            },
            'gains': [5, 10]
        },
        'king': {
            'chance': -1,
            'needOrb': True,
            'stats': {
                'damage': [4, 8],
                'defence': 4,
                'health': [20, 20]
            },
        },
    }

    current_enemy = None
    
    @staticmethod
    def haveEnemy():
        Grid = screens.game.map.grid.Grid
        
        # Reset
        attack.current_enemy = None

        # Not attack if hero is in town
        if Grid.heroInTown(): return False

        # Detect enemy present in grid
        for name in attack.enemies['list']:
            if name in Grid.tiles[hero.row][hero.column].sprites:
                attack.current_enemy = name
                # Load attack screen
                attack.initSurface()
                return True

        # Calculate enemy appearing
        chance_number = randint(1, 100)
        if chance_number > attack.enemies['appear_chance']: return False

        # Get new enemy based on chance
        base = 0
        new_enemy = False
        chance_number = randint(1, 100)
        
        for name in attack.enemies['list']:
            if base < chance_number <= attack.enemies[name]['chance']+base:
                attack.current_enemy = name
                new_enemy = True

            base += attack.enemies[name]['chance']
        
        # Add enemy to grid
        if new_enemy:
            Grid.tiles[hero.row][hero.column].sprites.insert(0, attack.current_enemy)

            # Show attack screen if there is an enemy
            attack.initSurface()

            return True

        return False

    @staticmethod
    def runChance():
        # Get chance of whether player can run from enemy
        chance_number = randint(1, 100)

        # Player able to run
        if chance_number <= attack.enemies['run_chance']:
            screens.game.attack.run.lock_state = False
            screens.game.attack.run.switchState('', False)
            
        # Player unable to run
        else: 
            screens.game.attack.run.switchState('Disabled', False)
            screens.game.attack.run.lock_state = True


    @staticmethod
    def initSurface():
        # Get enemy
        enemy = attack.enemies[attack.current_enemy]

        # Set enemy image
        screens.game.attack.enemy.switchState(attack.current_enemy.capitalize(), False)
        
        # Set enemy stats
        stats.damage.set('attack', *enemy['stats']['damage'], False, attack.enemies['multiplier'])
        stats.defence.set('attack', enemy['stats']['defence'], False, attack.enemies['multiplier'])
        stats.health.set('attack', *enemy['stats']['health'], False, attack.enemies['multiplier'])

        # Show enemy in grid
        screens.game.map.load(withItems=['grid'], refresh=True)

        # Enable buttons
        screens.game.attack.attack.switchState('', False)
        screens.game.attack.run.switchState('', False)

        # See chance of run
        attack.runChance()

        # Show message
        if attack.current_enemy == 'king': story.encounter_king.display()
        else: story.encounter_wild.display(attack.current_enemy.capitalize())

        # Load attack surface
        screens.game.attack.load(withItems='all', refresh=True)
        
        # Display new screen
        screens.game.display()

    @staticmethod
    def run():
        # Add a day
        stats.day.update()

        # Add run story
        story.run.display()

        # Show back in open
        screens.game.attack.unload()
        screens.game.in_open.display()

    @staticmethod
    def doDamage(by:str, to:str) -> int:
        # Calculate damage
        damage_done = randint(*stats.damage.get(by))

        # Remove defence
        damage_done = max(0, damage_done - stats.defence.get(to))

        # Deal damage to enemy
        stats.health.update(to, -damage_done)

        return damage_done

    @staticmethod
    def Attack(counter:int):
        # Start of attack
        if counter == 0: 

            # Disable buttons
            screens.game.attack.attack.switchState('Disabled')
            screens.game.attack.run.switchState('Disabled')

            # Enemy is immune without orb of power
            if attack.enemies[attack.current_enemy]['needOrb'] and not stats.power.hasOrb():
                # Hero cannot attack
                story.immune.display()
            
            # Hero attacks
            else:
                # Deal damage
                hero_damage = attack.doDamage(by='info', to='attack')
                story.hero_attack.display(hero_damage, attack.current_enemy)

        # Next move
        elif counter == 100: 

            # Enemy is dead
            if stats.health.get('attack')[0] == 0:
                # Show defeat message
                story.enemy_defeated.display(attack.current_enemy)
                # Get hero's position
                hero_r, hero_c = screens.game.map.grid.Grid.find('hero')
                # Remove enemy from grid
                screens.game.map.grid.Grid.tiles[hero_r][hero_c].sprites.pop(0)

            # Enemy attacks
            else:
                enemy_damage = attack.doDamage(by='attack', to='info')
                story.enemy_attack.display(attack.current_enemy, enemy_damage)

        # Next move
        elif counter == 200:

            # If player is dead, player loses
            if stats.health.get('info')[0] == 0:
                story.hero_defeated.display()

            # Enemy is dead            
            elif stats.health.get('attack')[0] == 0:

                # If king is defeated, player wins
                if attack.current_enemy == 'king':
                    story.win.display()

                # Just a wild enemy
                else:
                    # Gains here
                    
                    # Return to selection screen
                    screens.game.attack.unload()
                    screens.game.map.load(withItems=['grid'], refresh=True)
                    screens.game.info.load(withItems=['stats'], refresh=True)
                    screens.game.in_open.load()
                    screens.game.display()
                    return True
            
            # Both player and enemy is still alive
            else: 
                story.attack.display()
                # Enable buttons for another attack/run
                screens.game.attack.attack.switchState('')
                screens.game.attack.run.switchState('')
                return True

        # End attack sequence
        elif counter >= 300:

            # If player is dead, load game over screen
            if stats.health.get('info')[0] == 0:
                screens.end_game.unload()
                screens.end_game.gameover.load()
                screens.changeStack(type='load', screen='end_game')
                return True

            # If king is defeated, load win screen
            elif stats.health.get('attack')[0] == 0 and attack.current_enemy == 'king':
                # Player won
                screens.end_game.unload()
                screens.end_game.win.load()
                screens.changeStack(type='load', screen='end_game')
                return True