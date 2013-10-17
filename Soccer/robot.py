import pygame, constants, sys, maths
sys.path.append("..")
sys.dont_write_bytecode = True
import physics, configparser

class Robot(physics.MovingObject):
    def __init__(self, surf, name, logger, taskmanager, team="Red"):        
        rect = pygame.rect.Rect((surf.get_width()/2)-1-constants.ROBOT_SIZE/2, (surf.get_height()/2)-1-constants.ROBOT_SIZE/2, constants.ROBOT_SIZE, constants.ROBOT_SIZE)
        physics.MovingObject.__init__(self, name, rect)
        self.MASS = 2
        self.BOUNCYNESS = 90
        if team=="Red":
            self.color = (255, 0, 0)
            self.heading = 180
        elif team=="Blue":
            self.color = (0, 0, 255)
        self.team = team
        self.config = configparser.ConfigParser("Scripts/"+team+"/config.conf", logger, taskmanager)
        self.kickoffPosition = self.config.getDictValue("StartingPositionKickoff")[name]
        self.defensivePosition = self.config.getDictValue("StartingPositionDefensive")[name]
        self.sensorConfig = self.config.getDictValue("SensorConfiguration")[name]
        self.moveToKickoffPosition()
        self.surf = surf
        self.sensors = {}

    #---===[Updates]==
    
    def addSensorReading(self, name, data):
        self.sensors[name] = data
    
    def update(self):
        #Sensors:
        #Pos, Compass, Sonar
        if "GPS" in self.sensorConfig:
            self.sensors["GPS"] = self.getPosition()
        if "COMPASS" in self.sensorConfig:
            self.sensors["COMPASS"] = self.angle

    def draw(self):
        pygame.draw.circle(self.surf, self.color, self.rect.center, 8)
        pos1 = maths.polarToCartesian(self.getHeading(), 7)
        pygame.draw.line(self.surf, (0, 255, 0), (pos1[0]+self.rect.centerx, pos1[1]+self.rect.centery), self.rect.center, 1)   
        
    #---===[Misc]===
    
    def getTeam(self):
        return self.team   
    
    #---===[Move to Starting Positions]===
    
    def moveToKickoffPosition(self):
        if self.team=="Red":
            pos = self.kickoffPosition[0]+constants.WORLD_SIZE[0]/2, (constants.WORLD_SIZE[1]/2)-self.kickoffPosition[1]
        else:    
            pos = -self.kickoffPosition[0]+constants.WORLD_SIZE[0]/2, (constants.WORLD_SIZE[1]/2)+self.kickoffPosition[1]
        self.setPosition(pos)
            
    def moveToDefensivePosition(self):
        if self.team=="Red":
            pos = self.defensivePosition[0]+constants.WORLD_SIZE[0]/2, (constants.WORLD_SIZE[1]/2)-self.defensivePosition[1]
        else:    
            pos = -self.defensivePosition[0]+constants.WORLD_SIZE[0]/2, (constants.WORLD_SIZE[1]/2)+self.defensivePosition[1]
        self.setPosition(pos)
        
    #---===[Sensors]===
    
    def getSensorReading(self, name):
        try:
            return self.sensors[name]
        except:
            return None
        
    def getAvaliableSensors(self):
        return self.sensors.keys()
    
    def getAllSensors(self):
        return self.sensors
    
    def getNumberOfSensors(self):
        return len(self.sensors)