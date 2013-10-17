#Name: main.py
#Date: 6:58PM, 27/10/12
#Author: John Board

import constants, taskmanager, events, eventhandler
import profiler, logger, pygame, scripthandler
import configparser, physics, time, os
from Soccer import world
import sys
sys.dont_write_bytecode = True
os.environ['SDL_VIDEO_CENTERED'] = '1'

#TODO:
#
#Make The Moving->Solid collision more realistic (change aom instead of heading)
#Custom Collision Detection Engine
#
#

class Application:    
    def __init__(self):        
        self.elapsed = 0
        self.mainLoopSpeed = 0
        
        self.isInFullscreen = False
        
        self.taskmanager = taskmanager.TaskManager()
        self.logger = logger.Logger(self.taskmanager)

        self.logger.logNoTag(logger.logging.INFO, "=====[PyGame]=====")
        pygame.init()                                                  
        self.logger.info("Pygame Started.")
        self.logger.logNoTag(logger.logging.INFO, "==================\n")

        self.initProfiler = profiler.Profiler(self.logger, "Initalization", self.taskmanager)
        self.initProfiler.startTimer()

        self.mainLoopProfiler = profiler.Profiler(self.logger, "MainLoop", self.taskmanager)    
        self.eventhandler = eventhandler.EventHandler(self.logger, self.taskmanager)            
        self.initEvents()

        self.running = True    
        
        if constants.SHOW_SPLASH_ON_STARTUP:
            surf = pygame.display.set_mode(constants.SCREEN_RESOLUTION, pygame.NOFRAME)
            image = pygame.image.load("Data/logo.png")
            image.convert()
            surf.fill((0,0,0))
            pygame.event.pump()
            surf.blit(image, (0,0)) 
            pygame.display.flip()
            time.sleep(constants.SPLASH_TIME)
        
        if constants.SCALABLE:
            self.screen = pygame.display.set_mode(constants.SCREEN_RESOLUTION, pygame.RESIZABLE)
        else:
            self.screen = pygame.display.set_mode(constants.SCREEN_RESOLUTION)
        pygame.display.set_caption(constants.NAME)
        
        self.config = configparser.ConfigParser("Scripts/simulation.conf", self.logger, self.taskmanager)
        
        self.scripthandler = scripthandler.ScriptHandler(self.logger, self.taskmanager)
        
        self.physics = physics.PhysicsEngine(self.logger, self.taskmanager, self.eventhandler)
        
        self.world = world.World(self.physics, self.logger, self.screen, self.taskmanager, self.config, self.scripthandler)    #Start World
        self.world.loadAllRobots()

        self.fpsFont = pygame.font.Font("freesansbold.ttf", constants.FPS_FONT_SIZE)             
        
        self.initProfiler.stopTimer()
        if constants.SHOW_SPLASH_ON_STARTUP:
            time = self.initProfiler.getTime()-constants.SPLASH_TIME*1000
        else:
            time = self.initProfiler.getTime()
        self.logger.debug("Startup finished in (Excluding Splash): "+str(time)+"ms.")
        self.logger.logNoTag(logger.logging.INFO, "======================================================")
        
        
    def start(self):
        self.loop()
        
    def stop(self, event=None):
        if not event==None:
            if not event.isCancelled():
                
                if constants.DEBUG_MODE:
                    self.logger.displayTimes()
                
                self.running = False
        
                pygame.quit()
                quit()
        else:
            if constants.DEBUG_MODE:
                self.logger.displayTimes()
            self.running = False
            pygame.quit()
            quit()
        
    def initEvents(self):
        self.logger.info("Registering Event Listeners.")
        self.eventhandler.addEventListener("QuitButtonEvent", events.EventType.PYGAME_QUIT, self.stop)
        self.eventhandler.addEventListener("WindowResizeEvent", events.EventType.PYGAME_WINDOW_RESIZE, self.PygameWindowResizeEvent)        
        self.eventhandler.addEventListener("PygameKeydownEvent", events.EventType.PYGAME_KEYDOWN, self.PygameKeydownEvent)
        
    def loop(self):
        while self.running:
            spacePressed = False
            self.mainLoopProfiler.startTimer()                                 
            
            
            #-----[Main Loop]-----#
            self.screen.fill(constants.BACKGROUND_COLOR)                       
            for e in pygame.event.get():                                       
                self.handlePygameEvents(e)
            self.taskmanager.update(constants.FPS)                                             
    
            #-----[Put Updating Code Here]-----#
            
            if constants.BY_STEP_DEBUGGING:
                key = pygame.key.get_pressed()
                if key[pygame.K_s]:
                    spacePressed = True
                    self.world.update()
                    if constants.SHOW_FPS == True:
                        self.drawFPS()
                    self.eventhandler.callEvents(events.EventType.MAINLOOP_UPDATE, events.MainLoopUpdateEvent(self.taskmanager.getFPS()))
            else:
                self.world.update()
                if constants.SHOW_FPS == True:
                    self.drawFPS()
                self.eventhandler.callEvents(events.EventType.MAINLOOP_UPDATE, events.MainLoopUpdateEvent(self.taskmanager.getFPS()))
        
            #----------------------------------#
            
            if constants.LOG_FRAME_NUMBER:
                self.logger.logFrame(self.taskmanager.getFrameCount())
            
            if constants.BY_STEP_DEBUGGING:
                if spacePressed:
                    pass
                    pygame.display.flip()                                      
            else:
                pass
                pygame.display.flip()
            #---------------------#
            
            self.mainLoopProfiler.stopTimer()
            
    #---[Misc]---#
    
    def drawFPS(self):
        self.taskmanager.getFPS()
        textSurface = self.fpsFont.render(str(int(self.taskmanager.getFPS())), 1, constants.FPS_FONT_COLOR)
        pos = (constants.SCREEN_RESOLUTION[0] - textSurface.get_width()-10, 5)
        self.screen.blit(textSurface, pos)
    
    def handlePygameEvents(self, e):
        if e.type==pygame.KEYDOWN:
            key = e.dict["key"]
            event = events.PygameKeydownEvent()
            event.setData(key)
            self.eventhandler.callEvents(events.EventType.PYGAME_KEYDOWN, event)
        elif e.type==pygame.QUIT:
            event = events.PygameQuitButtonEvent()
            self.eventhandler.callEvents(events.EventType.PYGAME_QUIT, event)
        elif e.type==pygame.VIDEORESIZE:
            event = events.PygameWindowResizeEvent()            
            event.setData(e)
            self.eventhandler.callEvents(events.EventType.PYGAME_WINDOW_RESIZE, event)
            
    def PygameWindowResizeEvent(self, e):
        if e.isCancelled():
            self.screen = pygame.display.set_mode(constants.INITAL_SCREEN_RESOLUTION, pygame.RESIZABLE)
        else:
            constants.SCREEN_RESOLUTION = e.getData().dict['size']
            self.logger.debug("Window Was Resized: "+str(e.getData().dict))
            self.world.resizeToFitScreen()
            self.screen = pygame.display.set_mode(constants.SCREEN_RESOLUTION, pygame.RESIZABLE)
            
    def PygameKeydownEvent(self, e):
        e = e.getData()
        if e==pygame.K_ESCAPE:
            self.stop()
            
        elif e==pygame.K_F11:
            if self.isInFullscreen:
                pygame.display.set_mode(constants.SCREEN_RESOLUTION, pygame.RESIZABLE)
                self.isInFullscreen = False
            else:
                pygame.display.set_mode(constants.SCREEN_RESOLUTION, pygame.FULLSCREEN)
                self.isInFullscreen = True
            self.logger.debug("Toggling Fullscreen")
        elif e==pygame.K_F12:
            self.logger.displayTimes()
            
        
        if constants.DEBUG_MODE:
            ball = self.world.getRobot("Red", "Team1_Offensive")
            speed = 1
            if e==pygame.K_KP6:
                ball.setHeading(0)
                ball.setSpeed(speed)
            elif e==pygame.K_KP3:
                ball.setHeading(45)
                ball.setSpeed(speed)
            elif e==pygame.K_KP2:
                ball.setHeading(90)
                ball.setSpeed(speed)
            elif e==pygame.K_KP1:
                ball.setHeading(135)
                ball.setSpeed(speed)
            elif e==pygame.K_KP4:
                ball.setHeading(180)
                ball.setSpeed(speed)
            elif e==pygame.K_KP7:
                ball.setHeading(225)
                ball.setSpeed(speed)
            elif e==pygame.K_KP8:
                ball.setHeading(270)
                ball.setSpeed(speed)
            elif e==pygame.K_KP9:
                ball.setHeading(315)
                ball.setSpeed(speed)
            elif e==pygame.K_KP5:
                ball.setSpeed(0)
            elif e==pygame.K_KP0:
                ball.moveToCenter()

if __name__ == "__main__":
    app = Application()
    app.start()
    os.system("pause")
    
    