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


class soundHandler(coreFunc):
    def __init__(self, sound_dir:str = './sounds/', fileType:str = '.mp3'):
        self.sound_dir = sound_dir
        self.fileType = fileType

        # Save sound file to attributes
        sound_files = self.getFilesList()
        for sound_file in sound_files:
            sound_name = os.path.basename(sound_file).split('.')[0]
            setattr(self, sound_name, pygame.mixer.Sound(sound_file))
    
    def getFilesList(self) -> list:
        # Define variables
        image_dir = os.path.join(self.sound_dir, '*'+self.fileType)
        # Get list of image from dir
        return glob.glob(image_dir)

Sound = soundHandler()