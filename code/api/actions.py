######################################
# Import and initialize the librarys #
######################################
from code.api.core import log, coreFunc, os, screens


#################
# Setup logging #
#################
filename = os.path.basename(__file__).split('.')[0]
logger = log.get_logger(filename)


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
    def __init__(self, run:any, parameters:dict = None):
        self.run = run
        if parameters == None: self.parameters = dict()
        else: self.parameters = parameters

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
        screens.alert.unload(withSurfaces=['confirm', 'notify'])

        # Common dismissed action
        screens.alert.keyboard.dismiss.action = self.dismiss
        screens.alert.back.dismiss.action = self.dismiss

        # Check type of alert to load
        if self.type == 'confirm': 
            # Set messages
            screens.alert.confirm.message.title.setText(self.title, withDisplay=False)
            screens.alert.confirm.message.content.setText(self.content, withDisplay=False)

            # Set actions
            screens.alert.confirm.no.action = self.no
            screens.alert.confirm.yes.action = self.yes

            # Display to screen
            screens.alert.display(withSurfaces=['back', 'confirm'], refresh=True)

        elif self.type == 'notify':
            # Set messages
            screens.alert.notify.message.title.setText(self.title, withDisplay=False)
            screens.alert.notify.message.content.setText(self.content, withDisplay=False)

            # Set actions
            screens.alert.notify.ok.action = self.ok

            # Display to screen
            screens.alert.display(withSurfaces=['back', 'notify'], refresh=True)

        # When alert type not found
        else: logger.error('No such alert type: {}'.format(self.type))

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

        if actions != None:
            for name, action_data in actions.items(): self.add(name, action_data)
            

    def add(self, name, data):
        setattr(self, name, Key(self.screen, name, **data))
        self.containerList.append(name)


class Key(coreFunc):
    def __init__(self, screen, name, keys:list, action:any, onKey:str = 'down', useAscii:bool = True):
        self.screen = screen
        self.name = name
        self.keys = keys
        self.onKey = onKey
        self.useAscii = useAscii
        self.action = action



########################
# Mouse action classes #
########################
class Mouse:
    isTouch = False
    previous_mouse = None

    @classmethod
    def checkTouch(cls):
        if cls.previous_mouse == None: cls.previous_mouse = pygame.mouse.get_pos()
        
        else:
            current_mouse = pygame.mouse.get_pos()
            move_x, move_y = pygame.mouse.get_rel()

            diff_x = current_mouse[0] - cls.previous_mouse[0]
            diff_y = current_mouse[1] - cls.previous_mouse[1]

            if diff_x == 0 and diff_y == 0: return

            if diff_x != move_x or diff_y != move_y:
                cls.isTouch = True
                print('touching')
            elif cls.isTouch:
                cls.isTouch = False
                print('mousing')

            cls.previous_mouse = current_mouse

    @staticmethod
    def hoverObject(Object, frame_coord:tuple = None):
        if frame_coord == None: frame_coord = Object.frame.coord()
        on_object = None

        # Loop through loaded things
        for thing_object in Object:

            # If thing is not loaded or selectable, dont check
            if not(hasattr(thing_object, 'loaded') and hasattr(thing_object, 'selectable')): continue
            if not (thing_object.loaded and thing_object.selectable): continue

            # Check if thing_object is doesnt have state
            if hasattr(thing_object, 'state') and (thing_object.isState('Disabled') or thing_object.isState('Selected')): continue

            # Check if object is to do an action
            if hasattr(thing_object, 'action'):
                # Check if mouse over object
                if thing_object.frame.mouseIn(frame_coord):
                    thing_object.switchState('Hover')
                    on_object = thing_object
                # Mouse not over object
                elif thing_object.isState('Hover'): 
                    thing_object.switchState('')

            # Look for things in the object
            if hasattr(thing_object, 'containerList') and thing_object.containerList != []:
                result_thing = Mouse.hoverObject(thing_object, frame_coord=thing_object.frame.coord(frame_coord))
                if result_thing != None: on_object = result_thing

        return on_object


##########################
# Action outcome classes #
##########################
class ActionResult(coreFunc):
    def __init__(self, name:str = None, type:str = None, outcome:any = None): 
        self.name = name
        self.type = str(type)
        self.outcome = outcome

    def getOutcome(self, Action):
        # Check if have action
        if Action == None: return

        # A list of actions
        if type(Action) == list:
            self.outcome = []
            # Run through all the laction
            for action in Action:
                # Run the action
                try: self.outcome.append(action.do())
                # There is a error
                except Exception as e: logger.error(e, exc_info=True)

        else:
            # Run the action
            try: self.outcome = Action.do()
            # There is a error
            except Exception as e: logger.error(e, exc_info=True)

    def isName(self, name = None) -> bool: return self.name == name

    def isType(self, type = None) -> bool: return self.type == type

    def withOutcome(self, outcome = None) -> bool: return self.outcome == outcome