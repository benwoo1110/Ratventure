######################################
# Import and initialize the librarys #
######################################
import random
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
class Story(coreFunc):
    def __init__(self, stories:dict):
        # Save stories
        self.stories = stories

        # Add all the story as attributes
        for name, messages in stories.items():
            setattr(self, name, message(name, messages))

    def getCurrent(self) -> str:
        return screens.game.info.story.message.text

    def setCurrent(self, Message:str):
        screens.game.info.story.message.setText(Message)


class message(coreFunc):
    def __init__(self, name:str, messages:list):
        self.name = name
        self.messages = messages

    def display(self, *placeholder):
        # Show the selected story to game screen
        message = random.choice(self.messages)
        screens.game.info.story.message.setText(message.format(*placeholder))


# Get stories
story = Story(pg.loadJson('./gamefiles/stories.json'))