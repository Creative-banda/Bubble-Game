# 1.5 In this Code Snippet, We will fix the first problem by adding boundaries to the player rectangle movement.
# We will understand min() and max() functions to limit the player rectangle movement within the screen boundaries.

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
BACKGROUND_COLOR = (199, 199, 199)

# Player properties
player_width, player_height = 35, 55
player_x = (WIDTH - player_width) // 2
player_y = (HEIGHT - player_height) // 1.5
dragging = False


def handle_player_movement(event):
    """Handles mouse dragging to move the player left/right."""
    global player_x, dragging

    if event.type == pygame.MOUSEBUTTONDOWN:
        dragging = True

    elif event.type == pygame.MOUSEBUTTONUP:
        dragging = False

    elif event.type == pygame.MOUSEMOTION and dragging:
        player_x = event.pos[0]

    # Keep player within screen bounds
    player_x = max(0, min(WIDTH - player_width, player_x))

# Clock for FPS control
clock = pygame.time.Clock()

while running:

    screen.fill(BACKGROUND_COLOR)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        handle_player_movement(event)

    # Drawing a Rectangle (player)
    pygame.draw.rect(screen, PLAYER_COLOR, (player_x, player_y, player_width, player_height))

    pygame.display.flip()  # Update display
    clock.tick(60)  # Limit FPS to 60

pygame.quit()

# Note:
# - We will fix the first problem by adding boundaries to the player rectangle movement.
# - We still have the problem that the player suddenly jumps to the mouse position.