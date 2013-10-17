#Name: scripthandler.py
#Date: 6:58PM, 27/10/12
#Author: John Board

import os

class ScriptHandler:
    def __init__(self, logger, taskmanager):
        self.logger = logger
        self.logger.info("ScriptHandler initalized.")
        
        self.taskmanager = taskmanager
        
        self.scripts = {}
    
    def loadScript(self, team, name, api):
        script = None
        exec("import Scripts."+team+"."+name+" as script")
        self.scripts[name] = script.RobotAI(api)
        del script
        self.logger.info("Loaded AI "+name+" onto the "+api.getTeam()+" team.")
        
    def getLoadableScripts(self):
        return [files.strip("SCRIPT_").split(".")[0] for files in os.listdir("Scripts") if files.startswith("SCRIPT_") and files.endswith(".py")]
    
    def closeScript(self, name):
        del self.scripts[name]
    
    def updateScript(self, name):
        #self.taskmanager.addProcess(name, self.scripts)
        self.scripts[name].update()
        
    def updateAllScripts(self):
        for script in self.scripts:
            self.updateScript(script)