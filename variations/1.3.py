# 1.3 Introduce the Player Rectangle properties
# We will use constance variables to define the player rectangle properties such as width, height, color, and position.
# This will help us to easily modify the player in the future.

import pygame

# Initialize Pygame
pygame.init()

# Game variables
running = True

# Screen dimensions
WIDTH, HEIGHT = 400, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bubble Dash")

# Colors
PLAYER_COLOR = (0, 0, 255)  # Blue

# Player properties
player_width, player_height = 35, 55
player_x = (WIDTH - player_width) // 2
player_y = (HEIGHT - player_height) // 1.5

# Clock for FPS control
clock = pygame.time.Clock()

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Drawing a Rectangle (player)
    pygame.draw.rect(screen, PLAYER_COLOR, (player_x, player_y, player_width, player_height)) 

    pygame.display.flip()  # Update display
    clock.tick(60)  # Limit FPS to 60

pygame.quit()
