import physics, constants, pygame

#=====[Top Goal]=====#

redGoals = 0
blueGoals = 0

class TopGoalContainer(physics.ContainerObject):
	def __init__(self, name, surf):
		self.rect = surf.get_rect()		
		
		self.rect.left = (constants.WORLD_SIZE[0]/2)-(constants.GOAL_WIDTH/2)
		self.rect.top = constants.WALL_WIDTH+22
		self.rect.width = constants.GOAL_WIDTH
		self.rect.height = constants.GOAL_DEPTH
		
		physics.ContainerObject.__init__(self, name, self.rect)
		
		self.surf = surf
		
	def update(self):
		pass
		
	def draw(self):
		pygame.draw.rect(self.surf, (255, 100, 100), self.rect) #(100, 100, 255)
		
class TopGoalBackWall(physics.StationaryObject):
	def __init__(self, name, surf):
		rect = surf.get_rect()
		
		rect.left = (constants.WORLD_SIZE[0]/2)-(constants.GOAL_WIDTH/2)
		rect.top = 22+constants.WALL_WIDTH-constants.GOAL_WALL_WIDTH
		rect.width = constants.GOAL_WIDTH
		rect.height = constants.GOAL_WALL_WIDTH
		
		physics.StationaryObject.__init__(self, name, rect)
		self.surf = surf
		
	def update(self):
		pass
		
	def draw(self):
		pygame.draw.rect(self.surf, (0,0,0), self.rect)
		
class TopGoalLeftWall(physics.StationaryObject):
	def __init__(self, name, surf):
		rect = surf.get_rect()
		rect.height = constants.GOAL_WALL_WIDTH+22+constants.WALL_WIDTH
		rect.top = constants.WALL_WIDTH
		rect.width = constants.GOAL_WALL_WIDTH
		rect.left = (constants.WORLD_SIZE[0]/2)-(constants.GOAL_WIDTH/2)-constants.GOAL_WALL_WIDTH
		
		physics.StationaryObject.__init__(self, name, rect)
		self.surf = surf
		
	def update(self):
		pass
		
	def draw(self):
		pygame.draw.rect(self.surf, (0,0,0), self.rect)
		
class TopGoalRightWall(physics.StationaryObject):
	def __init__(self, name, surf):
		rect = surf.get_rect()
		
		rect.left = (constants.WORLD_SIZE[0]/2)-(45/2)+constants.GOAL_WIDTH
		rect.top = constants.WALL_WIDTH
		rect.width = constants.GOAL_WALL_WIDTH
		rect.height = constants.GOAL_WALL_WIDTH+constants.DIST_FROM_WALL_TO_GOAL+constants.WALL_WIDTH
		
		physics.StationaryObject.__init__(self, name, rect)
		self.surf = surf
		
	def update(self):
		pass
		
	def draw(self):
		pygame.draw.rect(self.surf, (0,0,0), self.rect)
		
#=====[Bottom Goal]=====#
		
class BottomGoalContainer(physics.ContainerObject):
	def __init__(self, name, surf):
		self.rect = surf.get_rect()		
		
		self.rect.left = (constants.WORLD_SIZE[0]/2)-(constants.GOAL_WIDTH/2)
		self.rect.top = constants.WORLD_SIZE[1]-30-constants.WALL_WIDTH
		self.rect.width = constants.GOAL_WIDTH
		self.rect.height = constants.GOAL_DEPTH
		
		physics.ContainerObject.__init__(self, name, self.rect)
		
		self.surf = surf
		
	def update(self):
		pass
		
	def draw(self):
		pygame.draw.rect(self.surf, (100, 100, 255), self.rect)
		
class BottomGoalBackWall(physics.StationaryObject):
	def __init__(self, name, surf):
		rect = surf.get_rect()
		
		rect.left = (constants.WORLD_SIZE[0]/2)-(constants.GOAL_WIDTH/2)
		rect.top = constants.WORLD_SIZE[1]-constants.WALL_WIDTH-constants.DIST_FROM_WALL_TO_GOAL
		rect.width = constants.GOAL_WIDTH
		rect.height = constants.GOAL_WALL_WIDTH
		
		physics.StationaryObject.__init__(self, name, rect)
		self.surf = surf
		
	def update(self):
		pass
		
	def draw(self):
		pygame.draw.rect(self.surf, (0,0,0), self.rect)
		
