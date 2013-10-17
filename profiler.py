#Name: profiler.py
#Date: 6:58PM, 27/10/12
#Author: John Board

import sys
sys.dont_write_bytecode = True
times = {}

def getTimes():
    return times

def getTime(name):
    return times[name]

def setTime(name, data):
    global times
    times[name] = data

class Profiler:
    def __init__(self, logger, name, taskmanager):
        self.taskmanager = taskmanager
        self.logger = logger
        self.name = name
        self.logger.debug("Profiler '"+name+"' Initalized.")
        self.start = 0
        self.stop = 0
        
    def startTimer(self):
        self.start = self.taskmanager.getCounter()
        
    def stopTimer(self):
        self.stop = self.taskmanager.getCounter()
        setTime(self.name, self.stop-self.start)
        
    def getTime(self):
        return self.stop-self.start