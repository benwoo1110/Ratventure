######################################
# Import and initialize the librarys #
######################################
from random import randint
from code.api.core import os, log, coreFunc
from code.api.data.Images import Images
from code.api.data.Frame import Frame
from code.logic.player import player


#################
# Setup logging #
#################
filename = os.path.basename(__file__).split('.')[0]
logger = log.get_logger(filename)
logger.info('Loading up {}...'.format(filename))


class Sprite(coreFunc):
    def __init__(self, spritePage:list):
        # Get sprite images
        images = Images(frame=Frame(x=0,y=0,w=101,h=101), imagePage=spritePage, scale=True)
        self.containerList = images.containerList

        # Load them to attributes
        for image in images.containerList:
            setattr(self, image, images[image])

    def types(self): return self.containerList

    def hasType(self, type:str): return str(type) in self.containerList

    def get(self, sprite:str):
        if sprite in self.containerList: return getattr(self, sprite)
        else: logger.error('No such sprite: "{}"'.format(sprite))

# Get sprites available
sprite = Sprite(spritePage=['game', 'map', 'sprites'])


class Grid(coreFunc):
    def __init__(self, frame:Frame, rows:int, columns:int, name:str = None, item:str = None, gridData:list = None):
        self.frame = frame
        self.rows = rows
        self.columns = columns
        self.name = name
        self.item = item

        # Set tile size
        self.spacing = 3
        self.size = 101
        
        # Get tiles
        self.generate()

    def generate(self, gridData:list = None):
        # Generate grid
        self.tiles = []

        # Create grid of tiles
        for row in range(self.rows):
            self.tiles.append([])
            for column in range(self.columns):
                if gridData == None: self.tiles[row].append(Tile(row, column))
                else: self.tiles[row].append(Tile(row, column, gridData[row][column]))

    def randomiseTowns(self, number:int = 4, spacing:int = 3):
        town_placed = 0
        spacing -= 1
        while town_placed < number:
            row = randint(0, 7)
            column = randint(0, 7)

            # Ensure that pos isnt a town or at king's location
            if self.tiles[row][column].hasSprite('town'): continue

            # Check if town in within 3 pos
            can_place = True
            for c in range(-spacing, spacing+1):
                for r in range(-(spacing-abs(c)), spacing-abs(c)+1):
                    # Ensure there is such a tile and is not itself and not at king location
                    if 0 <= row+r <= 7 and 0 <= column+c <= 7 and (r, c) != (7, 7):
                        if self.tiles[row+r][column+c].hasSprite():
                            can_place = False 
                            break
                if not can_place: break
            
            # Place down the town if checks pass
            if can_place: 
                self.tiles[row][column].sprites.append('town')
                town_placed += 1

    def clear(self): self.generate()
    
    def find(self, Sprite) -> tuple:
        for row in range(self.rows):
            for column in range(self.columns):
                if self.tiles[row][column].hasSprite(Sprite): return (row, column)

    def heroInTown(self):
        # Check if hero in town or open
        return self.tiles[player.hero.row][player.hero.column].hasSprite('town')

    def load(self):
        # Get surface
        Surface = self.item.surface.Surface

        # Load up the grid with sprites
        for row in range(self.rows):
            for column in range(self.columns):
                tile = self.tiles[row][column]
                x = self.size * column + self.spacing * column
                y = self.size * row + self.spacing * row
                for tile_sprite in tile.sprites:
                     Surface.blit(sprite.get(tile_sprite), (self.frame.coord((x, y))))

    def move(self, counter, row, column):
        # Get current hero location
        x = self.size * player.hero.column + self.spacing * player.hero.column
        y = self.size * player.hero.row + self.spacing * player.hero.row

        # Get new hero location, that hero is moving to
        new_x = self.size * column + self.spacing * column
        new_y = self.size * row + self.spacing * row

        # Calculate current animation position
        if x <= new_x: new_x = min(x+counter*3, new_x)
        else: new_x = max(x-counter*3, new_x)

        if y <= new_y: new_y = min(y+counter*3, new_y)
        else: new_y = max(y-counter*3, new_y)

        # Display to grid surface
        self.item.load()
        self.item.surface.Surface.blit(sprite.get('hero'), (self.frame.coord((new_x, new_y))))
        self.item.surface.display()   


class Tile(coreFunc):
    def __init__(self, row:int, column:int, sprites:list = None):
        self.row = row
        self.column = column
        
        if sprites == None: self.sprites = []
        else: self.sprites = sprites

    def getPos(self): return (self.row, self.column)

    def hasSprite(self, tile_sprite:str = None): 
        if tile_sprite == None: return self.sprites != []
        else: return tile_sprite in self.sprites