class BottomGoalLeftWall(physics.StationaryObject):
	def __init__(self, name, surf):
		rect = surf.get_rect()
		rect.left = (constants.WORLD_SIZE[0]/2)-(constants.GOAL_WIDTH/2)-constants.GOAL_WALL_WIDTH
		rect.top = constants.WORLD_SIZE[1]-constants.DIST_FROM_WALL_TO_GOAL-constants.GOAL_DEPTH-constants.WALL_WIDTH
		rect.width = constants.GOAL_WALL_WIDTH
		rect.height = constants.GOAL_WALL_WIDTH+constants.DIST_FROM_WALL_TO_GOAL+constants.WALL_WIDTH
		
		physics.StationaryObject.__init__(self, name, rect)
		self.surf = surf
		
	def update(self):
		pass
		
	def draw(self):
		pygame.draw.rect(self.surf, (0,0,0), self.rect)
		
class BottomGoalRightWall(physics.StationaryObject):
	def __init__(self, name, surf):
		rect = surf.get_rect()
		
		rect.left = (constants.WORLD_SIZE[0]/2)+(constants.GOAL_WIDTH/2)+1
		rect.top = constants.WORLD_SIZE[1]-constants.DIST_FROM_WALL_TO_GOAL-constants.GOAL_DEPTH-constants.WALL_WIDTH
		rect.width = constants.GOAL_WALL_WIDTH
		rect.height = constants.GOAL_WALL_WIDTH+constants.DIST_FROM_WALL_TO_GOAL+constants.WALL_WIDTH
		
		physics.StationaryObject.__init__(self, name, rect)
		self.surf = surf
		
	def update(self):
		pass
		
	def draw(self):
		pygame.draw.rect(self.surf, (0,0,0), self.rect)
		
#=====[Goal Logo Containers]=====#

class TopGoalLogo(physics.StationaryObject):
	def __init__(self, name, surf):
		self.rect = surf.get_rect()		
		
		#self.image = pygame.image.load("Data/robocup_soccer_logo.png")
		#self.image.convert()
		
		self.font = pygame.font.Font("freesansbold.ttf", 16)   
		
		self.rect.left = (constants.WORLD_SIZE[0]/2)
		self.rect.top = constants.WALL_WIDTH+1
		self.rect.width = 21
		self.rect.height = 14
		#self.rect.width = self.image.get_width()
		#self.rect.height = self.image.get_height()
		
		physics.StationaryObject.__init__(self, name, self.rect)
		
		self.surf = surf
		
	def draw(self):
		t = self.font.render(str(redGoals), 1, (0, 50, 0))
		self.surf.blit(t, (self.rect.left, self.rect.top))
		
class BottomGoalLogo(physics.StationaryObject):
	def __init__(self, name, surf):
		self.rect = surf.get_rect()	
		
		self.font = pygame.font.Font("freesansbold.ttf", 16)	
		
		#self.image = pygame.image.load("Data/robocup_soccer_logo.png")
		#self.image.convert()
		
		self.rect.left = (constants.WORLD_SIZE[0]/2)
		self.rect.top = constants.WORLD_SIZE[1]-constants.WALL_WIDTH-16
		self.rect.width = 21
		self.rect.height = 14
		
		physics.StationaryObject.__init__(self, name, self.rect)
		
		self.surf = surf
		
	def draw(self):
		t = self.font.render(str(blueGoals), 1, (0, 50, 0))
		self.surf.blit(t, (self.rect.left, self.rect.top))
		
#=====[Top Penlalty Box]=====#

class TopPenaltyBoxContainer(physics.ContainerObject):
	def __init__(self, name, surf):
		self.rect = surf.get_rect()		
		
		self.rect.left = (constants.WORLD_SIZE[0]/2)-(constants.GOAL_WIDTH/2)
		self.rect.height = constants.GOAL_WIDTH
		self.rect.width = constants.GOAL_WIDTH
		self.rect.top = constants.WALL_WIDTH+constants.DIST_FROM_WALL_TO_GOAL+constants.GOAL_DEPTH
		
		physics.ContainerObject.__init__(self, name, self.rect)
		
		self.surf = surf
		
	def update(self):
		pass
		
	def draw(self):
		pygame.draw.rect(self.surf, (0, 50, 0), self.rect)

class BottomPenaltyBoxContainer(physics.ContainerObject):
	def __init__(self, name, surf):
		self.rect = surf.get_rect()		
		
		self.rect.left = (constants.WORLD_SIZE[0]/2)-(constants.GOAL_WIDTH/2)
		self.rect.top = constants.WORLD_SIZE[1]-constants.DIST_FROM_WALL_TO_GOAL-constants.GOAL_WIDTH-constants.GOAL_WALL_WIDTH-constants.GOAL_DEPTH
		self.rect.width = constants.GOAL_WIDTH
		self.rect.height = constants.GOAL_WIDTH
		
		physics.ContainerObject.__init__(self, name, self.rect)
		
		self.surf = surf
		
	def update(self):
		pass
		
	def draw(self):
		pygame.draw.rect(self.surf, (0, 50, 0), self.rect)

#=====[Field]=====#

