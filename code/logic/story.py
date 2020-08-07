######################################
# Import and initialize the librarys #
######################################
import random
from code.api.core import os, log, screens, coreFunc


#################
# Setup logging #
#################
filename = os.path.basename(__file__).split('.')[0]
logger = log.get_logger(filename)
logger.info('Loading up {}...'.format(filename))


# Story stuff
stories = {
    "in_town": [
        "You are in town.",
        "Welcome to the town!"
    ],
    "in_open": [
        "You are in the open.",
        "You are in the wild."
    ],
    "rest": [
        "You are fully healed.",
        "You have regained full health."
    ],
    "change_orb": [
        "HmMm the orb changed location. Should I sense it?",
    ],
    "sense_orb": [
        "You sense that the Orb of Power is to the {}.",
        "You smell the Orb of Power at the {}."
    ],
    "take_orb": [
        "You found the Orb of Power!",
    ],
    "save": [
        "Game saved."
    ],
    "encounter_wild": [
        "Encounter! - {}",
        "A wild {} appeared!"
    ],
    "encounter_king": [
        "Tada! The Rat King is here!",
        "The one and only - Rat King!"
    ],
    "attack": [
        "Hmm should I attack or run?"
    ],
    "hero_attack": [
        "You deal {} damage to the {}."
    ],
    "enemy_attack": [
        "Ouch! The {} hit you for {} damage.",
        "The {} hit you for {} damage.",
        "The {} hit you for {} damage. That hurts!"
    ],
    "immune": [
        "You do not have the Orb of Power - the Rat King is immune!"
    ],
    "run": [
        "You have ran and hide."
    ],
    "enemy_defeated": [
        "The {} is dead! You are victorious!",
        "Congratulations, you have defeated the {}!",
        "You have defeated the {}, congratulations!"
    ],
    "hero_defeated": [
        "You are dead. Game over."
    ],
    "win": [
        "The world is saved! You Win!"
    ],
}


##################
# Gameplay logic #
##################
class Story(coreFunc):
    def __init__(self, stories:dict):
        # Save stories
        self.stories = stories

        # Add all the story as attributess
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
story = Story(stories)