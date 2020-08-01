######################################
# Import and initialize the librarys #
######################################
from code.api.core import log, coreFunc, os, pg, pygame
from code.api.actions import Info, Runclass, Switchscreen, actionResult


#################
# Setup logging #
#################
filename = os.path.basename(__file__).split('.')[0]
logger = log.get_logger(filename)
logger.info('Loading up {}...'.format(filename))


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


class events(coreFunc):

    def __init__(self, thing):
        self.thing = thing

    def Event(self, run_events:list):
        # init event result
        result = eventResults()
        # check events
        for event in pygame.event.get():
            for event_run in run_events: 
                # Run events
                event_result = event_run.event(event, *event_run.parameters)
                # Get and store result if any
                if event_result != None: result[event_run.action] = event_result

        return result

    def onThing(self, frame_coord:tuple = None):
        if frame_coord == None: frame_coord = self.thing.frame.coord()
        on_thing = None

        # Loop through loaded things
        for loaded_thing in self.thing.containerList:
            # Get the object
            thing_object = self.thing[loaded_thing]
            
            # If thing is not loaded or selectable, dont check
            if not (thing_object.loaded and hasattr(thing_object, 'selectable') and thing_object.selectable): continue

            # Check if thing_object is disabled
            if hasattr(thing_object, 'state') and thing_object.isState('Disabled'): continue

            # Check if object is to do an action
            if hasattr(thing_object, 'action') and thing_object.action != None:
                # Check if mouse over object
                if thing_object.frame.mouseIn(frame_coord):
                    thing_object.switchState('Hover')
                    on_thing = thing_object
                else: thing_object.switchState('')

            # Look for things in the object
            elif hasattr(thing_object, 'loaded') and thing_object.loaded:
                on_thing = events(thing_object).onThing(frame_coord=thing_object.frame.coord(frame_coord))

        return on_thing

    def get(self):
        # Check if mouse is an object
        on_thing = self.onThing()

        # Run events
        event_result = self.Event([
            eventRun(action='click', event=self.click, parameters=[on_thing]),
            eventRun(action='keydown', event=self.keydown),
            eventRun(action='keyup', event=self.keyup),
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
            # Add to keypressed
            pg.keypressed.append(event)

        return self.keyEvent(event, keyboard_result)
        
    def keyup(self, event):
        keyboard_result = None
        # When key is released
        if event.type == pygame.KEYUP:
            keyboard_result = actionResult(name=event.key, type='up', outcome='released')
            # Remove from keypressed
            for index, pressed in enumerate(pg.keypressed):
                if pressed.key == event.key: 
                    pg.keypressed.pop(index)
                    break
        
        return self.keyEvent(event, keyboard_result)

    def keyEvent(self, event, keyboard_result):
        # When there was an action
        if keyboard_result != None and hasattr(self.thing, 'keyboard'):
            keyboard = self.thing.keyboard
            # Check if key that was pressed have action to run
            for name in keyboard.containerList:
                key = keyboard[name]

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