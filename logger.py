#Name: logger.py
#Date: 6:58PM, 27/10/12
#Author: John Board

import logging, constants, sys, traceback 
import profiler

sys.dont_write_bytecode = True

class Logger:
    def __init__(self, taskmanager, name=constants.LOGGER_NAME, level=logging.DEBUG):
        logging.basicConfig(filename="Logging/log.txt", filemode="w", format=constants.LOGGING_FORMAT)
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        self.level = level
        self.taskmanager = taskmanager
        
        
        self.logNoTag(logging.INFO, "==========["+constants.NAME+"]==========\n")
        self.logNoTag(logging.INFO, "(c) John Board 2012\n")
        
        #print "==========[RoboCup Junior Soccer Simulator]==========\n"        
        #print "(c) John Board 2012\n"
        
        self.info("TaskManager Started.")
        self.info("Logger Started.\n")
        
    def logFrame(self, msg):
        self.logger.debug("[FRAME] "+str(msg))
        
    def silentDebugLog(self, msg):
        self.logger.debug("[DEBUG] "+str(msg))
            
    def debug(self, msg):                                                       #For general debugging info - i.e. profiler times
        self.logger.debug("[DEBUG] "+str(msg))
        if logging.DEBUG >= self.level:
            print "[DEBUG] "+str(msg)
        
    def info(self, msg):                                                        #General information - i.e. "Simulation Starting!"
        self.logger.info("[INFO] "+str(msg))
        if logging.INFO >= self.level:
            print "[INFO] "+str(msg)
        
    def warning(self, msg):                                                     #For possible errors - system time changing?
        self.logger.warning("[WARNING] "+str(msg))
        if logging.WARN >= self.level:
            print "[WARNING] "+str(msg)
        
    def error(self, msg):                                                       #For caught, no severe errors, errors that won't affect much - AI sytax wrong?
        self.logger.error("[ERROR] "+str(msg))
        if logging.ERROR >= self.level:
            print "[ERROR] "+str(msg)
        
    def critical(self, msg):                                                    #For errors that may have crashed part of the program - eventhandler KeyError?
        self.logger.critical("[CRITICAL] "+str(msg))
        if logging.CRITICAL >= self.level:
            print "[CRITICAL] "+str(msg)
        
    def fatal(self, msg):                                                       #For errors that have crashed the entire program
        self.logger.fatal("[FATAL] "+str(msg))
        if logging.FATAL >= self.level:
            print "[FATAL] "+str(msg)
        
    def log(self, level, msg):
        self.logger.log(level, "[LOG] "+str(msg))
        
    def logNoTag(self, level, msg):
        self.logger.log(level, str(msg))
        print str(msg)
        
    def printErrorStack(self):
        self.logNoTag(logging.DEBUG, "----------[Error]--------")
        traceback.print_exc()
        self.logNoTag(logging.DEBUG, "-------------------------")
        
    def displayTimes(self):
        self.logNoTag(logging.DEBUG, "\n")
        self.debug("==========[Times]==========")
        self.debug("FPS: "+str(int(self.taskmanager.getFPS())))
        for entry in profiler.getTimes():
            self.debug(entry+": "+str(profiler.getTime(entry))+ "ms")
        self.debug("===========================\n")