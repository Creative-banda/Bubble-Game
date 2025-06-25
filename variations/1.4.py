# 1.4 In this Code Snippet, We will add movement to the player rectangle.
# We will use the mouse dragging to move the player

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
# - Currently we have 2 Problems:
#   1. The player rectangle can go out of the screen.
#   2. As we drag the mouse, the player suddenly jumps to the mouse position.
# - We will fix these problems in the next snippets.