#Name: eventhandler.py
#Date: 6:58PM, 27/10/12
#Author: John Board

import sys
sys.dont_write_bytecode = True

class EventHandler:
    def __init__(self, logger, taskmanager):
        self.taskmanager = taskmanager
        self.logger = logger
        self.logger.info("EventHandler Started.")
        self.listeners = {}
        
    def addEventListener(self, name, type_, function):
        try:
            self.listeners[type_]
        except:
            self.listeners[type_] = {}
        self.listeners[type_][name] = function
        
        
    def deleteEventListener(self, name):
        del self.listeners[name]
        
    def callEvents(self, type_, data):
        if type_ in self.listeners:
            for e in self.listeners[type_]:
                self.listeners[type_][e](data)