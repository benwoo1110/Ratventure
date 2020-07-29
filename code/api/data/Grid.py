######################################
# Import and initialize the librarys #
######################################
from code.api.core import os, log, pg, coreFunc
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
        
        # Generate grid
        if gridData == None:
            # Create grid list
            self.tiles = [[None] * columns] * rows

            # Create grid of tiles
            for row in range(rows):
                for column in range(columns):
                    self.tiles[row][column] = Tile(row, column)
        
        else: self.tiles = gridData

    def load(self):
        # Get surface
        Surface = self.item.surface.Surface
        # Load up the grid with sprites
        for row in range(self.rows):
            for column in range(self.columns):
                tile = self.tiles[row][column]
                x = self.size * column + self.spacing * column
                y = self.size * row + self.spacing * row
                if tile.hasSprite(): Surface.blit(sprite.get(tile.sprites[0]), (self.frame.coord((x, y))))


class Tile(coreFunc):
    def __init__(self, row:int, column:int, sprites:list = ['orb']):
        self.row = row
        self.column = column
        self.sprites = sprites

    def hasSprite(self, sprite:str = None): 
        if sprite == None: return self.sprites != []
        else: return sprite in self.sprites