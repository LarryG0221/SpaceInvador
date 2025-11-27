import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Space Invader")

# Load background image
# background = pygame.Surface(screen.get_size())
background = pygame.image.load("bg.png")

# Game loop

while True:
    # Draw background
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
            
    # Update display
    pygame.display.update()

