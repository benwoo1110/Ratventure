######################################
# Import and initialize the librarys #
######################################
from random import randint
from code.api.core import os, log, screens, PgEss, pygame
from code.api.data.Sound import Sound
from code.logic.stats import Stats
from code.logic.story import story
from code.logic.player import Player
from code.logic.playerRank import PlayerRank



#################
# Setup logging #
#################
filename = os.path.basename(__file__).split('.')[0]
logger = log.get_logger(filename)


##################
# Gameplay logic #
##################
class Enemy:
    enemies = PgEss.loadJson('./gamefiles/enemies.json')
    stats = None
    name = None
    Enemy = dict()

    @staticmethod
    def load(name:str):
        # Set the enemy
        Enemy.name = name
        Enemy.Enemy = Enemy.enemies[name].copy()
        Enemy.stats = Stats (
            damage = Enemy.Enemy['stats']['damage'].copy(),
            defence = Enemy.Enemy['stats']['defence'],
            health = Enemy.Enemy['stats']['health'].copy()
        )

        # Set multiplier
        if Enemy.enemies['day_saturation'] == -1: saturation = 0
        else: saturation = ((Player.stats.day // Enemy.enemies['day_saturation']) * 0.15)

        Enemy.stats.multiply(Enemy.enemies['start_multiplier'] + saturation)

    @staticmethod
    def reset():
        Enemy.stats = None
        Enemy.name = None
        Enemy.Enemy = dict()


class Attack:
    
    @staticmethod
    def haveEnemy():
        Grid = screens.game.map.grid.Grid
        
        # Reset
        Enemy.reset()

        # Not attack if hero is in town
        if Grid.heroInTown(): return False

        # Detect enemy present in grid
        for name in Enemy.enemies['list']:
            if name in Grid.tiles[Player.hero.row][Player.hero.column].sprites:
                # Play rat king music
                if name == 'king':
                    pygame.mixer.fadeout(600)
                    Sound.rat_king.play(loops=-1, withVolume=PgEss.config.sound.background + 0.24, fadetime=3000)

                Enemy.load(name)
                # Load attack screen
                Attack.initSurface()
                return True

        # Calculate enemy appearing
        chance_number = randint(1, 100)
        if chance_number > Enemy.enemies['appear_chance']: return False

        # Get new enemy based on chance
        base = 0
        new_enemy = False
        chance_number = randint(1, 100)

        for name in Enemy.enemies['list']:
            if base < chance_number <= Enemy.enemies[name]['chance']+base:
                Enemy.load(name)
                new_enemy = True

            base += Enemy.enemies[name]['chance']

        # Add enemy to grid
        if new_enemy:
            Grid.tiles[Player.hero.row][Player.hero.column].sprites.insert(0, Enemy.name)
            # Show attack screen if there is an enemy
            Attack.initSurface()
            return True

        return False

    @staticmethod
    def runChance():
        # Get chance of whether player can run from enemy
        chance_number = randint(1, 100)

        # Player able to run
        if chance_number <= Enemy.enemies['run_chance']:
            screens.game.attack.run.lock_state = False
            screens.game.attack.run.switchState('', False)
            
        # Player unable to run
        else: 
            screens.game.attack.run.switchState('Disabled', False)
            screens.game.attack.run.lock_state = True


    @staticmethod
    def initSurface():
        # Set enemy image
        screens.game.attack.enemy.switchState(Enemy.name.capitalize(), False)
        
        # Set enemy stats
        Enemy.stats.display('damage', screens.game.attack.stats, False)
        Enemy.stats.display('defence', screens.game.attack.stats, False)
        Enemy.stats.display('health', screens.game.attack.stats, False)

        # Show enemy in grid
        screens.game.map.load(withItems=['grid'], refresh=True)

        # Enable buttons
        screens.game.attack.attack.switchState('', False)
        screens.game.attack.run.switchState('', False)

        # See chance of run
        Attack.runChance()

        # Reset stats update
        screens.game.attack.enemy.stats.setText('', withDisplay=False)

        # Show message
        if Enemy.name == 'king': story.encounter_king.display()
        else: story.encounter_wild.display(Enemy.name.capitalize())

        # Cool sword sound
        Sound.encounter.play()

        # Load attack surface
        screens.game.attack.load(withItems='all', refresh=True)
        
        # Display new screen
        screens.game.display()

    @staticmethod
    def run():
        # Play swoosh sound effect
        Sound.run.play(withVolume=0.6)

        # Add run story
        story.run.display()

        # Back to selection
        Attack.back()


    @staticmethod
    def back():
        # Stop rat king music if its playing
        if Sound.rat_king.isPlaying():
            pygame.mixer.fadeout(600)
            Sound.game_background.play(loops=-1, withVolume=PgEss.config.sound.background, fadetime=5000)

        # Return to in open selection screen
        screens.game.attack.unload()
        screens.game.map.load(withItems=['grid'], refresh=True)
        screens.game.info.load(withItems=['stats'], refresh=True)
        screens.game.in_open.load()
        screens.game.display()

    @staticmethod
    def attack(counter:int):
        # Start of attack
        if counter == 0: 

            # Disable buttons
            screens.game.attack.attack.switchState('Disabled')
            screens.game.attack.run.switchState('Disabled')

            # Cool sword battle effect
            Sound.battle.play(maxtime=3000, withVolume=0.24)

            # Enemy is immune without orb of power
            if Enemy.Enemy['needOrb'] and not Player.weapon.have('orb'):
                # Hero cannot attack
                hero_damage = 0
                story.immune.display()
            
            # Hero attacks
            else:
                hero_damage = Player.stats.calDamage(Enemy.stats.defence)
                story.hero_attack.display(hero_damage, Enemy.name)

            Enemy.stats.update('health', [-hero_damage, 0], screens.game.attack.stats, True, screens.game.attack.enemy)            

        # Next move
        elif counter == 130: 

            # Enemy is dead
            if Enemy.stats.health[0] <= 0:
                # Stop battle sound
                Sound.battle.stop()

                # Show defeat message
                story.enemy_defeated.display(Enemy.name)

                # Remove enemy from grid
                screens.game.map.grid.Grid.tiles[Player.hero.row][Player.hero.column].sprites.pop(0)
                
                # Cool win sound
                Sound.attack_win.play()

            # Enemy attacks
            else:
                enemy_damage = Enemy.stats.calDamage(Player.stats.defence)
                story.enemy_attack.display(Enemy.name, enemy_damage)

                Player.stats.update('health', [-enemy_damage, 0], screens.game.info.stats, True, screens.game.info.hero)

        # Next move
        elif counter == 260:

            # If player is dead, player loses
            if Player.stats.health[0] <= 0:
                story.hero_defeated.display()

            # Enemy is dead
            elif Enemy.stats.health[0] <= 0:

                # If king is defeated, player wins
                if Enemy.name == 'king':
                    story.win.display()

                # Just a wild enemy
                else:
                    # Gains from defeat
                    elixir_gained = randint(*Enemy.Enemy['gains'])
                    Player.stats.update('elixir', elixir_gained, screens.game.info.stats, True, screens.game.info.hero)
                    story.gain_elixir.display(elixir_gained)

                    # Cool coin sound
                    Sound.gain_elixir.play(withVolume=0.8)

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
            if Player.stats.health[0] <= 0:
                Attack.game_end('gameover')
                return True

            # Enemy is dead
            elif Enemy.stats.health[0] <= 0:
                # If king is defeated, load win screen
                if Enemy.name == 'king':
                    # Player won
                    Attack.game_end('win')
                    return True
                
                else:
                    Attack.back()
                    return True

    @staticmethod
    def game_end(type:str):
        screens.end_game.unload()

        # Stop game music, back to normal background music
        if not Sound.background.isPlaying():
            pygame.mixer.fadeout(200)
            Sound.background.play(loops=-1, withVolume=PgEss.config.sound.background, fadetime=3000)

        end_game_screen = screens.end_game
        # Check if win screen is the one loaded
        if type == 'win':
            # Save to leaderboard
            end_game_screen.win.leaderboard.rankid = PlayerRank.add()

            # Set player leaderboard on win screen
            end_game_screen.win.leaderboard.postion.setText(str(PlayerRank.getPos()), withDisplay=False)
            end_game_screen.win.leaderboard.nickname.setText(Player.nickname, withDisplay=False)
            end_game_screen.win.leaderboard.days.setText(str(Player.stats.day), withDisplay=False)

            # Load the changes
            end_game_screen.win.load(withItems='all', refresh=True)

            # Play win sound effect
            Sound.win.play()

        # Check if gameover screen is the one loaded
        elif type == 'gameover':
            # Load the screen changes
            end_game_screen.gameover.load(withItems='all', refresh=True)

            # Play gameover sound effect
            Sound.game_over.play()

        screens.changeStack(type='load', screen='end_game')
