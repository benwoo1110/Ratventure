######################################
# Import and initialize the librarys #
######################################
from code.api.core import os, log, screens, PgEss
from code.api.actions import Alert, Runclass
from code.logic.player import Player
from code.logic.difficulty import Difficulty
from code.api.data.Sound import Sound


#################
# Setup logging #
#################
filename = os.path.basename(__file__).split('.')[0]
logger = log.get_logger(filename)


##################
# Gameplay logic #
##################
class Store:
    weapons = PgEss.loadJson('./gamefiles/weapons.json')

    @staticmethod
    def gainText(gain_data) -> tuple:
        if type(gain_data[1]) == list: stats = gain_data[1][1]
        else: stats = gain_data[1]

        return ('{}: '.format(gain_data[0].capitalize()), '+ {}'.format(stats))

    @staticmethod
    def setGain(gain_text, gain_data:list):
        # Set the text
        prefix, text = Store.gainText(gain_data)
        gain_text.setText(prefix=prefix, text=text, withDisplay=False)

        # Set the text colour
        if gain_data[0] == 'defence': gain_text.format.colour = PgEss.colour.blue
        elif gain_data[0] == 'damage': gain_text.format.colour = PgEss.colour.red
        elif gain_data[0] == 'health': gain_text.format.colour = PgEss.colour.green

    @staticmethod
    def setWeapons():
        Store.weapons = PgEss.loadJson('./gamefiles/weapons.json')
        store_surface = screens.shop.store

        # Get multiplier
        price_multiplier = Difficulty.get()['price_multiplier']

        # Load up weapons stats to screen
        for name, weapon_data in Store.weapons.items():
            if name in Player.weapon.weapons:
                store_surface[name].price.setText('', withDisplay=False)
                store_surface[name].switchState('Disabled', False)
                continue

            else: store_surface[name].switchState('', False)

            # Set weapon text
            store_surface[name].object.setText(name.capitalize(), withDisplay=False)
            store_surface[name].price.setText(str(int(weapon_data['price'] * price_multiplier)), withDisplay=False)
            Store.setGain(store_surface[name].gain_1, weapon_data['gain_1'])
            Store.setGain(store_surface[name].gain_2, weapon_data['gain_2'])

            store_surface.load(withItems='all', refresh=True)

    @staticmethod
    def getPrice(weapon:str): return int(screens.shop.store[weapon].price.text)

    @staticmethod
    def checkBuy(weapon:str):
        # If player have enough elixir
        if Player.stats.elixir >= Store.getPrice(weapon):
            Alert(
                type = 'confirm',
                title = 'Buy {}'.format(weapon.capitalize()),
                content = 'Are you such you want to buy the {} for {} elixir?'.format(weapon.capitalize(), Store.getPrice(weapon)),
                yes = Runclass(run=Store.buy, parameters={'weapon': weapon})
            ).do()
        
        # Not enough elixir
        else:
            # Play error
            Sound.error.play()
            # Tell player
            Alert(
                type = 'notify',
                title = 'Awww Snap',
                content = 'You do not have enough elixir. This weapon requires {} elixir!'.format(Store.getPrice(weapon)),
            ).do()

    @staticmethod
    def addGain(gain):
        Player.stats.update(gain[0], gain[1], screens.shop.store.stats, True)

    @staticmethod
    def buy(weapon:str):
        # Pay the price
        Player.stats.update('elixir', -Store.getPrice(weapon),  screens.shop.store.stats, True)

        # Add gains to player stats
        Store.addGain(Store.weapons[weapon]['gain_1'])
        Store.addGain(Store.weapons[weapon]['gain_2'])

        # Show that weapon is bought
        screens.shop.store[weapon].price.setText('')
        screens.shop.store[weapon].switchState('Disabled')

        # Add weapon to weapons list
        Player.weapon.add(weapon)

        # Play cool sound
        Sound.weapon_equip.play()

        # Alert users on the gains
        Alert(
            type = 'notify',
            title = 'Bought {}'.format(weapon.capitalize()),
            content = 'You gained {} {} and {} {}! You have {} elixir left.'.format(
                *Store.gainText(Store.weapons[weapon]['gain_1']),
                *Store.gainText(Store.weapons[weapon]['gain_2']),
                Player.stats.elixir
            )
        ).do()

