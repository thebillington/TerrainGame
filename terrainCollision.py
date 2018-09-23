# Get imports
import pygame
from pygame.locals import *
import sys
import math

# Create a game class
class Game(object):
	
	# Constructor
	def __init__(self):
		
		# Initialize pygame
		pygame.init()
		
		# Create the window
		self.size = self.width, self.height = 800, 600
		self.screen = pygame.display.set_mode(self.size)
		pygame.display.set_caption("Terrain")
		
		# Background colour
		self.bg = (200, 200, 200)
		
		# Create the game clock
		self.clock = pygame.time.Clock()
		
		# Create a list to store all of the pieces of terrain
		self.terrain = []
		
		# Create an object to store the projectile
		self.projectile = None
		
		# Create a list to store the players
		self.players = []
		
		self.powerups = [RadiusPowerup(pygame.image.load('res/powerUp1.png')), HitsPowerup(pygame.image.load('res/powerUp2.png'))]
		self.powerups[1].setPos(400, 100)
		
		self.projectiles = []
		
	# Function to draw the initial screen
	def drawMap(self):
	
		# Clear the screen
		self.screen.fill(self.bg)
		
		# Draw all terrain
		self.drawTerrain()
		
	# Function to update the game
	def update(self):
		
		# Check for exit
		self.exit()
		
		# Update the proejectile
		self.updateProjectile()
		
		# Update the players
		self.updatePlayers()
		
		# Check that there is a projectile to draw
		
		# Check if there is a projectile
		for x in self.projectiles:
			
			self.projectile = x
		
			if not self.projectile == None:
			
				# Draw the projectile
				pygame.draw.rect(self.screen, (0, 0, 255), self.projectile.rect)
		
		for x in self.powerups:
			
			if x.active:
				
				x.draw(self.screen)
		
		# Update the display
		pygame.display.flip()
		
		# Tick
		self.clock.tick(60)
		
	# Function to update the position of the projectile
	def updateProjectile(self):
		
		# Check if there is a projectile
		for x in self.projectiles:
			
			self.projectile = x
			if not self.projectile == None:
			
				# Draw the projectile
				pygame.draw.rect(self.screen, self.bg, self.projectile.rect)
			
				# Move the projectile
				self.projectile.rect.left += self.projectile.speed[0]
				self.projectile.rect.top += self.projectile.speed[1]
				
				# Update gravity
				if self.projectile.speed[1] < self.projectile.maxSpeed:
					self.projectile.speed[1] += self.projectile.gravity
			
				# Check for projectile collision
				self.projectileCollision()
			
	# Function to update the players
	def updatePlayers(self):
		
		# Check pressed keys
		keys = pygame.key.get_pressed()
				
		# If left arrow
		if keys[K_LEFT]:
			
			# Set speed to move left
			self.players[0].direction = -1
			
		# If right arrow
		elif keys[K_RIGHT]:
			
			# Set speed to move right
			self.players[0].direction = 1
			
		# Otherwise reset player speed
		else:
			
			# Set speed to 0
			self.players[0].direction = 0
			
		# If up arrow
		if keys[K_UP]:
			
			# Have to add jump functionality
			self.players[0].jump()
			
		# If down arrow
		if keys[K_DOWN]:
			
			self.fire(0)
				
		# If a key
		if keys[K_a]:
			
			# Move the player to the left
			self.players[1].direction = -1
			
		# Else if d key
		elif keys[K_d]:
			
			# Move the player to the left
			self.players[1].direction = 1
		
		# If neither a or d are pressed
		else:
			
			# Stop all player movment
			self.players[1].direction = 0
			
		# Check the w key
		if keys[K_w]:
			
			#Peform jump
			self.players[1].jump()
			
		# Check the down key
		if keys[K_s]:
			
			# Need to add bomb functionality
			self.fire(1)
		
		for powerup in self.powerups:
			
			if powerup.active:
			
				for player in self.players:
				
					if powerup.rect.colliderect(player.rect):
					
						powerup.power(player)
					
		# Update each player
		for p in self.players:
			
			# Remove the player current position d
			pygame.draw.rect(self.screen, self.bg, p.rect)
			
			# Update the player
			p.update()
			
			# Update physics
			self.playerCollision()
			
			# Redraw the player
			self.screen.blit(p.image, p.rect)
			
	def fire(self, x):
		
		if self.players[x].bombCooldown():
			
				# Create a projectile
				p = Projectile(pygame.Rect(self.players[x].rect.x + 3, self.players[x].rect.y, 6, 6), [self.players[x].direction, 0], 0.1, 3, self.players[x].blastRadius, self.players[x].hits)
				
				if not self.players[x].uses[0] == 0:
					self.players[x].uses[0] -= 1
					
				if self.players[x].uses[0] == 0:
					self.players[x].blastRadius = 8
					
				if not self.players[x].uses[1] == 0:
					self.players[x].uses[1] -= 1
					
				if self.players[x].uses[1] == 0:
					self.players[x].hits = 0
					
				g.addProjectile(p)
				
				self.players[x].ableToFire = False
		
	# Function to check if projectile has collided with any terrain
	def projectileCollision(self):
		
		# Set px and py to none
		px = None
		py = None
		
		# Iterate over all the terrain
		for t in self.terrain:
			
			for x in range(len(self.projectiles)):
				
				self.projectile = self.projectiles[x]
			
				# If the projectile has collided with the bounding box
				if self.projectile.rect.colliderect(t.bounds):
					
					# Check each of the pixels in the terrain
					for p in t.pixels:
						
						# If the pixel has collided with the projectile
						if self.projectile.rect.colliderect(p):
							
							# Store the pixels location
							px = p.left
							py = p.top
							
							# Break the loop
							break
							
					# Check whether there was a collision between any pixels
					if not px == None:
						
						# Check each pixel to see whether it collided, and if so delete it
						for i in range(len(t.pixels) - 1, -1, -1):
							
							# If the pixel is in range of the blast zone
							if pythagoras(t.pixels[i].left, t.pixels[i].top, px, py) < self.projectile.blastRadius:
								
								# Delete the pixel
								t.pixels.pop(i)
						
						# Redraw this terrain
						pygame.draw.rect(self.screen, self.bg, t.bounds)
						for p in t.pixels:
							pygame.draw.rect(self.screen, (0, 0, 0), p)
						
						# Check if the projectile is a one hit
						if self.projectile.oneHit == 0:
							del self.projectiles[x]
							break
							
						self.projectile.oneHit -= 1
  
	# Function to resolve player collisions
	def playerCollision(self):
		
		# For each player
		for player in self.players:
		
			# Iterate over all the terrain
			for t in self.terrain:
				
				# If the player has collided with the bounding box
				if player.rect.colliderect(t.bounds):
					
					# Check if the player has collided horizontally or vertically
					if not player.speedX == 0:
					
						# While the player is colliding with a pixel in the current terrain
						while self.pixelCollision(player, t):
						
							# Set player to not be jumping
							player.jumping = False
							
							# Check the terrain type and respond to horizontal
							if t.terrainType == "horizontal":
							
								# Move the player away from the wall by one pixel toward direction of travel
								player.rect.x += player.direction
								
								# Move the player up by one pixel
								player.rect.y -= 1
								
							# Or vertical terrain
							else:
							
								# Move the player away from the wall by one pixel against direction of travel
								player.rect.x -= player.direction
							
					# Otherwise resolve on y axis
					else:
					
						# While the player is colliding with a pixel in the current terrain
						while self.pixelCollision(player, t):
							
							# Set player to not be jumping
							player.jumping = False
							
							# Move the player up by one pixel
							player.rect.y -= 1
						
	# Function to return true when the player is colliding with a pixel within a bounding box
	def pixelCollision(self, player, terrain):
		
		# Iterate over each of the pixels in the terrain and return true if there's a collision
		for p in terrain.pixels:
					
			# If the pixel has collided with the player
			if player.rect.colliderect(p):
				return True
		
    # Return false if there are no collisions
		return False
		
	# Function to draw the terrain
	def drawTerrain(self):
		
		# Iterate over all the terrain
		for t in self.terrain:
			
			# For each pixel in the terrain
			for p in t.pixels:
				
				# Light the pixel
				pygame.draw.rect(self.screen, (0, 0, 0), p)

			# Draw the bounding box
			#pygame.draw.rect(self.screen, (255, 0, 0), t.bounds, 1)
		
	# Create a function to add terrain
	def addTerrain(self, terrain):
		
		# Add the terrain
		self.terrain.append(terrain)
		
	# Create a function to add terrain
	def addPlayer(self, player):
		
		# Add the terrain
		self.players.append(player)
		
	# Function to create a projectile
	def addProjectile(self, projectile):
		
		# Set projectile
		self.projectiles.append(projectile)
        
	# Function to check for user closing the window
	def exit(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
				

	# Function to read data from file and create terrain objects
	def readFileToTerrain(self, fileName):
                
                # create new file object with read mode
                file = open(fileName)
                
                # create a list of the lines in the text file
                fileLines = file.read().splitlines()

                #iterate through each line in the file
                for line in fileLines:
                        #seperate the values between commas
                        fields = line.split(",")
                        
                        # Create a terrain object
                        t = Terrain(pygame.Rect(int(fields[0]), int(fields[1]), int(fields[2]), int(fields[3])), fields[4])
	
                        # Add some pixels to the terrain
                        for i in range(int(fields[2])):
                                for j in range(int(fields[3])):
                                        t.addPixel(pygame.Rect(t.bounds.left + i, t.bounds.top + j, 1, 1))

                        #add to the games terrain
                        self.addTerrain(t)
	
				
# Class to hold all the 'pixels' in a piece of terrain
class Terrain(object):
	
	# Constructor
	def __init__(self, locationRect, terrainType):
		
		# List to hold all of the 'pixels'
		self.pixels = []
		
		# Store a rectangle to be the bounding box of the terrain
		self.bounds = locationRect
		
		# Store the type of the terrain (horizontal or vertical)
		self.terrainType = terrainType
		
	# Function to add a pixel to the terrain
	def addPixel(self, pixel):
		
		# Add the pixel
		self.pixels.append(pixel)
		
# Class to hold information about a projectile
class Projectile(object):
	
	# Constructor
	def __init__(self, rect, speed, gravity, maxSpeed, collisionRadius, oneHit):
		
		# Fields
		self.rect = rect
		self.speed = speed
		self.gravity = gravity
		self.maxSpeed = maxSpeed
		self.blastRadius = collisionRadius
		self.oneHit = oneHit
		
# Pythagoras function
def pythagoras(xOne, yOne, xTwo, yTwo):
	
	# Return the absolute distance
	return math.sqrt(math.pow(xOne - xTwo, 2) + math.pow(yOne - yTwo, 2))

# Class to hold the player object
class Player(object):
	
	# Constructor
	def __init__(self, x, y, imgRes):
		
		# Get the player image from the provided resource
		self.image = pygame.image.load(imgRes)
		self.rect = self.image.get_rect()
		
		# Set the x and y
		self.rect.x = x
		self.rect.y = y
		
		# Store the horizontal speed
		self.hzSpeed = 2
		
		# Set the direction of the player
		self.direction = 0
		
		# Set the speed
		self.speedX = 0
		self.speedY = 0
		
		# Set the physics variables
		self.jumpSpeed = -2
		self.gravity = 0.1
		self.maxSpeed = 6
		
		# Check whether the player is jumping
		self.jumping = True
		
		#Create an array to hold the projectiles
		self.projectiles = []
		
		# Create a int to hold the blast radius of inpacts
		self.blastRadius = 8
		# Create an array to hold the two types of powerups uses
		self.uses = [0, 0]
		
		# An int to stop the bombs from being spamed multiple times
		self.cooldown = 0
		
		# An int to hold how many times a projectile can hit before deipersing
		self.hits = 0
		
		self.ableToFire = True
		
	# Function to update the player
	def update(self):
			
		# Remove the player current position
		#pygame.draw.rect(self.screen, self.bg, self.players[0].rect)
		
		# Check whether the player needs to accelerate
		if self.speedY < self.maxSpeed:
			
			# Accelerate
			self.speedY += self.gravity
			
		# Move the player
		self.speedX = self.direction * self.hzSpeed
		self.rect.x += self.speedX
		self.rect.y += self.speedY
			
		# If we are jumping, move twice on x to make up for platform collision checks
		if self.jumping:
			self.rect.x += 2 * self.speedX
			
		if self.uses[0] >= 1:
			self.blastRadius = 20
			
		if self.uses[1] >= 1:
			self.hits = 1
		
	# Function to make a player jump
	def jump(self):
		
		# If not already jumping
		if not self.jumping:
			
			# Set jumping to true
			self.jumping = True
		
			# Set the ySpeed to jump speed
			self.speedY = self.jumpSpeed

	def bombCooldown(self):
		
		if not self.ableToFire:
		
			if not self.cooldown == 10:
				
				self.cooldown += 1
			
		if self.cooldown == 10:
			
			self.ableToFire = True
			self.cooldown = 0
			
		if self.ableToFire:
			
			return True
			
		return False

# Create the powerup class		
class Powerup(object):
	
	#Constructor
	def __init__(self, image, x=0, y=0):
		
		self.image = image
		self.rect = self.image.get_rect()
		
		self.rect.x = x
		self.rect.y = y
		
		self.active = True
		
	def draw(self, surface):
		
		surface.blit(self.image, self.rect)
		
	def setPos(self, x, y):
		
		self.rect.x = x
		self.rect.y = y
		
class RadiusPowerup(Powerup):
	
	def __init__(self, image, uses=3, x=0, y=0):
		super(RadiusPowerup, self).__init__(image, x, y)
		
		self.uses = uses
		
	def power(self, player):
		
		player.uses[0] = self.uses
		player.uses[1] = 0
		
class HitsPowerup(Powerup):
	
	def __init__(self, image, uses=3, x=0, y=0):
		super(HitsPowerup, self).__init__(image, x, y)
		
		self.uses = uses
		
	def power(self, player):
		
		player.uses[1] = self.uses
		player.uses[0] = 0
	
# Run an instance of the game
if __name__ == "__main__":
	
	# Create a game object
	g = Game()
	
	# Create a player object
	player = Player(200, 30, 'res/player.png')
	player2 = Player(600, 30, 'res/player2.png')
	
	# Add the player to the game
	g.addPlayer(player)
	g.addPlayer(player2)
	
	# Read the level data
	g.readFileToTerrain("test.txt")
	
	# Draw the map
	g.drawMap()
	
	# Game loop
	while True:
		g.update()
