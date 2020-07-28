######################################
# Import and initialize the librarys #
######################################
from code.api.core import log, coreFunc, os, screens


#################
# Setup logging #
#################
filename = os.path.basename(__file__).split('.')[0]
logger = log.get_logger(filename)
logger.info('Loading up {}...'.format(filename))


########################
# Click action classes #
########################
class Info(coreFunc):
    def __init__(self, text:str):
        self.text = text


class Runclass(coreFunc):
    def __init__(self, run:any, parameters:dict = {}):
        self.run = run
        self.parameters = parameters


class Switchscreen(coreFunc):
    def __init__(self, type:str, screen:str = None):
        self.type = type
        self.screen = screen


###########################
# Keyboard action classes #
###########################
class keyboardActions(coreFunc):
    def __init__(self, screen, actions:dict):
        self.screen = screen

        # Add keyboard actions
        self.containerList = []
        for name, action_data in actions.items():
            self.add(name, action_data)
            self.containerList.append(name)

    def add(self, name, data):
        self.__dict__[name] = key(self.screen, name, **data)


class key(coreFunc):
    def __init__(self, screen, name, keys:list, action:any, onKey:str = 'down', useAscii:bool = True):
        self.screen = screen
        self.name = name
        self.keys = keys
        self.onKey = onKey
        self.useAscii = useAscii
        self.action = action


##########################
# Action outcome classes #
##########################
class actionResult(coreFunc):
    def __init__(self, name:str, type:str, outcome:any = None): 
        self.name = name
        self.type = str(type)
        self.outcome = outcome

    def getOutcome(self, object_thing):
        action = object_thing.action
        try:
            # Just passing of information
            if isinstance(action, Info): self.outcome = action.text
            # Run a method
            elif isinstance(action, Runclass): self.outcome = action.run(**action.parameters)
            # Change of screen
            elif isinstance(action, Switchscreen): self.outcome = screens.changeStack(action.type, action.screen)
        
        # There is a error
        except Exception as e: logger.error(e, exc_info=True)

    def isName(self, name = None) -> bool: return self.name == name

    def isType(self, type = None) -> bool: return self.type == type

    def withOutcome(self, outcome = None) -> bool: return self.outcome == outcome