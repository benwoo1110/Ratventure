######################################
# Import and initialize the librarys #
######################################
from code.api.core import os, log, screens, coreFunc, pg


#################
# Setup logging #
#################
filename = os.path.basename(__file__).split('.')[0]
logger = log.get_logger(filename)
logger.info('Loading up {}...'.format(filename))


##################
# Gameplay logic #
##################
class Player(coreFunc):
    def __init__(self, nickname:str, difficulty:str, damage:list, defence:int, 
    health:list, elixir:int, weapons:list, row:int, column:int,  fileid:str = None):
        self.nickname = nickname
        self.difficulty = difficulty
        self.damage = damage
        self.defence = defence
        self.health = health
        self.elixir = elixir
        self.weapons = weapons
        self.row = row
        self.column = column
        self.fileid = fileid

class player:
    data = None