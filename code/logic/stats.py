######################################
# Import and initialize the librarys #
######################################
from code.api.core import os, log, screens
from code.api.events import gameEvent


#################
# Setup logging #
#################
filename = os.path.basename(__file__).split('.')[0]
logger = log.get_logger(filename)
logger.info('Loading up {}...'.format(filename))


##################
# Gameplay logic #
##################
class stats:

    class day:

        @staticmethod
        def update(by:int = 1, withDisplay:bool = True):
            # Get day text
            day_data = screens.game.info.day.number

            # Set new value
            day_text = str(stats.day.get() + by)

            # Check for change orb day
            gameEvent.orb_change.call()

            # Output text
            day_data.setText(day_text, withDisplay=withDisplay)

        @staticmethod
        def set(day:int, withDisplay:bool = True):
            # Get day text
            day_data = screens.game.info.day.number

            # Set new value
            day_text = str(day)

            # Output text
            day_data.setText(day_text, withDisplay=withDisplay)

        @staticmethod
        def get() -> int:
            # Get day text
            day_data = screens.game.info.day.number

            return int(day_data.text)

    class damage:

        @staticmethod
        def set(surface:str, min_d:int, max_d:int, withDisplay:bool = True, multiplier:int = 1, screen:str = 'game'):
            # Get game screen
            game_screen = screens[screen]

            # Display the text
            damage_text = '{} - {}'.format(int(min_d*multiplier), int(max_d*multiplier))
            game_screen[surface].stats.damage.setText(damage_text, withDisplay=withDisplay)

        @staticmethod
        def update(surface:str, min_d:int, max_d:int, withDisplay:bool = True, screen:str = 'game'):
            # Get game screen
            game_screen = screens[screen]

            # Get value
            min_damage, max_damage = stats.damage.get(surface)

            # Set new value
            min_damage += min_d
            max_damage += max_d

            # Display the text
            damage_text = '{} - {}'.format(min_damage, max_damage)
            game_screen[surface].stats.damage.setText(damage_text, withDisplay=withDisplay)

        @staticmethod  
        def get(surface:str) -> tuple:
            # Get game screen
            game_screen = screens.game

            # Get the damage text
            damage_text = game_screen[surface].stats.damage.text
            min_damage, max_damage = damage_text.split(' - ')

            return (int(min_damage), int(max_damage))

    class defence:

        @staticmethod
        def set(surface:str, number:int, withDisplay:bool = True, multiplier:int = 1, screen:str = 'game'):
            # Get game screen
            game_screen = screens[screen]

            # Display the text
            defence_number = int(number*multiplier)
            game_screen[surface].stats.defence.setText(str(defence_number), withDisplay=withDisplay)

        @staticmethod
        def update(surface:str, number:int, withDisplay:bool = True, screen:str = 'game'):
            # Get game screen
            game_screen = screens[screen]

            # Get value
            new_defence = str(stats.defence.get(surface) + number)

            # Display the text
            game_screen[surface].stats.defence.setText(new_defence, withDisplay=withDisplay)

        @staticmethod
        def get(surface:str):
            # Get game screen
            game_screen = screens.game

            return int(game_screen[surface].stats.defence.text)

    class health:

        @staticmethod
        def set(surface:str, current_h:int = 0, max_h:int = 0, withDisplay:bool = True, multiplier:int = 1, screen:str = 'game'):
            # Get game screen
            game_screen = screens[screen]

            # Display the text
            health_text = '{}/{}'.format(int(current_h*multiplier), int(max_h*multiplier))
            game_screen[surface].stats.health.setText(health_text, withDisplay=withDisplay)

        @staticmethod
        def update(surface:str, current_h:int = 0, max_h:int = 0, withDisplay:bool = True, screen:str = 'game'):
            # Get game screen
            game_screen = screens[screen]

            # Get value
            current_health, max_health = stats.health.get(surface)

            # Set new value
            current_health = max(0, current_health + current_h)
            max_health += max_h

            # Display the text
            health_text = '{}/{}'.format(current_health, max_health)
            game_screen[surface].stats.health.setText(health_text, withDisplay=withDisplay)

        @staticmethod
        def setBonus(surface:str, number:int, withDisplay:bool = True):
            # Get game screen
            game_screen = screens.game
            
            # Set new value
            health_text = '+ {}'.format(number)

            # Display the text
            game_screen[surface].stats.health.setText(health_text, withDisplay=withDisplay)

        @staticmethod
        def getBonus(surface:str, number:int = 0):
            # Get game screen
            game_screen = screens.game

            health_text = game_screen[surface].stats.health.text

            if health_text.startswith('+ '): health_text = health_text[2:]
            else: logger.error('Error getting health.')

            return int(health_text)

        @staticmethod
        def get(surface:str):
            # Get game screen
            game_screen = screens.game

            health_text = game_screen[surface].stats.health.text.split('/')

            if len(health_text) != 2: logger.error('Error getting health, did you mean to getBonus()?')

            return (int(health_text[0]), int(health_text[1]))

    class power:

        @staticmethod
        def set(haveOrb:bool, withDisplay:bool = True):
            # Get game screen
            game_screen = screens.game

            if haveOrb: stats.power.take(withDisplay)
            else: stats.power.remove(withDisplay)

        @staticmethod
        def take(withDisplay:bool = True):
            # Get game screen
            game_screen = screens.game

            # Display the text
            orb_text = 'Orb of power'
            game_screen.info.stats.power.setText(orb_text, withDisplay=withDisplay)

        @staticmethod
        def remove(withDisplay:bool = True):
            # Get game screen
            game_screen = screens.game

            # Display the text
            orb_text = ''
            game_screen.info.stats.power.setText(orb_text, withDisplay=withDisplay)

        @staticmethod
        def hasOrb() -> bool:
            # Get game screen
            game_screen = screens.game

            # Output if player have orb of power
            return game_screen.info.stats.power.text == 'Orb of power'