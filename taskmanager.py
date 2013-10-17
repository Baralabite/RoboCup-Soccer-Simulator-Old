#TODO: Make more object orientated (for example, self.threads objects can be a class
#class Thread for example

import threading, time, pygame, constants
import sys
from multiprocessing import Process
sys.dont_write_bytecode = True

class TaskManager:
    def __init__(self):
        self.threads = {}
        self.processes = {}
        self.tasks = {}
        self.scheduledTasks = {}

        self.counter = 0
        self.currentMS = 0
        
        self.frameCount = 0
        
        self.clock = pygame.time.Clock()
        
        self.addThread("CounterUpdateLoop", self.counterUpdateLoop)
        self.addScheduledTask("ThreadListClearner", self.cleanThreadList, 333)
        
        self.clock = pygame.time.Clock()
        
    #FPS Updating
    
    def update(self, fps=0):
        
        if constants.LIMIT_FPS:
            self.clock.tick(fps)
        else:
            self.clock.tick()
            
        self.frameCount += 1
        
    def getFrameCount(self):
        return self.frameCount
    
    def setFrameCount(self, frames):
        self.frameCount = frames
        
    def getFPS(self):
        return self.clock.get_fps()
    
    def stacktraces(self):
        return
        """for threadId, stack in sys._current_frames().items():
            #code.append("\n# ThreadID: %s" % threadId)
            #print "\n# ThreadID: %s" % threadId
            for filename, lineno, name, line in traceback.extract_stack(stack):
                #code.append('File: "%s", line %d, in %s' % (filename, lineno, name))
                #print 'File: "%s", line %d, in %s' % (filename, lineno, name)
                print filename.split("\\")[len(filename.split("\\"))-1]
                if line:
                    #code.append("  %s" % (line.strip()))
                    #print "  %s" % (line.strip())
                    pass"""
        
    #Thread Stuff
        
    def addThread(self, name, func, daemon=True, start=True, params=None):  
        """
        Returns bool
        
        Starts a new thread, and saves it's data into self.threads
        """
        try:                    
            if params != None:
                t = threading.Thread(target=func, args=[params])               
            else:
                t = threading.Thread(target=func)
            t.setDaemon(daemon)                                                    
            self.threads[name] = (func, t)                                         
            if start==True:                                                        
                self.startThread(name)
            return True
        except:
            return False
        
    def deleteThread(self, name):  
        """
        Returns bool
        
        Deletes a thread from self.threads
        """   
        try:                                                                    #Delete thread  
            del self.threads[name]                                 
            return True
        except:
            return False
        
    def startThread(self, name): 
        """
        Returns bool
        
        Starts a thread in self.threads
        """
        try:
            self.threads[name][1].start()     
            return True
        except:
            return False
        
    def cleanThreadList(self):
        """
        Returns bool
        
        Clears finished threads from the thread list
        """
        try:
            for t in self.threads:
                if self.threads[t][1].is_alive() == False:
                    del self.threads[t]
            return True
        except RuntimeError:
            try:
                time.sleep(0.01)
                for t in self.threads:
                    if self.threads[t][1].is_alive() == False:
                        del self.threads[t]
            except RuntimeError:
                return False
        
           
        
    def getActiveThreadCount(self):                                             
        """
        Returns int
        
        Number of threads currently running as defined by threading
        """
        return threading.active_count()

    def getListedThreadCount(self):
        """
        Returns int
        
        Number of threads currently runnning as defined by the threads listed
        in self.threads
        """
        return len(self.threads)
        
    #Process Stuff
    
    def addProcess(self, name, func, daemon=True, start=True, params=None):  
        """
        Returns bool
        
        Starts a new thread, and saves it's data into self.threads
        """
        try:                    
            if params != None:
                t = Process(target=func, args=[params])               
            else:
                t = Process(target=func)
            t.daemon = daemon                                                    
            self.processes[name] = (func, t)                                         
            if start==True:                                                        
                self.startProcess(name)
            return True
        except:
            return False
        
    def deleteProcess(self, name):  
        """
        Returns bool
        
        Deletes a thread from self.threads
        """   
        try:                                                                    #Delete thread  
            del self.processes[name]                                 
            return True
        except:
            return False
        
    def startProcess(self, name):
        """
        Returns bool
        
        Starts a process"
        """
        try:
            self.processes[name].start()
            return True
        except:
            return False
        
    def stopProcess(self, name):
        """
        Returns bool
        
        True on sucessfully deleting the thread.
        """
        try:
            self.processes[name].terminate()
            return True
        except:
            return False
        
        
        
    #Task Stuff
    
    def addTask(self, name, func, startingTime, updateTime, threaded=False):
        """
        Returns bool
        
        Adds a new task.
        """
        try:
            self.tasks[name] = (func, startingTime, updateTime, threaded, 0)
            return True
        except:
            return False
    
    def addScheduledTask(self, name, func, time, threaded=False):
        """
        Returns bool
        
        Adds a task to be executed at a pertucular counter position
        """
        try:
            self.scheduledTasks[name] = (func, time, threaded)
            return True
        except:
            return False
        
    def deleteScheduledTask(self, name):
        """
        Returns bool
        
        Removes a scheduled task
        """
        try:
            del self.scheduledTasks[name]
            return True
        except:
            return False

    def callPossibleTasks(self, cnt):
        """
        Returns bool
        
        Executes any task that happens to be scheduled on the current counter's
        position
        """
        
        #try:
            #print cnt            
        for task in self.scheduledTasks:
            if self.scheduledTasks[task][1] == cnt%1000:
                if self.scheduledTasks[task][2]:
                    self.addThread("scheduledTask_"+task,self.scheduledTasks[task][0])
                else:
                    self.scheduledTasks[task][0]()
                
                
        for task in self.tasks:
            
            if self.tasks[task][1]==cnt:
                if self.tasks[task][3]:
                    self.addThread("task_"+task, self.tasks[task][0])
                else:
                    self.tasks[task][0]()
                self.tasks[task] = self.tasks[task][0], self.tasks[task][1], self.tasks[task][2], self.tasks[task][3], cnt+self.tasks[task][2]
            if self.tasks[task][4]==cnt:
                if self.tasks[task][3]:
                    self.addThread("task_"+task, self.tasks[task][0])
                else:
                    self.tasks[task][0]()
                self.tasks[task] = self.tasks[task][0], self.tasks[task][1], self.tasks[task][2], self.tasks[task][3], cnt+self.tasks[task][2]
                
                
                
        self.deleteThread("CallScheduledTasks")
        return True
        #except:
        #    return False
        
    #Counter Stuff
    
    def counterUpdateLoop(self):
        """
        Returns None
        
        Updates the counter value every 1ms
        """
        
        while 1:
            #self.counter = self.counter + 1
            #time.sleep(0.001)
            self.counter = pygame.time.get_ticks()
            self.addThread("CallScheduledTasks", self.callPossibleTasks, params=self.counter)
            
            
    def getCounter(self):
        """
        Returns int
        
        Returns current counter value
        """
        return self.counter
    
    def setCounter(self, value):
        """
        Returns bool
        
        Sets current counter value
        """
        try:
            self.counter = value
            return True
        except:
            return False
        
    def getCurrentMS(self):
        """
        Return int
        
        Returns current MS
        """        
        try:
            return self.counter % 1000
            return True
        except:
            return False
