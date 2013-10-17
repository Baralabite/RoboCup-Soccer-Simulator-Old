import profiler, constants, maths
#Convert Collisions to event infrastructure

class PhysicsEngine:
    def __init__(self, logger, taskmanager, eventhandler):
        self.taskmanager = taskmanager
        self.logger = logger
        self.eventhandler = eventhandler
        self.updateProfiler = profiler.Profiler(logger, "Physics Engine Update Loop", taskmanager)
        
        self.logger.info("Physics Engine Started.")
        
        self.objects = {}
        self.collisions = {}
        
        self.collisionLogger = CollisionLogger("Logging/collisions.txt")
        
    def addObject(self, object_):
        self.objects[object_.getName()] = object_
        
    def getObjects(self):
        return self.objects
    
    #@profile
    def update(self):
        self.updateProfiler.startTimer()
        self.updateMovement()
        self.updateCollisions()
        self.updateProfiler.stopTimer()
      
    def updateMovement(self):
        for obj in self.objects:
            obj = self.objects[obj]
            if obj.TYPE=="MovingObject":
                obj.setSpeed(maths.getReducedSpeedByPercent(obj.FRICTION, obj.getSpeed()))
                vec = maths.polarToCartesian(obj.getAngle(), obj.getSpeed())
                obj.setVector(vec)
                #print vec, obj.getAngle(), obj.getSpeed(), obj.getPosition()
                obj.setPosition((obj.getPosition()[0]+vec[0], obj.getPosition()[1]+vec[1]))
            
        
    #@profile
    def updateCollisions(self):
        for obj in self.objects:
            collisions = self.objects[obj].getRect().collidedictall(self.constructRSD(self.objects))
            collisions = self.normalizeDictFromRSD(collisions)
            try:
                del collisions[obj]
            except:
                pass
                #if constants.DEBUG_MODE:        
                #    self.logger.printErrorStack()
                
 
            try: 
                self.scanThroughObjectsForCollisions(collisions, obj)
            except KeyError:
                pass
            except Exception:
                self.logger.printErrorStack()
            
            self.collisions[obj] = collisions
        if constants.DEBUG_MODE and constants.LOG_COLLISIONS:
                self.logCollisions()
                
    def scanThroughObjectsForCollisions(self, collisions, obj):
        diff = set(collisions.keys()) - set(self.collisions[obj].keys())
        if len(diff)>=1:
            collisionList = list(diff)
            collisionDict = {}
            for x in collisionList:
                collisionDict[x] = collisions[x]
                
            objectThatCollided = self.objects[obj]
            objectsThatWereHit = {}
            for x in collisionDict:
                objectsThatWereHit[x] = self.objects[x]
            self.handleCollide(objectThatCollided, objectsThatWereHit)
            
    def logCollisions(self):
        self.collisionLogger.startBlock(self.taskmanager.getFrameCount())
        for x in self.collisions:
            if not self.collisions[x] == {}:
                self.collisionLogger.addTopic(x)
                for y in self.collisions[x]:
                    self.collisionLogger.addSubTopic(y, self.collisions[x][y])
        self.collisionLogger.finishBlock()
                
               
    def normalizeDictFromRSD(self, dictionary):
        return dict(zip(dict(dictionary).values(), dict(dictionary).keys()))
    
    def handleCollide(self, object_, objectsHit):
        for obj in objectsHit:
            if not objectsHit[obj] in object_.handledCollisions: 
                obj = objectsHit[obj]
                if object_.getType()=="MovingObject" and obj.getType()=="StationaryObject":
                    c = self.getCollisionDirection(object_, obj)
                    if c[0] or c[1]:
                        object_.setAngle(maths.getAngleOfReflection(object_.getAngle(), 0))
                        pos = object_.getPosition()
                        vec = maths.polarToCartesian((180+object_.getAngle())%360, 3)
                        pos = pos[0]-vec[0], pos[1]-vec[1]
                        object_.setPosition(pos)
                    elif c[2] or c[3]:
                        object_.setAngle(maths.getAngleOfReflection(object_.getAngle(), 90))
                        pos = object_.getPosition()
                        vec = maths.polarToCartesian((180-object_.getAngle())%360, 3)
                        pos = pos[0]-vec[0], pos[1]-vec[1]
                        object_.setPosition(pos)
                    
                    
                    object_.setSpeed(maths.getReducedSpeedByPercent(object_.BOUNCYNESS, object_.getSpeed()))
                    object_.onCollide(obj)                         
                elif object_.getType()=="StationaryObject" and obj.getType()=="StationaryObject":
                    object_.onCollide(obj)
                elif object_.getType()=="MovingObject" and obj.getType()=="MovingObject":
                    object_.moveBack(object_.getSpeed()*2)        
                    print object_.getName(), obj.getName()                  
                    vec = maths.getFinalPolarVectorFromVector(object_.MASS, object_.getVector(), obj.MASS, obj.getVector())
                    #vec = maths.getFinalPolarVectorFromVector(obj.MASS, obj.getVector(), object_.MASS, object_.getVector())
                    
                    if object_.getName()!="Ball":
                        obj.setSpeed(vec[0][1])
                        obj.setAngle(vec[0][0])
                        obj.addHandledCollision(object_)
                        object_.setSpeed(vec[1][1])
                        object_.setAngle(vec[1][0])
                    else:
                        obj.setSpeed(vec[1][1])
                        obj.setAngle(vec[1][0])
                        obj.addHandledCollision(object_)
                        object_.setSpeed(vec[0][1])
                        object_.setAngle(vec[0][0])
    
                elif object_.getType()=="StationaryObject" and obj.getType()=="MovingObject":
                    object_.onCollide(obj)
                elif object_.getType()=="ContainerObject" and obj.getType()=="MovingObject":
                    object_.onCollide(obj)
                elif object_.getType()=="MovingObject" and obj.getType()=="ContainerObject":
                    object_.onCollide(obj)
                else:
                    self.logger.error("Invalid Object(s): "+str(object_.getType())+", "+str(obj.getType()))
                
    def getCollisionDirection(self, a, b):
        return (b.getRect().collidepoint((a.getRect().midtop[0], a.getRect().midtop[1])),
                b.getRect().collidepoint((a.getRect().midbottom[0], a.getRect().midbottom[1]-1)),
                b.getRect().collidepoint((a.getRect().midleft[0], a.getRect().midleft[1])),
                b.getRect().collidepoint((a.getRect().midright[0]-1, a.getRect().midright[1]))
                )
                
    
    def constructRSD(self, dictionary):
        ans = {}
        for x in dictionary:
            ans[x] = tuple(dictionary[x].getRect())
        return dict(zip(ans.values(), ans.keys()))
    
