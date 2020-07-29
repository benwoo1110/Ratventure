######################################
# Import and initialize the librarys #
######################################
from code.api.core import os, log, screens


#################
# Setup logging #
#################
filename = os.path.basename(__file__).split('.')[0]
logger = log.get_logger(filename)
logger.info('Loading up {}...'.format(filename))


class stats:

    class damage:

        @staticmethod
        def set(surface:str, item:str, min_d:int, max_d:int, withDisplay:bool = True):
            # Get game screen
            game_screen = screens.game

            # Display the text
            damage_text = '{} - {}'.format(min_d, max_d)
            game_screen[surface][item].damage.setText(damage_text, withDisplay=withDisplay)

        @staticmethod
        def update(surface:str, item:str, min_d:int, max_d:int, withDisplay:bool = True):
            # Get game screen
            game_screen = screens.game

            # Get value
            min_damage, max_damage = stats.damage.get(surface, item)

            # Set new value
            min_damage += min_d
            max_damage += max_d

            # Display the text
            damage_text = '{} - {}'.format(min_damage, max_damage)
            game_screen[surface][item].damage.setText(damage_text, withDisplay=withDisplay)

        @staticmethod  
        def get(surface:str, item:str) -> tuple:
            # Get game screen
            game_screen = screens.game

            # Get the damage text
            damage_text = game_screen[surface][item].damage.text
            min_damage, max_damage = damage_text.split(' - ')

            return (int(min_damage), int(max_damage))

    class defence:

        @staticmethod
        def set(surface:str, item:str, number:int, withDisplay:bool = True):
            # Get game screen
            game_screen = screens.game

            # Display the text
            game_screen[surface][item].defence.setText(str(number), withDisplay=withDisplay)

        @staticmethod
        def update(surface:str, item:str, number:int, withDisplay:bool = True):
            # Get game screen
            game_screen = screens.game

            # Get value
            new_defence = str(stats.defence.get(surface, item) + number)

            # Display the text
            game_screen[surface][item].defence.setText(new_defence, withDisplay=withDisplay)

        @staticmethod
        def get(surface:str, item:str):
            # Get game screen
            game_screen = screens.game

            return int(game_screen[surface][item].defence.text)

    class health:

        @staticmethod
        def set(surface:str, item:str, current:int = 0, max:int = 0, withDisplay:bool = True):
            # Get game screen
            game_screen = screens.game

            # Display the text
            health_text = '{}/{}'.format(current, max)
            game_screen[surface][item].health.setText(health_text, withDisplay=withDisplay)

        
        @staticmethod
        def update(surface:str, item:str, current:int = 0, max:int = 0, withDisplay:bool = True):
            # Get game screen
            game_screen = screens.game

            # Get value
            current_health, max_health = stats.health.get(surface, item)

            # Set new value
            current_health += current
            max_health += max

            # Display the text
            health_text = '{}/{}'.format(current_health, max_health)
            game_screen[surface][item].health.setText(health_text, withDisplay=withDisplay)

        @staticmethod
        def setBonus(surface:str, item:str, number:int, withDisplay:bool = True):
            # Get game screen
            game_screen = screens.game
            
            # Set new value
            health_text = '+ {}'.format(number)

            # Display the text
            game_screen[surface][item].health.setText(health_text, withDisplay=withDisplay)

        @staticmethod
        def getBonus(surface:str, item:str, number:int = 0):
            # Get game screen
            game_screen = screens.game

            health_text = game_screen[surface][item].health.text

            if health_text.startswith('+ '): health_text = health_text[2:]
            else: logger.error('Error getting health.')

            return int(health_text)

        @staticmethod
        def get(surface:str, item:str):
            # Get game screen
            game_screen = screens.game

            health_text = game_screen[surface][item].health.text.split('/')

            if len(health_text) != 2: logger.error('Error getting health, did you mean to getBonus()?')

            return (int(health_text[0]), int(health_text[1]))

    class power:

        @staticmethod
        def set(surface:str, item:str, haveOrb:bool, withDisplay:bool = True):
            # Get game screen
            game_screen = screens.game

            if haveOrb: stats.power.take(surface, item, withDisplay)
            else: stats.power.remove(surface, item, withDisplay)

        @staticmethod
        def take(surface:str, item:str, withDisplay:bool = True):
            # Get game screen
            game_screen = screens.game

            # Display the text
            orb_text = 'Orb of power'
            game_screen[surface][item].power.setText(orb_text, withDisplay=withDisplay)

        @staticmethod
        def remove(surface:str, item:str, withDisplay:bool = True):
            # Get game screen
            game_screen = screens.game

            # Display the text
            orb_text = ''
            game_screen[surface][item].power.setText(orb_text, withDisplay=withDisplay)

        @staticmethod
        def hasOrb(surface:str, item:str) -> bool:
            # Get game screen
            game_screen = screens.game

            orb_text = game_screen[surface][item].power.text

            return len(orb_text) == 'Orb of power'