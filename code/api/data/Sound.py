######################################
# Import and initialize the librarys #
######################################
from code.api.core import log, coreFunc, os, pg, pygame, glob
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
        # Default fallback
        if sound_file == None: 
            self.soundfile = None
            return
        
        try: self.soundfile = pygame.mixer.Sound(sound_file)
        except: 
            self.soundfile = None
            logger.error('Error loading sound {}'.format(sound_file), exc_info=True)

    def play(self, maxtime:int = -1, loops:int = 0, withVolume:float = 1.0, fadetime:int = 0):
        # There was error loading sound file
        if self.soundfile == None: return
        
        # Play the sound
        self.soundfile.set_volume(withVolume*pg.config.sound.effects)
        self.soundfile.play(loops=loops, maxtime=maxtime, fade_ms=fadetime)

    def stop(self, fadetime:int = 0): 
        # There was error loading sound file
        if self.soundfile == None: return

        # Stop the sound with fading if any
        self.soundfile.fadeout(fadetime)

    def isPlaying(self) -> bool:
        # There was error loading sound file
        if self.soundfile == None: return

        # Check if sound is playing in any channel
        return self.soundfile.get_num_channels() >= 1


class soundHandler(coreFunc):
    def __init__(self, sound_dir:str = './sounds/', fileType:str = ''):
        self.sound_dir = sound_dir
        self.fileType = fileType
        self.containerList = ['_default']

        # Default fallback
        setattr(self, '_default', Effect(None))

        # Save sound file to attributes
        sound_files = self.getFilesList()
        for sound_file in sound_files:
            sound_name = os.path.basename(sound_file).split('.')[0]
            setattr(self, sound_name, Effect(sound_file))
            self.containerList.append(sound_name)

    def __getattr__(self, name): 
        try: return self.__dict__[name]
        except:
            logger.error('Error getting sound {}'.format(name), exc_info=True)
            return self.__dict__['_default']
    
    def getFilesList(self) -> list:
        # Define variables
        image_dir = os.path.join(self.sound_dir, '*'+self.fileType)
        # Get list of image from dir
        return glob.glob(image_dir)

Sound = soundHandler()