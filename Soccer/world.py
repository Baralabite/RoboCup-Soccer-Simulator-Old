import constants, pygame, robot, sys, robotapi
import fieldsections, profiler, maths
sys.dont_write_bytecode = True

class World:
    def __init__(self, physics, logger, surf, taskmanager, config, scripthandler):
        self.screen = surf
        self.physics = physics
        self.scripthandler = scripthandler
        self.surf = pygame.surface.Surface((constants.WORLD_SIZE[0], constants.WORLD_SIZE[1]))
        self.logger = logger
        self.taskmanager = taskmanager
        self.config = config
        
        self.updateProfiler = profiler.Profiler(logger, "World Update Loop", taskmanager)
        
        self.logger.info("World Loaded.")
        
        self.robots = {}
        
        self.objects = []
        
        self.loadFieldObjects()
        self.resizeToFitScreen()
        
        if constants.THREAD_PHYSICS:
            self.taskmanager.addThread("PhysicsUpdateLoop", self.updatePhysicsThread)
        
    #---===[Main]===
    
    def update(self):
        self.updateProfiler.startTimer()
        if constants.THREAD_PHYSICS==False:
            self.physics.update()
        self.updateFieldObjects()
        self.scripthandler.updateAllScripts()
        self.updateRobots()
        self.draw()
        self.updateProfiler.stopTimer()
        
    def updatePhysicsThread(self):
        while 1:
            self.physics.update()
        
    def draw(self):
        self.drawAllFieldObjects()
        #---Draw Stuff Here
        
        self.drawAllRobots()
        
        if constants.DRAW_BOUNDING_BOXES:
            for obj in self.physics.getObjects():
                pygame.draw.rect(self.surf, constants.BOUNDING_BOX_COLOR, self.physics.getObjects()[obj].getRect(), 1)
        
        #---===========
        
        if constants.SCALE_WORLD_SURFACE:
            surf = pygame.transform.scale(self.surf, (int(constants.WORLD_SIZE[0]*constants.WORLD_SCALE), int(constants.WORLD_SIZE[1]*constants.WORLD_SCALE)))
        else:
            surf = self.surf
        self.screen.blit(surf, (self.screen.get_width()/2 - surf.get_width()/2,
                                self.screen.get_height()/2 - surf.get_height()/2 ))
    
    def resizeToFitScreen(self):
        constants.WORLD_SCALE = float(constants.SCREEN_RESOLUTION[1]) / float(constants.WORLD_SIZE[1]+10)
        
    #---===[Field]===
        
    def loadFieldObjects(self):
        self.addObject("OutField", fieldsections.OutField) #This must be created first, else nothing else will render
        self.addObject("NorthWall", fieldsections.NorthWall)
        self.addObject("EastWall", fieldsections.EastWall)
        self.addObject("SouthWall", fieldsections.SouthWall)
        self.addObject("WestWall", fieldsections.WestWall)
        self.addObject("PlayingZone", fieldsections.PlayingZone)
        
        self.addObject("TopGoalContainer", fieldsections.TopGoalContainer)
        self.addObject("TopGoalBackWall", fieldsections.TopGoalBackWall)
        self.addObject("TopGoalLeftWall", fieldsections.TopGoalLeftWall)
        self.addObject("TopGoalRightWall", fieldsections.TopGoalRightWall)
        
        self.addObject("BottomGoalContainer", fieldsections.BottomGoalContainer)
        self.addObject("BottomGoalBackWall", fieldsections.BottomGoalBackWall)
        self.addObject("BottomGoalLeftWall", fieldsections.BottomGoalLeftWall)
        self.addObject("BottomGoalRightWall", fieldsections.BottomGoalRightWall)
        
        self.addObject("TopPenaltyBoxContainer", fieldsections.TopPenaltyBoxContainer)
        self.addObject("BottomPenaltyBoxContainer", fieldsections.BottomPenaltyBoxContainer)
        
        self.addObject("TopGoalLogo", fieldsections.TopGoalLogo)
        self.addObject("BottomGoalLogo", fieldsections.BottomGoalLogo)
        
        self.addObject("InnerPlayingZone", fieldsections.InnerPlayingZone)
        
        
        self.addBall("Ball")
        
    def getObject(self, name):
        for x in self.objects:
            if x.getName()==name:
                return x
        
    def addObject(self, name, class_):
        fieldSection = class_(name, self.surf)
        self.objects.append(fieldSection)
        self.physics.addObject(fieldSection)
        
    def addBall(self, name):
        ball = fieldsections.Ball(name, pygame.rect.Rect(self.surf.get_width()/2, self.surf.get_height()/2, 10, 10), self.surf)
        ball.setAngle(0)
        self.objects.append(ball)
        self.physics.addObject(ball)
            
    def updateFieldObjects(self):
        for object_ in self.objects:
            object_.update()
            
    def drawAllFieldObjects(self):
        for object_ in self.objects:
            object_.draw()
        
    #---===[Robots]===
    
    def getRobot(self, team, name):
        return self.robots[team][name]
        
    def loadAllRobots(self):
        if len(self.config.getEvalValue("RedTeamScripts")) > 0:
            self.loadTeamRobots("Red")
        if len(self.config.getEvalValue("BlueTeamScripts")) > 0:
            self.loadTeamRobots("Blue")
        
    def loadTeamRobots(self, team):
        for script in self.config.getEvalValue(team+"TeamScripts"):
            api = self.addRobot(script, team)
            self.scripthandler.loadScript(team, script, api)
        
    def addRobot(self, name, team="Red"):
        try:
            self.robots[team]
        except KeyError:
            self.robots[team] = {}
        self.robots[team][name] = robot.Robot(self.surf, name, self.logger, self.taskmanager, team)
        
        if team=="Red":
            self.robots[team][name].setAngle(90)
        else:
            self.robots[team][name].setAngle(270)
            
        
        #self.robots[team][name].setPosition()
        self.physics.addObject(self.robots[team][name])
        return robotapi.RobotAPI(self.robots[team][name])
    

    def updateRobots(self):
        for team in self.robots:
            for robot in self.robots[team]:
                rbt = self.robots[team][robot]
                rbt.update()
                
                closestDist = 200
                closestObject = 0, (200, 200), 0
                closestObjectPhy = None
                
                for obj in self.physics.objects:
                    obj = self.physics.objects[obj]
                    if obj.VISIBLE_BY_SONAR:
                        result = maths.isLookingAt(rbt.getPosition(), rbt.getAngle(), obj.getRect())
                        if result[0]:
                            dist = obj.getRect().center
                            dist = dist[0]-rbt.getPosition()[0], dist[1]-rbt.getPosition()[1]
                            dist = maths.math.sqrt((dist[0]*dist[0])+(dist[1]*dist[1]))
                            
                            if dist < closestDist:
                                if not obj.getName() == rbt.getName():
                                    closestDist = dist
                                    closestObject = result
                                    closestObjectPhy = obj
                try:
                    pos2 = maths.polarToCartesian(rbt.getAngle(), dist+100)
                    pos2 = rbt.getPosition()[0]+pos2[0], rbt.getPosition()[1]+pos2[1]
                    lookingAt = maths.getPointOfIntersection(rbt.getPosition(), 
                                                              pos2, 
                                                              maths.indexToCoordinate(closestObjectPhy.getRect(), closestObject[2]), 
                                                              maths.indexToCoordinate(closestObjectPhy.getRect(), closestObject[3]))
                    
                    dx, dy = lookingAt[0]-rbt.getPosition()[0], lookingAt[1]-rbt.getPosition()[1]
                    distFromPointBeingLookedAt = maths.math.sqrt((dx*dx)+(dy*dy))
                    rbt.addSensorReading("SONAR", distFromPointBeingLookedAt)
                    rbt.addSensorReading("TYPE", closestObjectPhy.getName())
                except Exception, ex:
                    pass #TODO
                                    
    def drawAllRobots(self):
        for team in self.robots:
            for robot in self.robots[team]:
                self.robots[team][robot].draw()
                