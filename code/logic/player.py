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


##################
# Gameplay logic #
##################
class Player:
    nickname = ''
    difficulty = ''
    stats = None
    weapon = None
    hero = None
    orb = None
    fileid = None

    @staticmethod
    def reset():
        Player.nickname = screens.new_game.options.nickname.text.text
        Player.difficulty = screens.new_game.options.difficulty.mode.text
        Player.stats = Stats (
            day = 1,
            damage = [2, 4],
            defence = 1, 
            health = [20, 20],
            elixir = 0
        )
        Player.weapon = Weapon()
        Player.hero = Location(row=0, column=0)
        Player.orb = Location(row=0, column=0)
        Player.fileid = None

    @staticmethod
    def get() -> dict():
        return {
            'nickname': Player.nickname,
            'difficulty': Player.difficulty,
            'stats': Player.stats.__dict__.copy(),
            'weapon': Player.weapon.__dict__.copy(),
            'hero': Player.hero.__dict__.copy(),
            'orb': Player.orb.__dict__.copy()
        }

    @staticmethod
    def load(data:dict):
        Player.nickname = data['nickname']
        Player.difficulty = data['difficulty']
        Player.stats = Stats(**data['stats'])
        Player.weapon = Weapon(**data['weapon'])
        Player.hero = Location(**data['hero'])
        Player.orb = Location(**data['orb'])
        Player.fileid = data['fileid']

    @staticmethod
    def next_day():
        Player.stats.update('day', 1, screens.game.info.days, True)
