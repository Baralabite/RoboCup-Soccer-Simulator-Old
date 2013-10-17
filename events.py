#Name: events.py
#Date: 6:58PM, 27/10/12
#Author: John Board

import sys, constants
sys.dont_write_bytecode = True

"""
File for common events, and custom events.
"""

#---[Event Definitions]---#

#This is really just an enum of event types, not required, just makes the code
#prettier

#
        
            
#---[Templates]---#

class Event:
    def __init__(self):
        pass
    
class EventWithData(Event):
    def __init__(self):
        self.data = None
        
    def setData(self, data):
        self.data = data
        
    def getData(self):
        return self.data

class CancellableEvent(Event):
    def __init__(self):
        Event.__init__(self)
        self.cancelled = False
    def isCancelled(self):
        return self.cancelled
    
    def setCancelled(self, cancelled):
        self.cancelled = cancelled
        
class CancellableEventWithData(EventWithData):
    def __init__(self):
        Event.__init__(self)
        self.cancelled = False
    def isCancelled(self):
        return self.cancelled
    
    def setCancelled(self, cancelled):
        self.cancelled = cancelled
        
        

#---[Custom Events]---#

class EventType:
    PYGAME_QUIT = 0,
    PYGAME_WINDOW_RESIZE = 1,
    MAINLOOP_UPDATE = 2,
    COLLISION = 3,
    PYGAME_KEYDOWN=4
    

class PygameQuitButtonEvent(CancellableEventWithData):
    def __init__(self):
        CancellableEventWithData.__init__(self)
    
class PygameWindowResizeEvent(CancellableEventWithData):
    def __init__(self):
        CancellableEventWithData.__init__(self)
        
class PygameKeydownEvent(CancellableEventWithData):
    def __init__(self):
        CancellableEventWithData.__init__(self)
        
class MainLoopUpdateEvent(Event):
    def __init__(self, fps):
        Event.__init__(self)
        self.fps = fps
        
    def getCurrentFPS(self):
        return self.fps
    
    def setUpdateFPS(self, fps):
        constants.FPS = fps
        
    def getUpdateFPS(self, fps):
        return constants.FPS
    
class CollisionEvent(CancellableEvent):
    def __init__(self, collisions):
        CancellableEvent.__init__(self)
        self.collisions = collisions
        
    def getCollisions(self):
        return self.collisions
    
    def setCollisions(self):
        return self.collisions
    
    def addCollision(self, name, data):
        self.collisions[name] = data
        
    def deleteCollision(self, name):
        del self.collisions[name]
        