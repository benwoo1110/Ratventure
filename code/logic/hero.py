######################################
# Import and initialize the librarys #
######################################
from code.api.core import os, log, screens
from code.logic.stats import stats


#################
# Setup logging #
#################
filename = os.path.basename(__file__).split('.')[0]
logger = log.get_logger(filename)
logger.info('Loading up {}...'.format(filename))


##################
# Gameplay logic #
##################
class hero:
    row = 0
    column = 0

    @staticmethod
    def resetStats():
        stats.day.set(1, False)
        stats.damage.set('info', 2, 4, False)
        stats.defence.set('info', 1, False)
        stats.health.set('info', 20, 20, False)
        stats.power.set(False, False)

    @staticmethod
    def setStats(stats_data:dict):
        stats.day.set(stats_data['day'], False)
        stats.damage.set('info', *stats_data['damage'], False)
        stats.defence.set('info', stats_data['defence'], False)
        stats.health.set('info', *stats_data['health'], False)
        stats.power.set(stats_data['power'], False)
    
    @staticmethod
    def getStats() -> dict:
        stats_data = dict()

        stats_data['day'] = stats.day.get()
        stats_data['damage'] = stats.damage.get('info')
        stats_data['defence'] = stats.defence.get('info')
        stats_data['health'] = stats.health.get('info')
        stats_data['power'] = stats.power.hasOrb()

        return stats_data