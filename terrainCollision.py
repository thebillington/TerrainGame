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
		if not self.projectile == None:
		
			# Draw the projectile
			pygame.draw.rect(self.screen, (0, 255, 50), self.projectile.rect)
		
		# Update the display
		pygame.display.flip()
		
		# Tick
		self.clock.tick(60)
		
	# Function to update the position of the projectile
	def updateProjectile(self):
		
		# Check if there is a projectile
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
		
		# For each player
		for p in self.players:
			
			# Remove the player current position d
			pygame.draw.rect(self.screen, self.bg, p.rect)
			
			# Update physics
			p.update()
			self.playerCollision()
			
			# Redraw the player
			self.screen.blit(p.image, p.rect)
				
	# Function to check if projectile has collided with any terrain
	def projectileCollision(self):
		
		# Set px and py to none
		px = None
		py = None
		
		# Iterate over all the terrain
		for t in self.terrain:
			
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
					if self.projectile.oneHit:
						self.projectile = None
						break
  
	# Function to resolve player collisions
	def playerCollision(self):
		
		# For each player
		for player in self.players:
		
			# Iterate over all the terrain
			for t in self.terrain:
				
				# If the player has collided with the bounding box
				if player.rect.colliderect(t.bounds):
					
					# While the player is colliding with a pixel in the current terrain
					while self.pixelCollision(player, t):
						
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
	def setProjectile(self, projectile):
		
		# Set projectile
		self.projectile = projectile
        
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
                        t = Terrain(pygame.Rect(int(fields[0]), int(fields[1]), int(fields[2]), int(fields[3])))
	
                        # Add some pixels to the terrain
                        for i in range(int(fields[2])):
                                for j in range(int(fields[3])):
                                        t.addPixel(pygame.Rect(t.bounds.left + i, t.bounds.top + j, 1, 1))

                        #add to the games terrain
                        self.addTerrain(t)
	
				
# Class to hold all the 'pixels' in a piece of terrain
class Terrain(object):
	
	# Constructor
	def __init__(self, locationRect):
		
		# List to hold all of the 'pixels'
		self.pixels = []
		
		# Store a rectangle to be the bounding box of the terrain
		self.bounds = locationRect
		
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
	def __init__(self, x, y, imgRes, gravity, maxSpeed):
		
		# Get the player image from the provided resource
		self.image = pygame.image.load(imgRes)
		self.rect = self.image.get_rect()
		
		# Set the x and y
		self.rect.x = x
		self.rect.y = y
		
		# Set the speed
		self.speedX = 0
		self.speedY = 0
		
		# Set the physics variables
		self.gravity = gravity
		self.maxSpeed = maxSpeed
		
	# Function to move the player
	def move(self, x, y):
		#set the speed of player by specifed x and y values
		self.speedX += x
		self.speedY += y
		
	# Function to update the player
	def update(self):
		
		# Check whether the player needs to accelerate
		if self.speedY < self.maxSpeed:
			
			# Accelerate
			self.speedY += self.gravity
			
		# Move by the speed
		self.rect.x += self.speedX
		self.rect.y += self.speedY
	
	#IM TOO STUPID FOR THIS
	#def dropBomb(self):
	#
	#	if direction == "left":
	#		p = project(pygame.Rect(self.x, self.y, 6, 6), [-3, -7.33], 0.1, 3, 8, True)
	
# Run an instance of the game
if __name__ == "__main__":

	# a boolean for the game loop
	loopBool = True
	
	# Create a game object
	g = Game()
	
	# Create a terrain object
	t = Terrain(pygame.Rect(0, g.height - 4, g.width, 4))
			
	# Create a projectile
	p = Projectile(pygame.Rect(750, 600, 6, 6), [-3, -7.33], 0.1, 3, 8, False)
	
	# Add the projectile to the game
	g.setProjectile(p)
	
	# Create a player object
	player = Player(400, 50, 'res/player.png', 0.1, 6)
	
	# Add the player to the game
	g.addPlayer(player)
	
	# Read the level data
	g.readFileToTerrain("test.txt")
	
	# Draw the map
	g.drawMap()

	# Game loop
	while loopBool == True:
		#uses pygame event library to check for events
		for event in pygame.event.get():
			# if the event is the X in top right being pressed
			if event.type == pygame.QUIT:
				# quit game and exit the game loop
				pygame.quit(); 
				sys.exit()
				loopBool == False
			# if a key has been pressed down
			if event.type == pygame.KEYDOWN:
				#if left arrow
				if event.key == pygame.K_LEFT:
					#move player left
					player.move(-2,0)
				# if right arrow
				if event.key == pygame.K_RIGHT:
					# move player right
					player.move(2,0)
				# if up arrow
				if event.key == pygame.K_UP:
					# have to add jump functionality
					print("jump")
				# if down arrow
				if event.key == pygame.K_DOWN:
					# have to add bomb functionality
					print("Bomb dropped")
			
			# if a key has been released
			if event.type == pygame.KEYUP:
				# if left arrow
				if event.key == pygame.K_LEFT:
					# set the speedX variable back to 0
					player.move(2,0)
				# if the right arrow
				if event.key == pygame.K_RIGHT:
					# set the speedX variable back to 0
					player.move(-2,0)

		g.update()
