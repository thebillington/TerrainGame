# Get imports
import pygame
from pygame.locals import *

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
		
	# Function to update the game
	def update(self):
		
		# Check for exit
		self.exit()
		
		# Clear the screen
		self.screen.fill(self.bg)
		
		# Draw all terrain
		self.drawTerrain()
		
		# Update the display
		pygame.display.flip()
		
		# Tick
		self.clock.tick(60)
		
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
        
	# Function to check for user closing the window
	def exit(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				
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
	
	# Add the terrain to the game
	g.addTerrain(t)
	
	# Game loop
	while True:
		g.update()