class OutField(physics.ContainerObject):
	def __init__(self, name, surf):
		self.rect = surf.get_rect()		
		self.rect.width = self.rect.width - constants.WALL_WIDTH*2
		self.rect.left = self.rect.left + constants.WALL_WIDTH
		self.rect.height = self.rect.height - constants.WALL_WIDTH*2
		self.rect.top = self.rect.top + constants.WALL_WIDTH
		
		physics.ContainerObject.__init__(self, name, self.rect)
		
		self.surf = surf
		
	def update(self):
		pass
		
	def draw(self):
		self.surf.fill((255, 255, 255))
		
class PlayingZone(physics.ContainerObject):
	def __init__(self, name, surf):
		self.rect = surf.get_rect()
		
		self.rect.left = constants.WALL_WIDTH+30
		self.rect.width = constants.FIELD_SIZE[0]
		self.rect.top = constants.WALL_WIDTH+30
		self.rect.height = constants.FIELD_SIZE[1]
		
		physics.ContainerObject.__init__(self, name, self.rect)
		
		self.surf = surf
	
	def update(self):
		pass
	
	def draw(self):
		pygame.draw.rect(self.surf, (0, 200, 0), self.rect)
		
class InnerPlayingZone(physics.ContainerObject):
	def __init__(self, name, surf):
		self.rect = surf.get_rect()
		
		self.rect.left = (constants.WORLD_SIZE[0]/2)-(constants.GOAL_WIDTH/2)
		self.rect.width = constants.GOAL_WIDTH
		self.rect.top = constants.WALL_WIDTH+constants.DIST_FROM_WALL_TO_GOAL+constants.GOAL_DEPTH+constants.GOAL_WIDTH
		self.rect.height = constants.FIELD_SIZE[1]-(constants.GOAL_WIDTH*2)
		
		physics.ContainerObject.__init__(self, name, self.rect)
		
		self.surf = surf
		
	def draw(self):
		pygame.draw.rect(self.surf, (0, 100, 0), self.rect)		

#=====[Borders]=====#
		
class NorthWall(physics.StationaryObject):
	def __init__(self, name, surf):
		rect = surf.get_rect()
		rect.height = constants.WALL_WIDTH
		physics.StationaryObject.__init__(self, name, rect)
		self.surf = surf
		
	def update(self):
		pass
		
	def draw(self):
		pygame.draw.rect(self.surf, (0,0,0), self.rect)
		
class EastWall(physics.StationaryObject):
	def __init__(self, name, surf):
		rect = surf.get_rect()
		rect.left = rect.width-constants.WALL_WIDTH
		rect.width = constants.WALL_WIDTH
		physics.StationaryObject.__init__(self, name, rect)
		self.surf = surf
		
	def update(self):
		pass
		
	def draw(self):
		pygame.draw.rect(self.surf, (0,0,0), self.rect)
		
class SouthWall(physics.StationaryObject):
	def __init__(self, name, surf):
		rect = surf.get_rect()
		rect.top = rect.height - constants.WALL_WIDTH
		rect.height = constants.WALL_WIDTH
		physics.StationaryObject.__init__(self, name, rect)
		self.surf = surf
		
	def update(self):
		pass
		
	def draw(self):
		pygame.draw.rect(self.surf, (0,0,0), self.rect)
		
class WestWall(physics.StationaryObject):
	def __init__(self, name, surf):
		rect = surf.get_rect()
		rect.width = constants.WALL_WIDTH
		physics.StationaryObject.__init__(self, name, rect)
		self.surf = surf
		
	def update(self):
		pass
		
	def draw(self):
		pygame.draw.rect(self.surf, (0,0,0), self.rect)
		
#=====[Ball]=====#
		
class Ball(physics.MovingObject):
	def __init__(self, name, rect, surf):
		physics.MovingObject.__init__(self, name, rect)
		self.FRICTION = 2
		self.MASS = 0.1
		self.BOUNCYNESS = 10
		self.RADIUS = constants.BALL_SIZE
		
		self.setPosition((constants.WORLD_SIZE[0]/2, constants.WORLD_SIZE[1]/2))
		self.surf = surf 
				
	def update(self):
		pass
	
	def draw(self):
		pygame.draw.circle(self.surf, (255, 255, 0), (self.rect.centerx, self.rect.centery), self.RADIUS)
		
	def onCollide(self, data):
		global redGoals, blueGoals
		if data.getName()=="TopGoalBackWall":
			blueGoals += 1
			self.moveToCenter()
		elif data.getName()=="BottomGoalBackWall":
			redGoals += 1
			self.moveToCenter()
		elif data.getName()=="NorthWall" or data.getName()=="WestWall" or data.getName()=="EastWall" or data.getName()=="SouthWall":
			self.moveToCenter()
		