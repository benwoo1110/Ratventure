######################################
# Import and initialize the librarys #
######################################
import logging
import yaml
import os


# Default setting for file
default_config_contents = '''\
#########################
# Ratventure config.yml #
#########################

# NOTE: Change only if you know what you are doing!

# Window caption
title: 'Ratventure'

# Application icon file location
icon_file: './icon.png'

# Pygame windows fills the entire screen
fullscreen: False

# Config size of pygame window (Only apply if not fullscreen)
scale: 0.6

# Level of output shown
# CRITICAL -> 50
# ERROR -> 40
# WARNING -> 30
# INFO -> 20
# DEBUG -> 10
logging:
  # For console output
  console_level: 'INFO'
  # App activities logged in './Ratventure/logs/'
  file_level: 'DEBUG'
  # Number of logs to keep in logs folder
  keep_logs: 5

# Changes the refresh rate of pygame
framerate: 60
'''


##########################
# Getting configurations #
##########################
config_dir = './config.yml'
if os.path.basename(os.getcwd()) == 'code': config_dir = '../config.yml'

# Create file if it doesnt exist
if not os.path.isfile(config_dir):
    with open(config_dir, 'w') as config_file:
        config_file.write(default_config_contents)
        print("Generated ./config.yml")

# Read from config file
with open(config_dir) as config_file:
    parsed_config_file = yaml.load(config_file, Loader=yaml.FullLoader)
    config_file.close()


###########################
# Loading config to class #
###########################
class Struct:
    def __init__(self, **response):
        for k,v in response.items():
            if isinstance(v,dict):
                self.__dict__[k] = Struct(**v)
            else:
                self.__dict__[k] = v

    def __repr__(self): return '{}'.format(self.__dict__)


# Convert dict to class object
class config:
    @staticmethod
    def get() -> Struct:
        return Struct(**parsed_config_file)