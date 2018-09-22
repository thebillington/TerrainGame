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
		
		# Create a list to store all of the projectiles
		self.projectile = None
		
	# Function to update the game
	def update(self):
		
		# Check for exit
		self.exit()
		
		# Update the proejectile
		self.updateProjectile()
		
		# Clear the screen
		self.screen.fill(self.bg)
		
		# Check that there is a projectile to draw
		if not self.projectile == None:
		
			# Draw the projectile
			pygame.draw.rect(self.screen, (0, 255, 50), self.projectile.rect)
		
		# Draw all terrain
		self.drawTerrain()
		
		# Update the display
		pygame.display.flip()
		
		# Tick
		self.clock.tick(60)
		
	# Function to update the position of the projectile
	def updateProjectile(self):
		
		# Check if there is a projectile
		if not self.projectile == None:
		
			# Move the projectile
			self.projectile.rect.left += self.projectile.speed[0]
			self.projectile.rect.top += self.projectile.speed[1]
			
			# Update gravity
			if self.projectile.speed[1] < self.projectile.maxSpeed:
				self.projectile.speed[1] += self.projectile.gravity
		
			# Check for projectile collision
			self.projectileCollision()
				
	# Function to check if projectile has collided with any terrain
	def projectileCollision(self):
		
		# Set px and py to none
		px = None
		py = None
		
		# Iterate over all the terrain
		for t in self.terrain:
			
			# If the projectile has collided with the bounding box
			if self.projectile.rect.colliderect(t.bounds):
				
				print("Bounding box collision...")
				
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
					
					# Check if the projectile is a one hit
					if self.projectile.oneHit:
						self.projectile = None
		
	# Function to draw the terrain
	def drawTerrain(self):
		
		# Iterate over all the terrain
		for t in self.terrain:
			
			# Draw the bounding box
			pygame.draw.rect(self.screen, (255, 0, 0), t.bounds, 1)
			
			# For each pixel in the terrain
			for p in t.pixels:
				
				# Light the pixel
				pygame.draw.rect(self.screen, (0, 0, 0), p)
		
	# Create a function to add terrain
	def addTerrain(self, terrain):
		
		# Add the terrain
		self.terrain.append(terrain)
		
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
				
# Run an instance of the game
if __name__ == "__main__":
	
	# Create a game object
	g = Game()
	
	# Create a terrain object
	t = Terrain(pygame.Rect(200, 200, 100, 50))
	
	# Add some pixels to the terrain
	for i in range(20, 80):
		for j in range(10, 40):
			t.addPixel(pygame.Rect(t.bounds.left + i, t.bounds.top + j, 1, 1))
			
	# Create a projectile
	p = Projectile(pygame.Rect(500, 500, 6, 6), [-3, -7], 0.1, 3, 5, True)
	
	# Add the projectile to the game
	g.setProjectile(p)
	
	# Add the terrain to the game
	g.addTerrain(t)
	
	# Game loop
	while True:
		g.update()
