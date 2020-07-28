######################################
# Import and initialize the librarys #
######################################
from code.api.core import log, coreFunc, os, pygame, glob
from code.api.data.Frame import Frame


#################
# Setup logging #
#################
filename = os.path.basename(__file__).split('.')[0]
logger = log.get_logger(filename)
logger.info('Loading up {}...'.format(filename))


class Images(coreFunc):
    def __init__(self, imagePage:list, frame:Frame, fileType:str = '.png'):
        self.imagePage = imagePage
        self.fileType = fileType
        self.frame = frame
        self.containerList = []
        self.get()

    def getFilesList(self) -> list:
        # Define variables
        image_dir = os.path.join('surfaces', *self.imagePage, '*'+self.fileType)
        # Get list of image from dir
        return glob.glob(image_dir)

    def get(self):
        self.image_dir_list = self.getFilesList()
        # get the image
        for image in self.image_dir_list:
            # Get name
            image_name = os.path.basename(image).split('.')[0]
            # Load image
            image_surface = pygame.image.load(image).convert_alpha()
            # Store image
            self.__dict__[image_name] = image_surface
            self.containerList.append(image_name)