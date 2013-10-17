#Name: configparser.py
#Date: 6:58PM, 27/10/12
#Author: John Board

import profiler

class ConfigParser:
    def __init__(self, path, logger, taskmanager):
        self.logger = logger
        self.taskmanager = taskmanager
        try:
            prof = profiler.Profiler(logger, "ConfigParser", taskmanager)
            prof.startTimer()
            self.file = open(path, "r")
            self.values = {}
            for value in self.file.readlines():
                self.values[value.split(":")[0]] = value.split(":")[1].lstrip(" ").rstrip("\n")
            self.file.close()
            prof.stopTimer()
            logger.info("ConfigParser loaded config in "+str(prof.getTime())+" ms.")
        except Exception:
            logger.info("ConfigParser failed to load config file:")
            logger.printErrorStack()
    
    def getString(self, name):
        try:
            return str(self.values[name])
        except KeyError:
            self.logger.error("Key ("+name+") Doesn't Exist")
            return ""
        except:
            self.logger.printErrorStack()
            return ""
      
    def getDictValue(self, name):
        try:
            return eval(self.values[name].replace("=", ":"))
        except KeyError:
            self.logger.error("Key ("+name+") Doesn't Exist")
            return []
        except:
            self.logger.printErrorStack()
            return []
        
    def getEvalValue(self, name):
        try:
            return eval(self.values[name])
        except KeyError:
            self.logger.error("Key ("+name+") Doesn't Exist")
            return []
        except:
            self.logger.printErrorStack()
            return []
        
    def getBoolean(self, name):
        try:
            if self.values[name]=="True":
                return True
            elif self.values[name]=="False":
                return False
        except KeyError:
            self.logger.error("Key ("+name+") Doesn't Exist")
            return None
        except:
            self.logger.printErrorStack()
            return None
    
    def getInt(self, name):
        try:
            return int(self.values[name])
        except KeyError:
            self.logger.error("Key ("+name+") Doesn't Exist")
            return -1
        except:
            self.logger.printErrorStack()
            return -1