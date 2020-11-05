######################################
# Import and initialize the librarys #
######################################
from code.api.core import log, coreFunc, os, PgEss, pygame
from code.api.actions import Info, Runclass, Alert, Switchscreen, ActionResult, Mouse
from code.api.data.Sound import sound, Effect


#################
# Setup logging #
#################
filename = os.path.basename(__file__).split('.')[0]
logger = log.get_logger(filename)


#################
# Event classes #
#################
class Sequence(coreFunc):
    def __init__(self, name, n:int, timer:int = 10, withCounter:bool = True, autoRemove:bool = True):
        self.name = name
        self.Event = pygame.USEREVENT + n
        self.counter = 0
        self.queue = []
        self.withCounter = withCounter
        self.autoRemove = autoRemove
        self.run = True
        if timer != -1: pygame.time.set_timer(self.Event, timer)

    def addQueue(self, Action:Runclass):
        if isinstance(Action, Runclass): self.queue.append(Action)
        else: logger.error('Unable to add action to queue. Action needs to be a Runclass.')

    def call(self):
        pygame.event.post(pygame.event.Event(self.Event))

    def pause(self): self.run = False

    def play(self): self.run = True

    def clearQueue(self): 
        self.queue = []
        self.counter = 0

class GameEvent(coreFunc):
    def __init__(self, Events:dict = None):
        self.containerList = []
        if Events != None:
            for name, Event in Events.items(): self.add(name, Event)
    
    def add(self, name:str, Event:dict):
        setattr(self, name, Sequence(name, **Event))
        self.containerList.append(name)


gameEvent = GameEvent(
    {
        'stats': {'n': 1, 'timer': 10},
        'animate': {'n': 2, 'timer': 10},
        'orb_change': {'n': 3, 'timer': -1, 'withCounter': False, 'autoRemove': False}
    }
)


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
        if type(value) == str:
            return any(result[key] == value for result in self.__dict__.values())
        elif type(value) == list:
            return any(result[key] in value for result in self.__dict__.values())


class Events(coreFunc):
    def __init__(self, Object):
        self.Object = Object
        self.on_object = None

    def event(self, run_events:list):
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

    def get(self):
        # Run events
        event_result = self.event([
            eventRun(action='click', event=self.click),
            eventRun(action='keyup', event=self.keyup),
            eventRun(action='keydown', event=self.keydown),
            eventRun(action='game', event=self.game),
            eventRun(action='quit', event=self.quit)
        ])
        
        # Output event's result if any
        if event_result.didAction(): 
            logger.debug('[{}] {}'.format(self.Object.name, event_result))
            return event_result

    def click(self, event):
        # Check for move hover when mouse moves
        if event.type == pygame.MOUSEMOTION or (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
            self.on_object = Mouse.hoverObject(self.Object)

        # Check if item is valid
        if self.on_object == None: return

        # If item is disabled
        if hasattr(self.on_object, 'state') and self.on_object.isState('Disabled'): return

        # Check if mouse is clicked
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            # Play click sound
            if isinstance(self.on_object.clickSound, Effect):
                self.on_object.clickSound.play(maxtime=1000, withVolume=PgEss.config.sound.button)

            # Set state to clicked
            click_result = ActionResult(name=self.on_object.name, type=self.on_object.type, outcome='clicked')

            # Object back to normal state
            self.on_object.switchState('')
            
            # Get the outcome of running
            click_result.getOutcome(self.on_object.action)

            # Output result
            return click_result

    def game(self, event):
        for Event in gameEvent:
            # Init result
            game_result = ActionResult(name=Event.name, type='gameEvent')

            # Check for event
            if event.type == Event.Event:
                # Run the event if can
                if Event.queue != [] and Event.run:
                    eventAction = Event.queue[0]
                    # Set counter parameter
                    if Event.withCounter: eventAction.parameters['counter'] = Event.counter
                    # Run the animation instant
                    game_result.getOutcome(eventAction)
                    if Event.withCounter: Event.counter += 1

                # Animate error
                if game_result.isOutcome("__error__"):
                    Event.queue.pop(0)
                    return game_result

                # Animate is done, remove it and reset
                if game_result.isOutcome(True):
                    Event.counter = 0
                    if Event.autoRemove: Event.queue.pop(0)
                    return game_result

    def keydown(self, event):
        keyboard_result = None
        # When key is pressed
        if event.type == pygame.KEYDOWN:
            keyboard_result = ActionResult(name=event.key, type='down', outcome='pressed')
            # Add to keypressed
            PgEss.keypressed.append(event)

        return self.keyEvent(event, keyboard_result)
        
    def keyup(self, event):
        keyboard_result = None
        # When key is released
        if event.type == pygame.KEYUP:
            keyboard_result = ActionResult(name=event.key, type='up', outcome='released')
            # Remove from keypressed
            for index, pressed in enumerate(PgEss.keypressed):
                if pressed.key == event.key: 
                    PgEss.keypressed.pop(index)
                    break
        
        return self.keyEvent(event, keyboard_result)

    def keyEvent(self, event, keyboard_result):
        # When there was an action
        if keyboard_result != None and hasattr(self.Object, 'keyboard'):
            keyboard = self.Object.keyboard
            # Check if key that was pressed have action to run
            for name in keyboard.containerList:
                key = keyboard[name]

                # On match key state and match key
                if key.onKey == keyboard_result.type and event.key in key.keys:
                    # Set name of result
                    keyboard_result.name = key.name
                    # Get the outcome of running
                    keyboard_result.getOutcome(key.action) 
            
        return keyboard_result

    def quit(self, event):
        # Prompt user if they want to quit the game
        if event.type == pygame.QUIT: 
            Alert (
                type='confirm', 
                title='Quit Game',
                content='Are you sure you want to quit?',
                yes=Info(text='quit')
            ).do()