######################################
# Import and initialize the librarys #
######################################
from code.api.core import log, coreFunc, os, pg, pygame, screens


#################
# Setup logging #
#################
filename = os.path.basename(__file__).split('.')[0]
logger = log.get_logger(filename)
logger.info('Loading up {}...'.format(filename))


##################
# Action classes #
##################
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


#################
# Event classes #
#################
class eventRun(coreFunc):
    def __init__(self, action:str, event:any, parameters:list = []): 
        self.action = action
        self.event = event
        self.parameters = parameters


class eventResults(coreFunc):
    def __init__(self, **kwargs): 
        self.__dict__.update(kwargs)

    def didAction(self, action = None) -> bool: 
        # Check if there was an action
        if action == None: return self.__dict__ != {}
        # Check for specific action
        else: return hasattr(self, action)

    def contains(self, key:str, value:any) -> bool: 
        return any(result[key] == value for result in self.__dict__.values())


class event(coreFunc):

    def __init__(self, thing):
        self.thing = thing

    def Event(self, events:list):
        # init event result
        result = eventResults()
        # check events
        for event in pygame.event.get():
            for event_run in events: 
                # Run events
                event_result = event_run.event(event, *event_run.parameters)
                # Get and store result if any
                if event_result != None: result[event_run.action] = event_result

        pg.updateDisplay()
        
        return result

    def onThing(self, frame_coord:tuple = None):
        if frame_coord == None: frame_coord = self.thing.frame.coord()
        on_thing = None

        # Loop through loaded things
        for loaded_thing in self.thing.loaded:
            thing_object = self.thing[loaded_thing]

            # Check if thing can be selected
            if hasattr(thing_object, 'selectable') and thing_object.selectable:

                # Check if object is to do an action
                if hasattr(thing_object, 'action') and thing_object.action != None:
                    # Check if mouse over object
                    if thing_object.frame.mouseIn(frame_coord):
                        thing_object.switchState('Hover')
                        on_thing = thing_object
                    else: thing_object.switchState('')

                # Look for things in the object
                elif hasattr(thing_object, 'loaded') and thing_object.loaded != [] and thing_object.frame.mouseIn(frame_coord):
                    on_thing = event(thing_object).onThing(frame_coord=thing_object.frame.coord(frame_coord))

        return on_thing

    def get(self):
        # Check if mouse is an object
        on_thing = self.onThing()

        # Run events
        event_result = self.Event([
            eventRun(action='click', event=self.click, parameters=[on_thing]),
            #eventRun(action='keydown', event=self.keydown),
            #eventRun(action='keyup', event=self.keyup),
            eventRun(action='quit', event=self.quit)
        ])       
        
        # Output event's result if any
        if event_result.didAction(): 
            logger.debug('[{}] {}'.format(self.thing.name, event_result))
            return event_result

    def click(self, event, object_thing):
        # Check if item is valid
        if object_thing == None: return

        # Check if mouse is clicked
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Set state to clicked
            click_result = actionResult(name=object_thing.name, type=object_thing.type, outcome='clicked')
            
            # Get the outcome of running
            click_result.getOutcome(object_thing)

            # Output result
            return click_result

    def keydown(self, event):
        keyboard_result = None
        # When key is pressed
        if event.type == pygame.KEYDOWN:
            keyboard_result = actionResult(name=event.key, type='down', outcome='pressed')
            keypressed.append(event)

        return self.keyEvent(event, keyboard_result)
        
    def keyup(self, event):
        keyboard_result = None
        # When key is released
        if event.type == pygame.KEYUP:
            keyboard_result = actionResult(name=event.key, type='up', outcome='released')
            for index, pressed in enumerate(keypressed):
                if pressed.key == event.key: keypressed.pop(index)
        
        return self.keyEvent(event, keyboard_result)

    def keyEvent(self, event, keyboard_result):
        # When there was an action
        if keyboard_result != None:
            # Check if key that was pressed have action to run
            for name in list(self.__screen__.keyboardActions.__dict__.keys())[1:]:
                key = self.__screen__.keyboardActions[name]

                # On match key state and match key
                if key.onKey == keyboard_result.type and event.key in key.keys:
                    # Set name of result
                    keyboard_result.name = key.name
                    # Get the outcome of running
                    keyboard_result.getOutcome(key) 
            
        return keyboard_result

    def quit(self, event):
        if event.type == pygame.QUIT: 
            return actionResult(name='quit', type='quit', outcome='quit')