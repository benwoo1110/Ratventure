######################################
# Import and initialize the librarys #
######################################
from random import random, randint
from code.api.core import os, log, screens
from code.logic.stats import stats
from code.api.data.Grid import Sprite


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
        'rat': {
            'chance': 0.6,
            'needOrb': False,
            'stats': {
                'damage': [1, 3],
                'defence': 1,
                'health': [8, 8]
            },
            'gains': {
                'damage': [0, 1],
                'defence': 0,
                'health': [0, 0]
            },
        },
        'moth': {
            'chance': 0.4,
            'needOrb': False,
            'stats': {
                'damage': [1, 2],
                'defence': 2,
                'health': [12, 12]
            },
            'gains': {
                'damage': [0, 0],
                'defence': 1,
                'health': [0, 0]
            },
        },
        'king': {
            'chance': 0,
            'needOrb': True,
            'stats': {
                'damage': [8, 12],
                'defence': 5,
                'health': [25, 25]
            },
        },
    }

    current_enemy = None
    
    @staticmethod
    def haveEnemy():
        Grid = screens.game.map.grid.Grid
        
        # Reset
        attack.current_enemy = None

        # Get hero's position
        hero_r, hero_c = Grid.find('hero')

        # Not attack if hero is in town
        if Grid.heroInTown(): return False

        # Calculate enemy appearing
        new_enemy = False
        for name, enemy in attack.enemies.items():
            # Detect enemy present in grid
            if name in Grid.tiles[hero_r][hero_c].sprites:
                attack.current_enemy = name
                break
            
            # Get chance of new enemy appearing
            chance_number = random()
            if chance_number < enemy['chance']:
                attack.current_enemy = name
                new_enemy = True
        
        # Add enemy to grid
        if new_enemy: Grid.tiles[hero_r][hero_c].sprites.insert(0, attack.current_enemy)

        # Show attack screen if there is an enemy
        if attack.current_enemy != None: 
            attack.initSurface()
            return True

        return False

    @staticmethod
    def initSurface():
        Grid = screens.game.map.grid.Grid

        # Get enemy
        enemy = attack.enemies[attack.current_enemy]

        # Get hero's position
        hero_r, hero_c = Grid.find('hero')

        # Set enemy image
        screens.game.attack.enemy.switchState(attack.current_enemy.capitalize(), False)
        
        # Set enemy stats
        stats.damage.set('attack', 'stats', *enemy['stats']['damage'], False)
        stats.defence.set('attack', 'stats', enemy['stats']['defence'], False)
        stats.health.set('attack', 'stats', *enemy['stats']['health'], False)

        # Show enemy in grid
        screens.game.map.load(withItems=['grid'], refresh=True)

        # Load attack surface
        screens.game.attack.load(withItems='all', refresh=True)
        
        # Display new screen
        screens.game.display()

    @staticmethod
    def run():
        Grid = screens.game.map.grid.Grid

        # Add a day
        stats.day.update()

        # Show back in open
        screens.game.attack.unload()
        screens.game.in_open.display()

    @staticmethod
    def doDamage(by:str, to:str):
        # Calculate damage
        damage_done = randint(*stats.damage.get(by, 'stats'))

        # Remove defence
        damage_done -= stats.defence.get(to, 'stats')

        # Deal damage to enemy
        stats.health.update(to, 'stats', -damage_done)

        print(damage_done)

    @staticmethod
    def Attack():
        can_damage = True
        # Check if enemy require orb to deal damage
        if attack.enemies[attack.current_enemy]['needOrb']:
            if not stats.power.hasOrb(): can_damage = False

        # Calculate damage by hero
        if can_damage:
            print('damage by hero: ',end='')
            attack.doDamage(by='info', to='attack')

        # Calculate damage by enemy
        print('damage by enemy: ',end='')
        attack.doDamage(by='attack', to='info')

        # When hero dies, game over
        if stats.health.get('info', 'stats')[0] == 0:
            # actions to do when hero dies
            return

        # Check when enemy dies
        if stats.health.get('attack', 'stats')[0] == 0:
            
            # When the king is defeated, player wins
            if attack.current_enemy == 'king':
                # Player won
                return

            Grid = screens.game.map.grid.Grid

            # Gains from winning
            gains = attack.enemies[attack.current_enemy]['gains']
            stats.damage.update('info', 'stats', *gains['damage'], False)
            stats.defence.update('info', 'stats', gains['defence'], False)
            stats.health.update('info', 'stats', *gains['health'], False)

            # Reset
            attack.current_enemy = None

            # Get hero's position
            hero_r, hero_c = Grid.find('hero')

            # Remove enemy from grid
            Grid.tiles[hero_r][hero_c].sprites.pop(0)

            # Load back in open selection
            screens.game.attack.unload()
            screens.game.map.load(withItems=['grid'], refresh=True)
            screens.game.info.load(withItems=['stats'], refresh=True)
            screens.game.in_open.load()
            screens.game.display()