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


class Images(coreFunc):
    def __init__(self, imagePage:list, frame:Frame, fileType:str = '.png', scale:bool = False, alpha:bool = False):
        self.imagePage = imagePage
        self.fileType = fileType
        self.frame = frame
        self.alpha = alpha
        self.containerList = []
        self.scale = scale
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
            if self.alpha: loaded_image = pygame.image.load(image).convert_alpha()
            else: loaded_image = pygame.image.load(image).convert()

            # With scaling
            if self.scale:
                # Load surface
                if self.alpha: image_surface = pygame.surface.Surface(self.frame.size(), pygame.SRCALPHA)
                else: image_surface = pygame.surface.Surface(self.frame.size()) 

                # Width or height is larger, get scale
                w, h = loaded_image.get_size()
                if w > h: scale_factor = self.frame.w / w
                else: scale_factor = self.frame.h / h

                # Scale surface
                loaded_image = pygame.transform.smoothscale(loaded_image, (int(w * scale_factor), int(h * scale_factor)))
                w, h = loaded_image.get_size()
                
                # Load to image surface
                image_surface.blit(loaded_image, ((int(self.frame.w-w)/2), (int(self.frame.h-h)/2)))
            
            else: image_surface = loaded_image

            # Store image
            setattr(self, image_name, image_surface)
            self.containerList.append(image_name)