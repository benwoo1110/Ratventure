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


class Sprite(coreFunc):
    def __init__(self, spritePage:list, size:tuple, alpha:bool = True):
        # Get sprite images
        images = Images(frame=Frame(x=0,y=0,w=size[0],h=size[1]), imagePage=spritePage, scale=True, alpha=alpha)
        self.containerList = images.containerList

        # Load them to attributes
        for image in images.containerList:
            setattr(self, image, images[image])

    def types(self): return self.containerList

    def hasType(self, type:str): return str(type) in self.containerList

    def get(self, sprite:str):
        if sprite in self.containerList: return getattr(self, sprite)
        else: logger.error('No such sprite: "{}"'.format(sprite))
