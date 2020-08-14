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


# Try to start sound mixer
try: pygame.mixer.init()
except: logger.error('Error initialising pygame sound... Sound effects will not work!', exc_info=True)


class Effect(coreFunc):
    def __init__(self, sound_file):
        try: self.soundfile = pygame.mixer.Sound(sound_file)
        except: self.soundfile = None

    def play(self): 
        if self.soundfile != None: self.soundfile.play()


class soundHandler(coreFunc):
    def __init__(self, sound_dir:str = './sounds/', fileType:str = ''):
        self.sound_dir = sound_dir
        self.fileType = fileType

        # Save sound file to attributes
        sound_files = self.getFilesList()
        for sound_file in sound_files:
            sound_name = os.path.basename(sound_file).split('.')[0]
            try: setattr(self, sound_name, Effect(sound_file))
            except: logger.error('Error loading sound {}'.format(sound_file), exc_info=True)
    
    def getFilesList(self) -> list:
        # Define variables
        image_dir = os.path.join(self.sound_dir, '*'+self.fileType)
        # Get list of image from dir
        return glob.glob(image_dir)

Sound = soundHandler()