class CollisionLogger():
    def __init__(self, path):
        self.f = open(path, "w")
        self.endLength = 0
    
    def startBlock(self, frameCount):
        block = ("#"+("="*10)+"[ "+str(frameCount)+" ]"+("="*10)+"#\n")
        self.endLength = len(block)
        self.f.write(block)
    
    def addTopic(self, name):
        self.f.write(name+":\n")
        
    def addSubTopic(self, name, data):
        self.f.write("  - "+name+": "+str(data)+"\n")
        
    def addSubSubTopic(self, name, data):
        self.f.write("     - "+name+": "+str(data)+"\n")
        
    def finishBlock(self):
        self.f.write("#"+str("="*(self.endLength-3))+"#\n\n")
        
    def closeFile(self):
        self.f.close()
    
class Object:
    def __init__(self, name, rect):
        self.MASS = 0
        self.FRICTION = 0
        self.BOUNCYNESS = 0
        self.TYPE = "OBJECT"
        self.VISIBLE_BY_SONAR = False
        
        self.name = name
        self.rect = rect
        self.handledCollisions = []
        
    def addHandledCollision(self, obj):
        self.handledCollisions.append(obj)
        
    def getRect(self):
        return self.rect
    
    def setRect(self, rect):
        self.rect = rect
        
    def getName(self):
        return self.name
    
    def setName(self, name):
        self.name = name
        
    def onCollide(self, data):
        pass
    
    def getType(self):
        return self.TYPE
    
    def setType(self, type_):
        self.TYPE = type_
        
    def update(self):
        self.handledCollisions = []
    
    def draw(self):
        pass
    
    def moveToCenter(self):
        self.setPosition(((constants.WORLD_SIZE[0]/2), (constants.WORLD_SIZE[1]/2)))
        self.setSpeed(0)
        
class MovingObject(Object):
    def __init__(self, name, rect):
        Object.__init__(self, name, rect)
        self.VISIBLE_BY_SONAR = True
        self.TYPE = "MovingObject"
        
        self.speed = 0
        self.heading = 0
        self.acceleration = 0
        self.angle = 0
        self.position = 0, 0
        self.oldPosition = 0, 0
        self.vector = 0, 0
        self.objectLookingAt = None
        
    def moveBack(self, steps):
        self.vector = maths.polarToCartesian(self.angle, -steps)
        x,y = self.vector
        self.position = self.position[0]+x, self.position[1]+y
        
    def getPosition(self):
        return self.position
    
    def setPosition(self, position):
        self.oldPosition = self.position
        self.position = position
        self.rect.centerx = self.getPosition()[0]
        self.rect.centery = self.getPosition()[1]
        
    def revertToOldPosition(self):
        self.setPosition(self.oldPosition)
        
    def setVector(self, vec):
        self.vector = vec
        
    def getVector(self):
        return self.vector
    
    def setSpeed(self, speed):
        self.speed = speed
        
    def getSpeed(self):
        return self.speed
    
    def getHeading(self):
        return self.heading
    
    def setHeading(self, heading):
        self.heading = heading
        self.angle = self.heading
        
    def setAcceleration(self, acceleration):
        self.acceeleration = acceleration
        
    def getAcceleration(self):
        return self.acceleration
    
    def setAngle(self, angle):
        self.angle = angle
        
    def getAngle(self):
        return self.angle
    
class StationaryObject(Object):
    def __init__(self, name, rect):
        Object.__init__(self, name, rect)
        self.VISIBLE_BY_SONAR = True
        self.TYPE = "StationaryObject"
        self.MASS = -1
        
class ContainerObject(Object):
    def __init__(self, name, rect):
        Object.__init__(self, name, rect)
        self.TYPE = "ContainerObject"