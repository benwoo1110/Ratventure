######################################
# Import and initialize the librarys #
######################################
from random import randint
from code.api.core import os, log, screens, coreFunc, pg
from code.api.events import gameEvent
from code.api.actions import Runclass


#################
# Setup logging #
#################
filename = os.path.basename(__file__).split('.')[0]
logger = log.get_logger(filename)
logger.info('Loading up {}...'.format(filename))


##################
# Gameplay logic #
##################
class Stats(coreFunc):
    def __init__(self, day:int = None, damage:list = None, defence:int = None, health:list = None, elixir:int = None):
        self.day = day
        self.damage = damage
        self.defence = defence
        self.health = health
        self.elixir = elixir

    def isFullHealth(self):
        if self.health == None: return
        return self.health[0] >= self.health[1]

    def multiply(self, multiplier:int):
        for name, value in self.__dict__.items():
            if value != None:
                if type(value) == list: 
                    for i in range(len(value)): value[i] = int(value[i] * multiplier)
                else:
                    value = int(value * multiplier)

                setattr(self, name, value)

    def calDamage(self, defence:int = 0):
        if self.damage != None: return max(0, randint(*self.damage) - defence)

    def addBonus(self, bonus, item, withDisplay:bool = False, animate = None):
        for name, by in bonus.__dict__.items():
            if by != None: self.update(name, by, item, withDisplay, animate)

    def update(self, name:str, by, item, withDisplay:bool = False, animate = None):
        # For damage
        if name == 'damage':
            self.damage[0] += by[0]
            self.damage[1] += by[1]

        # For health
        elif name == 'health':
            self.health[0] = max(0, self.health[0] + by[0])
            self.health[1] += by[1]

        # The rest
        else: 
            setattr(self, name, getattr(self, name) + by)

            # Check for change orb day
            if name == 'day': gameEvent.orb_change.call()

        # Display change
        if animate == None: self.display(name, item, withDisplay)
        
        # If animate instead
        else: 
            # Add stats animation to queue
            gameEvent.stats.addQueue(
                Runclass(run=self.animate, parameters={'name': name, 'by': by, 'item': item, 'animate': animate})
            )

    def animate(self, counter:int, name:str, by, item, animate):
        if counter == 0:
            # Generate the text to display
            if type(by) == list: 
                if by[1] != 0: text = by[1]
                else: text = by[0]
            else: text = by

            # Adding polarity sign (+/-)
            if text <= 0: text = '- {}'.format(abs(text))
            else: text = '+ {}'.format(text)

            # Set text colour to represent the stats type
            if name == 'damage': animate.stats.format.colour = pg.colour.red
            elif name == 'defence': animate.stats.format.colour = pg.colour.blue
            elif name == 'health': animate.stats.format.colour = pg.colour.green
            elif name == 'elixir': animate.stats.format.colour = pg.colour.purple
            else: animate.stats.format.colour = pg.colour.white

            animate.stats.setText(text, withDisplay=False)

        # Pop out
        elif counter <= 30:
            animate.stats.format.modifyFont(fontSize=counter*2)
            animate.display(withData='all')

        # Pop back abit
        elif counter <= 34:
            animate.stats.format.modifyFont(fontSize=60-(counter-31)*2)
            animate.display(withData='all')

        # Show the updated stats
        elif counter == 35: self.display(name, item, True)

        # Pop out
        elif 100 < counter <= 126: 
            animate.stats.format.modifyFont(fontSize=52-(counter-100)*2)
            animate.display(withData='all')

        # Animation ended 
        elif counter > 126: 
            animate.stats.setText('')
            return True

    def set(self, name:str, to, item, withDisplay:bool = False):
        # Set the new stats
        setattr(self, name, to)
        self.display(name, item, withDisplay)
    
    def display(self, name:str, item, withDisplay:bool = False):
        # Generate the text
        if name == 'damage': text = str('{} - {}'.format(*self.damage))
        elif name == 'health': text = str('{}/{}'.format(*self.health))
        else: text = str('{}'.format(getattr(self, name)))

        # Display to stats screen
        item[name].setText(text, withDisplay=withDisplay)


class Bonus(coreFunc):
    def __init__(self, damage:list = None, defence:int = None, health:list = None, elixir:int = None):
        self.damage = damage
        self.defence = defence
        self.health = health
        self.elixir = elixir

    def set(self, name:str, to, item, withDisplay:bool = False, index:int = 1):
        # Set the new stats
        setattr(self, name, to)
        self.display(name, item, withDisplay, index)

    def display(self, name:str, item = None, withDisplay:bool = False, index:int = 1):
        stats = getattr(self, name)
        # Generate teh text to display
        if type(stats) == list: text = str('+ {}'.format(stats[index]))
        else: text = str('+ {}'.format(stats))

        # Display to stats screen
        item[name].setText(text, withDisplay=withDisplay)


class Location(coreFunc):
    def __init__(self, row, column):
        self.row = row
        self.column = column

    def pos(self): return (self.row, self.column)

    def setNew(self, pos:tuple):
        self.row = pos[0]
        self.column = pos[1]


class Weapon(coreFunc):
    def __init__(self, weapons:list = None):
        self.weapons = []

        # Reset weapon grid
        screens.game.info.hero.weapons.generate()
        
        # Set weapons to display in grid
        if weapons != None: 
            for weapon in weapons: self.add(weapon, False)
       
        screens.game.info.load(withItems=['hero'], refresh=True)

    def have(self, weapon:str): return weapon in self.weapons

    def add(self, weapon:str, withLoad:bool = True): 
        # Add to weapon list
        self.weapons.append(weapon)

        # Add to gui grid
        number_of_weapons = len(self.weapons)
        row = number_of_weapons // 2
        column = number_of_weapons % 2

        screens.game.info.hero.weapons.tiles[row][column].sprites.append(weapon)
        if withLoad: screens.game.info.load(withItems=['hero'], refresh=True)