# 1.6 In this Code Snippet, We will fix the Second problem by addding an offset to the player position when dragging starts.
# We will understand the logic of offset and how it making the player rectangle movement smooth.

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
offset_x = 0


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
