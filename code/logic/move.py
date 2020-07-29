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


class move:
    pass

