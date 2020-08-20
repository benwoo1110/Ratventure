######################################
# Import and initialize the librarys #
######################################
from code.api.core import os, log, screens, pg
from code.api.actions import Alert, Runclass
from code.logic.player import player
from code.logic.difficulty import difficulty
from code.api.data.Sound import Sound


#################
# Setup logging #
#################
filename = os.path.basename(__file__).split('.')[0]
logger = log.get_logger(filename)


##################
# Gameplay logic #
##################
class store:
    weapons = pg.loadJson('./gamefiles/weapons.json')

    @staticmethod
    def gainText(gain_data) -> tuple:
        if type(gain_data[1]) == list: stats = gain_data[1][1]
        else: stats = gain_data[1]

        return ('{}: '.format(gain_data[0].capitalize()), '+ {}'.format(stats))

    @staticmethod
    def setGain(gain_text, gain_data:list):
        # Set the text
        prefix, text = store.gainText(gain_data)
        gain_text.setText(prefix=prefix, text=text, withDisplay=False)

        # Set the text colour
        if gain_data[0] == 'defence': gain_text.format.colour = pg.colour.blue
        elif gain_data[0] == 'damage': gain_text.format.colour = pg.colour.red
        elif gain_data[0] == 'health': gain_text.format.colour = pg.colour.green

    @staticmethod
    def setWeapons():
        store.weapons = pg.loadJson('./gamefiles/weapons.json')
        store_surface = screens.shop.store

        # Get multiplier
        price_multiplier = difficulty.get()['price_multiplier']

        # Load up weapons stats to screen
        for name, weapon_data in store.weapons.items():
            if name in player.weapon.weapons:
                store_surface[name].price.setText('', withDisplay=False)
                store_surface[name].switchState('Disabled', False)
                continue

            else: store_surface[name].switchState('', False)

            # Set weapon text
            store_surface[name].object.setText(name.capitalize(), withDisplay=False)
            store_surface[name].price.setText(str(int(weapon_data['price'] * price_multiplier)), withDisplay=False)
            store.setGain(store_surface[name].gain_1, weapon_data['gain_1'])
            store.setGain(store_surface[name].gain_2, weapon_data['gain_2'])

            store_surface.load(withItems='all', refresh=True)

    @staticmethod
    def getPrice(weapon:str): return int(screens.shop.store[weapon].price.text)

    @staticmethod
    def checkBuy(weapon:str):
        # If player have enough elixir
        if player.stats.elixir >= store.getPrice(weapon):
            Alert(
                type = 'confirm',
                title = 'Buy {}'.format(weapon.capitalize()),
                content = 'Are you such you want to buy the {} for {} elixir?'.format(weapon.capitalize(), store.getPrice(weapon)),
                yes = Runclass(run=store.buy, parameters={'weapon': weapon})
            ).do()
        
        # Not enough elixir
        else:
            # Play error
            Sound.error.play()
            # Tell player
            Alert(
                type = 'notify',
                title = 'Awww Snap',
                content = 'You do not have enough elixir. This weapon requires {} elixir!'.format(store.getPrice(weapon)),
            ).do()

    @staticmethod
    def addGain(gain):
        player.stats.update(gain[0], gain[1], screens.shop.store.stats, True)

    @staticmethod
    def buy(weapon:str):
        # Pay the price
        player.stats.update('elixir', -store.getPrice(weapon),  screens.shop.store.stats, True)

        # Add gains to player stats
        store.addGain(store.weapons[weapon]['gain_1'])
        store.addGain(store.weapons[weapon]['gain_2'])

        # Show that weapon is bought
        screens.shop.store[weapon].price.setText('')
        screens.shop.store[weapon].switchState('Disabled')

        # Add weapon to weapons list
        player.weapon.add(weapon)

        # Play cool sound
        Sound.weapon_equip.play()

        # Alert users on the gains
        Alert(
            type = 'notify',
            title = 'Bought {}'.format(weapon.capitalize()),
            content = 'You gained {} {} and {} {}! You have {} elixir left.'.format(
                *store.gainText(store.weapons[weapon]['gain_1']),
                *store.gainText(store.weapons[weapon]['gain_2']),
                player.stats.elixir
            )
        ).do()

