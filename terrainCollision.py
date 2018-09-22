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
		
	# Function to update the game
	def update(self):
		
		# Check for exit
		self.exit()
		
		# Clear the screen
		self.screen.fill(self.bg)
		
		# Update the display
		pygame.display.flip()
		
		# Tick
		self.clock.tick(60)
        
	# Function to check for user closing the window
	def exit(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				
# Run an instance of the game
if __name__ == "__main__":
	
	# Create a game object
	g = Game()
	
	# Game loop
	while True:
		g.update()
