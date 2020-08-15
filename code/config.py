######################################
# Import and initialize the librarys #
######################################
import yaml
import os
import traceback


###################
# Default setting #
###################
default_config_contents = '''\
# +-+-+-+-+-+-+-+-+-+-+-+-+
# | Ratventure config.yml |
# +-+-+-+-+-+-+-+-+-+-+-+-+
# NOTE: Change only if you know what you are doing!


# +-+-+-+-+-+-+-+-+-+-+-+
# | Pygame GUI Settings |
# +-+-+-+-+-+-+-+-+-+-+-+
# Changes the refresh rate of pygame
framerate: 60

# Window caption
title: 'Ratventure'

# Application icon file location
icon_file: './icon.png'

# Pygame windows fills the entire screen
fullscreen: False

# Config size of pygame window (Only apply if not fullscreen)
scale: 0.6


# +-+-+-+-+-+-+-+-+-+
# | Sounds Settings |
# +-+-+-+-+-+-+-+-+-+
sound:
    # Master volume for all effects
    effects: 1.0

    # Volume range from 0 to 1.0 inclusive, with 1.0 being the loudest
    button: 0.12
    background: 0.12


# +-+-+-+-+-+-+-+-+-+
# | Logger Settings |
# +-+-+-+-+-+-+-+-+-+
# CRITICAL -> 50
# ERROR -> 40
# WARNING -> 30
# INFO -> 20
# DEBUG -> 10

logging:
  # For console output
  console_level: 'DEBUG'

  # App activities logged in './Ratventure/logs/'
  file_level: 'DEBUG'

  # Number of logs to keep in logs folder
  keep_logs: 5
'''


###########################
# Loading config to class #
###########################
class Struct:
    def __init__(self, **response):
        for key,value in response.items():
            if isinstance(value, dict): setattr(self, key, Struct(**value))
            else: setattr(self, key, value)

    def __repr__(self): return '{}'.format(self.__dict__)


##################
# Config actions #
##################
class config:
    file_dir = './config.yml'

    @staticmethod
    def check():
        # Create file if it doesnt exist
        if not os.path.isfile(config.file_dir):
            with open(config.file_dir, 'w') as config_file:
                config_file.write(default_config_contents)
                print("Generated new ./config.yml")

    @staticmethod
    def get() -> Struct:
        try:
            # Read from config file
            with open(config.file_dir) as config_file:
                parsed_config_file = yaml.load(config_file, Loader=yaml.FullLoader)
                config_file.close()

        except FileNotFoundError: 
            # File not found, run check to create new one
            print('Config not found, trying to create a new one...')
            config.check()

            # Try again
            with open(config.file_dir) as config_file:
                parsed_config_file = yaml.load(config_file, Loader=yaml.FullLoader)
                config_file.close()

        except:
            traceback.print_exc()
            # Possible issue with yaml file formating, try reset config
            print('Config seem broken, renaming it to ./config_broken.yml')
            os.rename(config.file_dir, './config_broken.yml')
            config.check()

            # Try again
            with open(config.file_dir) as config_file:
                parsed_config_file = yaml.load(config_file, Loader=yaml.FullLoader)
                config_file.close()

        # Load config dict to a structured class
        return Struct(**parsed_config_file)


###################
# Checking config #
###################
config.check()