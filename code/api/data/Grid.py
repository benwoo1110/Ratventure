######################################
# Import and initialize the librarys #
######################################
from code.api.core import os, log, coreFunc
from code.api.data.Images import Images
from code.api.data.Frame import Frame


#################
# Setup logging #
#################
filename = os.path.basename(__file__).split('.')[0]
logger = log.get_logger(filename)
logger.info('Loading up {}...'.format(filename))


class Sprite(coreFunc):
    def __init__(self):
        # Get sprite images
        images = Images(frame=Frame(x=0,y=0,w=101,h=101), imagePage=['game', 'map', 'sprites'], scale=True)
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
sprite = Sprite()


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

    def clear(self): self.generate()
    
    def find(self, Sprite) -> tuple:
        for row in range(self.rows):
            for column in range(self.columns):
                if self.tiles[row][column].hasSprite(Sprite): return (row, column)

    def heroInTown(self):
        # Get hero's position
        hero_r, hero_c = self.find('hero')

        # Check if hero in town or open
        return self.tiles[hero_r][hero_c].hasSprite('town')

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