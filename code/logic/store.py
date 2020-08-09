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
class store:
    weapons = pg.loadJson('./gamefiles/weapons.json')

    @staticmethod
    def setGain(gain_text, gain_data:list):
        # Set the text
        prefix = '{}: '.format(gain_data[0].capitalize())
        gain_text.setText(prefix=prefix, text=str(gain_data[1]), withDisplay=False)

        # Set the text colour
        if gain_data[0] == 'defence': gain_text.format.colour = pg.colour.blue
        elif gain_data[0] == 'damage': gain_text.format.colour = pg.colour.red
        elif gain_data[0] == 'health': gain_text.format.colour = pg.colour.green

    @staticmethod
    def setWeapons(bought:list = None):
        store_surface = screens.shop.store

        # Reset bought
        if bought != None: store.bought = []
        else: store.bought = bought

        # Load up weapons stats to screen
        for name, weapon_data in store.weapons.items():
            # Set weapon text
            store_surface[name].object.setText(name.capitalize(), withDisplay=False)
            store_surface[name].price.setText(str(weapon_data['price']), withDisplay=False)
            store.setGain(store_surface[name].gain_1, weapon_data['gain_1'])
            store.setGain(store_surface[name].gain_2, weapon_data['gain_2'])

            store_surface[name].switchState('', False)
            store_surface.load(withItems='all', refresh=True)