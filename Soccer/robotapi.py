#Name: robotapi.py
#Date: 6:58PM, 27/10/12
#Author: John Board

import constants

class RobotAPI:
    def __init__(self, robot):
        self.__robot = robot
        
    def getSensorReading(self, name):
        return self.__robot.getSensorReading(name)
        
    def getNumberOfSensors(self):
        return self.__robot.getNumberOfSensors()
    
    def getAllSensors(self):
        return self.__robot.getAllSensors()
        
    def getConfig(self):
        return self.__robot.config
    
    def Forward(self, speed):
        self.__robot.setSpeed(speed)
        
    def Backward(self, speed):
        self.__robot.setSpeed(-speed)
        
    def TurnRight(self, angle):
        if angle > constants.MAX_ROBOT_TURNING_SPEED:
            angle = constants.MAX_ROBOT_TURNING_SPEED
        self.__robot.setAngle((self.__robot.getAngle()+angle)%360)
        
    def TurnLeft(self, angle):
        if angle > constants.MAX_ROBOT_TURNING_SPEED:
            angle = constants.MAX_ROBOT_TURNING_SPEED
        self.__robot.setAngle((self.__robot.getAngle()-angle)%360)
        
    def getTeam(self):
        return self.__robot.getTeam()
        
    def debug(self, msg):
        self.logger.debug("[SCRIPT: '"+self.__robot.getName()+"'] "+msg)