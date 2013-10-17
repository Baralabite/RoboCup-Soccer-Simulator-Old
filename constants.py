#Name: constants.py
#Date: 6:58PM, 27/10/12
#Author: John Board

import sys
sys.dont_write_bytecode = True

#---[Physics]---#



#---[Global]---#

#Software Types: "DEV", "SHAREWARE", "FULL"
SOFTWARE_LICENSE_TYPE = "FULL"
VERSION = 1.0
VERSION_DESCRIPTION = "Prototype Version"
NAME = "RoboCup Junior Soccer Simulator"

#---[Debug]---#

DEBUG_MODE = True
BY_STEP_DEBUGGING = False

#---[Screen]---#
INITAL_SCREEN_RESOLUTION = (640, 480)
SCREEN_RESOLUTION = INITAL_SCREEN_RESOLUTION
BACKGROUND_COLOR = (50, 50, 50)
LIMIT_FPS = True
FPS = 30
SCALABLE = True
SCALE_WORLD_SURFACE = True
DRAW_BOUNDING_BOXES = False
BOUNDING_BOX_COLOR = (0, 0, 255)
SHOW_SPLASH_ON_STARTUP = False
SPLASH_TIME = 2

#---[Team Names]---#

RED_TEAM_NAME = "John Board 1"    
BLUE_TEAM_NAME = "John Board 2"

#---[FPS]---#
SHOW_FPS = True
FPS_FONT_SIZE = 32
FPS_FONT_COLOR = (0, 255, 0)

#---[Logging]---#
LOGGING_FORMAT = "%(asctime)-15s %(message)s"
LOGGER_NAME = "Main"
LOG_FRAME_NUMBER = True
LOG_COLLISIONS = False

#---[Field]---#

#Unless you know what your doing, leave these settings alone

FIELD_SIZE = 122, 183
WORLD_SCALE = 1
WALL_WIDTH = 4 #Need to work on this feature
WORLD_SIZE = FIELD_SIZE[0]+60+WALL_WIDTH*2, FIELD_SIZE[1]+60+WALL_WIDTH*2
THREAD_PHYSICS = False
GOAL_WALL_WIDTH = 4 #Need to work on this feature
GOAL_WIDTH = 45
GOAL_DEPTH = 8
DIST_FROM_WALL_TO_GOAL = 22

BALL_SIZE = 4

#---[Robot]---#
MAX_TURNING_SPEED = 4
MAX_SIZE = 22 #CM Diameter
ROBOT_SIZE = 16
MAX_ROBOT_TURNING_SPEED = 2

#===[On Goal]===#
#0: Straigtaway, 1: Takes some time, 2: Wait for user
ON_GOAL_OPTION = 2
ON_GOAL_WAIT_TIME = 2

#---[Simulation.conf Defaults]---#
CONF_DEFAULTS = {"BlueTeam": 2,
                "ReadTeam": 2,
                "BlueTeamScripts": ["Blue_Offensive", "Blue_Defensive"],
                "RadTeamScripts": ["Red_Offensive", "Red_Offensive"]
                    }