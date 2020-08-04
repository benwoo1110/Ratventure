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

    def do(self):
        logger.info('{}'.format(self.text))
        return self.text


class Runclass(coreFunc):
    def __init__(self, run:any, parameters:dict = {}):
        self.run = run
        self.parameters = parameters

    def do(self):
        # Run the function if possible
        if callable(self.run): return self.run(**self.parameters)
        else: raise Exception('Function {} not callable.'.format(self.run))


class Alert(coreFunc):
    def __init__(self, type:str, title:str, content:str, ok:any = None, no:any = None, yes:any = None, dismiss:any = None):
        self.type = str(type)
        self.title = title
        self.content = content
        self.ok = ok
        self.no = no
        self.yes = yes
        self.dismiss = dismiss

    def do(self):
        # Unload first
        screens.alert.unload()

        # Update the action for alert button
        screens.alert.unload()

        # Check type of alert to load
        if self.type == 'confirm': 
            # Set messages
            screens.alert.confirm.message.title.setText(self.title, withDisplay=False)
            screens.alert.confirm.message.content.setText(self.content, withDisplay=False)

            # Set actions
            screens.alert.confirm.no.action = self.no
            screens.alert.confirm.yes.action = self.yes
            screens.alert.keyboard.dismiss.action = self.dismiss

            screens.alert.confirm.load(withItems=['message'], refresh=True)

        
        elif self.type == 'notify':
            # Set messages
            screens.alert.notify.message.title.setText(self.title, withDisplay=False)
            screens.alert.notify.message.content.setText(self.content, withDisplay=False)

            # Set actions
            screens.alert.notify.ok.action = self.ok
            screens.alert.keyboard.dismiss.action = self.dismiss            
            
            screens.alert.notify.load(withItems=['message'], refresh=True)

        # Go to alert screen
        return screens.changeStack(type='load', screen='alert')


class Switchscreen(coreFunc):
    def __init__(self, type:str, screen:str = None):
        self.type = type
        self.screen = screen
    
    def do(self):
         return screens.changeStack(self.type, self.screen)


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
        # Check if have action
        if object_thing.action == None: return

        # A list of actions
        if type(object_thing.action) == list:
            self.outcome = []
            # Run through all the laction
            for action in object_thing.action:
                # Run the action
                try: self.outcome.append(action.do())
                # There is a error
                except Exception as e: logger.error(e, exc_info=True)

        else:
            # Run the action
            try: self.outcome = object_thing.action.do()
            # There is a error
            except Exception as e: logger.error(e, exc_info=True)

    def isName(self, name = None) -> bool: return self.name == name

    def isType(self, type = None) -> bool: return self.type == type

    def withOutcome(self, outcome = None) -> bool: return self.outcome == outcome