# Get imports
import pygame
from pygame.locals import *
import sys
import math
from random import choice, randint

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
		
		# Create a list to store the players
		self.players = []
		
		# List to store the powerups
		self.powerups = []
		
		# List to store the available powerups constructors
		self.possPowerups = [DrillPowerup, NukePowerup]
		
		# List to store the projectiles
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
		self.updateProjectiles()
		
		# Update the players
		self.updatePlayers()
		
		# Update the powerups
		self.updatePowerups()
		
		# For each projectile
		for p in self.projectiles:
			
			# Draw the projectile
			pygame.draw.rect(self.screen, (0, 0, 255), p.rect)
		
		# Draw the powerups
		for p in self.powerups:
			p.draw(self.screen)
		
		# Update the display
		pygame.display.flip()
		
		# Tick
		self.clock.tick(60)
		
	# Function to update the position of the projectiles
	def updateProjectiles(self):
		
		# Check if there is a projectile
		for p in self.projectiles:
			
			# Draw the projectile
			pygame.draw.rect(self.screen, self.bg, p.rect)
		
			# Move the projectile
			p.rect.left += p.speed[0]
			p.rect.top += p.speed[1]
			
			# Update gravity
			if p.speed[1] < p.maxSpeed:
				p.speed[1] += p.gravity
		
		# Check for projectile collision
		self.projectileCollisions()
			
	# Function to update the players
	def updatePlayers(self):
		
		# Check pressed keys
		keys = pygame.key.get_pressed()
					
		# Update each player
		for p in self.players:
			
			# Check for key presses and pass in this game object
			p.control(keys, self)
			
			# Remove the player current position d
			pygame.draw.rect(self.screen, self.bg, p.rect)
			
			# Update the player
			p.update()
			
			# Update physics
			self.playerCollision()
			
			# Redraw the player
			self.screen.blit(p.image, p.rect)
			
	# Function to spawn a powerup
	def spawnPowerup(self):
		
		# Choose a random piece of terrain
		t = choice(self.terrain)
		
		# Choose a random powerup and create it
		self.powerups.append(choice(self.possPowerups)(t.bounds.x + randint(-50, 50), t.bounds.y + randint(-50, 50)))
	
	# Function to check for powerup collisions
	def updatePowerups(self):
		
		# Look at each powerup
		for powerup in self.powerups:
				
			# Look at each player
			for player in self.players:
				
				# If the player hits the powerup
				if powerup.rect.colliderect(player.rect):
					
					# Powerup the player
					powerup.power(player)
		
	# Function to check if projectile has collided with any terrain
	def projectileCollisions(self):
		
		# Set px and py to none
		px = None
		py = None
		
		# Iterate over all the terrain
		for t in self.terrain:
			
			# Iterate backwards over the projectiles
			for i in range(len(self.projectiles) - 1, -1, -1):
			
				# If the projectile has collided with the bounding box
				if self.projectiles[i].rect.colliderect(t.bounds):
					
					# Check each of the pixels in the terrain
					for p in t.pixels:
						
						# If the pixel has collided with the projectile
						if self.projectiles[i].rect.colliderect(p):
							
							# Store the pixels location
							px = p.left
							py = p.top
							
							# Break the loop
							break
							
					# Check whether there was a collision between any pixels
					if not px == None:
						
						# Check each pixel to see whether it collided, and if so delete it
						for j in range(len(t.pixels) - 1, -1, -1):
							
							# If the pixel is in range of the blast zone
							if pythagoras(t.pixels[j].left, t.pixels[j].top, px, py) < self.projectiles[i].blastRadius:
								
								# Delete the pixel
								t.pixels.pop(j)
						
						# Redraw this terrain
						pygame.draw.rect(self.screen, self.bg, t.bounds)
						for p in t.pixels:
							pygame.draw.rect(self.screen, (0, 0, 0), p)
						
						# Reduce one from the number of hits left for this projectile
						self.projectiles[i].hits -= 1
						
						# Check if the projectile is a one hit
						if self.projectiles[i].hits == 0:
							self.projectiles.pop(i)
							break
  
	# Function to resolve player collisions
	def playerCollision(self):
		
		# For each player
		for player in self.players:
		
			# Iterate over all the terrain
			for t in self.terrain:
				
				# If the player has collided with the bounding box
				if player.rect.colliderect(t.bounds):
					
					# Set collided to true for this terrain
					collided = False
					
					# Set number of y movements to 0
					dy = 0
					
					# While the player is colliding with a pixel in the current terrain
					while self.pixelCollision(player, t):
						
						# Set collided to true
						collided = True
						
						# Set player to not be jumping
						player.jumping = False
						
						# Move the player up by one pixel
						player.rect.y -= 1
						
						# Add one to the y movement
						dy += 1
						
						# Check if dy is greater than 5
						if dy > 6:
							player.rect.x -= player.direction * player.hzSpeed
							while self.pixelCollision(player, t):
								player.rect.y -= 1
							break
							
					# If collided with this wall, redraw it
					if collided:
						pygame.draw.rect(self.screen, self.bg, t.bounds)
						for p in t.pixels:
							pygame.draw.rect(self.screen, (0, 0, 0), p)
						self.screen.blit(player.image, player.rect)
						
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
	def __init__(self, rect, speed, gravity, maxSpeed, collisionRadius, hits):
		
		# Fields
		self.rect = rect
		self.speed = speed
		self.gravity = gravity
		self.maxSpeed = maxSpeed
		self.blastRadius = collisionRadius
		self.hits = hits
		
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
		
		# Store the number of hits a projectile gets
		self.uses = 1
		
		# Store the number of uses the current powerup gets
		self.powerupUses = 0
		
		# Store the y power of projectiles
		self.projectileY = -3
		
		# An int to stop the bombs from being spamed multiple times
		self.cooldown = 0
		
	# Function to setup key presses
	def setupKeys(self, left, right, up, down):
		
		# Setup fields
		self.left = left
		self.right = right
		self.up = up
		self.down = down
		
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
			
		# Update bomb cooldown
		self.bombCooldown()
	
	# Create a controller for the player
	def control(self, keys, g):
				
		# If left arrow
		if keys[self.left]:
			
			# Set speed to move left
			self.direction = -1
			
		# If right arrow
		elif keys[self.right]:
			
			# Set speed to move right
			self.direction = 1
			
		# Otherwise reset player speed
		else:
			
			# Set speed to 0
			self.direction = 0
			
		# If up arrow
		if keys[self.up]:
			
			# Have to add jump functionality
			self.jump()
			
		# If down arrow
		if keys[self.down]:
			
			# Fire a projectile
			self.fire(g)
		
	# Function to make a player jump
	def jump(self):
		
		# If not already jumping
		if not self.jumping:
			
			# Set jumping to true
			self.jumping = True
		
			# Set the ySpeed to jump speed
			self.speedY = self.jumpSpeed
			
	# Function to fire a projectile
	def fire(self, g):
		
		# Check whether we can fire
		if self.cooldown == 10:
			
			# Create a projectile
			p = Projectile(pygame.Rect(self.rect.x + 3, self.rect.y, 6, 6), [self.direction, self.projectileY], 0.1, 3, self.blastRadius, self.uses)
				
			# Add the projectile to the game
			g.addProjectile(p)
			
			self.cooldown = 0
			
	# Check the cooldown for each player
	def bombCooldown(self):
		
		# Check whether or not we can fire
		if not self.cooldown == 10:
			self.cooldown += 1

