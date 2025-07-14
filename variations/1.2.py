# 1.2 In this Code Snippet, We will Create a Rectangle in the window.

import pygame

# Initialize Pygame
pygame.init()

# Game variables
running = True

# Screen dimensions
WIDTH, HEIGHT = 400, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bubble Dash")

# Clock for FPS control
clock = pygame.time.Clock()


while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Drawing a Rectangle (player)
    pygame.draw.rect(screen, (0, 255, 0), (WIDTH // 2, HEIGHT - 200, 50, 70))

    pygame.display.flip()  # Update display
    clock.tick(60)  # Limit FPS to 60

pygame.quit()


# For Creating Rectangle you have to use pygame.draw.rect(screen, color, (x, y, width, height))
# pygame.draw.rect() function parameters:
# - screen: The surface on which to draw the rectangle.
# - color: Color of the rectangle in RGB format
# - (x, y): x and y position of the rectangle
# - width and height: Width and height of the rectangle