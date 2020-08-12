######################################
# Import and initialize the librarys #
######################################
from code.api.core import os, log, screens, coreFunc
from code.logic.stats import Stats, Location, Weapon


#################
# Setup logging #
#################
filename = os.path.basename(__file__).split('.')[0]
logger = log.get_logger(filename)
logger.info('Loading up {}...'.format(filename))


##################
# Gameplay logic #
##################
class player:
    nickname = ''
    difficulty = ''
    stats = None
    weapon = None
    hero = None
    orb = None
    fileid = None

    @staticmethod
    def reset():
        player.nickname = screens.new_game.options.nickname.text.text
        player.difficulty = screens.new_game.options.difficulty.mode.text
        player.stats = Stats (
            day = 1,
            damage = [2, 4],
            defence = 1, 
            health = [20, 20],
            elixir = 0
        )
        player.weapon = Weapon()
        player.hero = Location(row=0, column=0)
        player.orb = Location(row=0, column=0)
        player.fileid = None

    @staticmethod
    def get() -> dict():
        return {
            'nickname': player.nickname,
            'difficulty': player.difficulty,
            'stats': player.stats.__dict__.copy(),
            'weapon': player.weapon.__dict__.copy(),
            'hero': player.hero.__dict__.copy(),
            'orb': player.orb.__dict__.copy()
        }

    @staticmethod
    def load(data:dict):
        player.nickname = data['nickname']
        player.difficulty = data['difficulty']
        player.stats = Stats(**data['stats'])
        player.weapon = Weapon(**data['weapon'])
        player.hero = Location(**data['hero'])
        player.orb = Location(**data['orb'])
        player.fileid = data['fileid']

    @staticmethod
    def next_day():
        player.stats.update('day', 1, screens.game.info.days, True)