# Create the powerup class		
class Powerup(object):
	
	#Constructor
	def __init__(self, image, x, y, blastRadius, uses, colour):
		
		# Store fields
		self.image = pygame.image.load(image)
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.colour = colour
		self.blastRadius = blastRadius
		self.uses = uses
	
	# Draw the powerup on screen
	def draw(self, surface):
		surface.blit(self.image, self.rect)
	
	# Set the position of the powerup
	def setPos(self, x, y):
		self.rect.x = x
		self.rect.y = y
	
	# Activate the powerup for a given player
	def power(self, player):
		player.uses = self.uses
		player.blastRadius = self.blastRadius

# Create a powerup to drill through multiple pieces of terrain
class DrillPowerup(Powerup):
	
	# Call the parent constructor
	def __init__(self, x, y):
		super(DrillPowerup, self).__init__('res/powerUp1.png', x, y, 8, 5, (0, 255, 0))

# Create a powerup to nuke a large portion of the terrain
class NukePowerup(Powerup):
	
	# Call the parent constructor
	def __init__(self, x, y):
		super(NukePowerup, self).__init__('res/powerUp1.png', x, y, 30, 2, (0, 100, 160))
	
# Run an instance of the game
if __name__ == "__main__":
	
	# Create a game object
	g = Game()
	
	# Create a player object
	player = Player(200, 30, 'res/player.png')
	player2 = Player(600, 30, 'res/player2.png')
	player.setupKeys(K_LEFT, K_RIGHT, K_UP, K_DOWN)
	player2.setupKeys(K_a, K_d, K_w, K_s)
	
	# Add the player to the game
	g.addPlayer(player)
	g.addPlayer(player2)
	
	# Read the level data
	g.readFileToTerrain("test.txt")
	
	g.spawnPowerup()
	
	# Draw the map
	g.drawMap()
	
	# Game loop
	while True:
		g.update()
