RoboCup Soccer Simulator
=======================

Owner: John Board
Authors:
 - John Board
Date: 15:09, 14/11/12

=======================

TODO:

Create UDP interface, for controling simulation and/or robots and other field objects.
Work on physics engine
Create more comphrehensive collision system
 - Each object knows what it is on/collided with much better.
Sensors

Everything apart from this is secondary - i.e. server mode.

=======================

Pre-Running:

You must have the following installed to run this program:

 - Python 2.7
 - Pygame

=======================

Running:

To open in console mode, open main.py, to open in no-console mode, open main_windowless.pyw.

=======================

Configuration:

Open constants.py, and edit the values, read the documentation at the top of constants.py
for information on what each constant does. All configuration to do directly with the simulation is
in the "Scripts" folder, to and then under topic.

Each configuration file, not to do with constants.py has the file type ".conf", and can be edited using notepad, 
or equivalent.

=======================

To write scripts for the simulator, the user must know atleast the basics about pythonical:

Variables (Lists, Dictionaries, and other basic types (ints, strings))
Methods
Class Inheritance, and other class related information
Syntax
Other general knowledge

=======================

Scripts/simulation.conf

These contains lists of what robots will be competing in the next match...

BlueTeamScripts: ["Team1_Offensive", "Team1_Defensive"]
RedTeamScripts: ["Team2_Offensive", "Team2_Defensive"]

For example.

You can only have 2 entries in each list.

=======================

Scripts/<Red/Blue>/config.conf:

config.conf in each team's folder should have the following variables:

StartingPositionKickoff, StartingPositionDefensive,

like so:

StartingPositionKickoff: {"Team2_Offensive": (x, y), "Team2_Defensive": (x, y)}
StartingPositionDefensive: {"Team2_Offensive": (x, y), "Team2_Defensive": (x, y)}

These positions outline the starting positions of the robots specified when starting each point, so, the start
of the kickoff, or recieving a kickoff.

===INFORMATION ABOUT THE POSITION RELATIVE TO BALL HERE===

=======================



