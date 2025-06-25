# 2.2 In this Code Snippet, we will make the obstacle fall down the screen.


import pygame
import random

# Initialize Pygame
pygame.init()


# Game variables
running = True
game_speed = 5  # Speed of the game, controls how fast the obstacle falls

# Screen dimensions
WIDTH, HEIGHT = 400, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bubble Dash")

# Colors
PLAYER_COLOR = (0, 0, 255)  # Blue
BACKGROUND_COLOR = (199, 199, 199)

# Player properties
player_width, player_height = 35, 55
player_x = (WIDTH - player_width) // 2
player_y = (HEIGHT - player_height) // 1.5
dragging = False
offset_x = 0

obstacle = {}

def handle_player_movement(event):
    """Handles mouse dragging to move the player left/right."""
    global player_x, dragging, offset_x

    if event.type == pygame.MOUSEBUTTONDOWN:
        dragging = True
        offset_x = event.pos[0] - player_x

    elif event.type == pygame.MOUSEBUTTONUP:
        dragging = False

    elif event.type == pygame.MOUSEMOTION and dragging:
        player_x = event.pos[0] - offset_x  # Move player left/right

    # Keep player within screen bounds
    player_x = max(0, min(WIDTH - player_width, player_x))

def create_obstacle():
    global obstacle
    """Creates a new obstacle with random width and adds it to the list."""
    obstacle_width = random.randint(20, 80)
    obstacle_height = 30
    x = random.randint(0, WIDTH - obstacle_width)
    y = obstacle_height

    obstacle = {"x": x, "y": y, "width": obstacle_width, "height": obstacle_height}

create_obstacle() 

# Clock for FPS control
clock = pygame.time.Clock()

while running:
    screen.fill(BACKGROUND_COLOR)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        handle_player_movement(event)

    # Move the obstacle down the screen
    obstacle["y"] += game_speed

    # draw the obstacle
    pygame.draw.rect(screen, (255, 0, 0), (obstacle["x"], obstacle["y"], obstacle["width"], obstacle["height"]))

    # Drawing a Rectangle (player)
    pygame.draw.rect(screen, PLAYER_COLOR, (player_x, player_y, player_width, player_height))

    pygame.display.flip()  # Update display
    clock.tick(60)  # Limit FPS to 60

pygame.quit()

# This code has one obstacle that falls down the screen.
# When it goes off the bottom, it doesn't come back or make new ones.
# In the next part (2.3), we'll make lots of obstacles that keep coming!