# 3.1 In this Code Snippet, We will add coins to the game that fall from the top of the screen.
# Task For you:
# - Create a new list to store coin data.
# - Create a new function to create coins and make it height and width to 20 or any good size.
# - Create a new function to draw coins on the screen.
# - Create a new function to update coins and make them fall down the screen.

import pygame
import random

# Initialize Pygame
pygame.init()

# Game variables
running = True
game_speed = 5  # Speed of the game, controls how fast the obstacle falls
number_of_items = 5 # Number of obstacles
obstacles = []  # List to store obstacle data

# Screen dimensions
WIDTH, HEIGHT = 400, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bubble Dash")

# Colors
PLAYER_COLOR = (0, 0, 255)  # Blue
BACKGROUND_COLOR = (199, 199, 199)
OBSTACLE_COLOR = (255, 0, 0)  # Red for obstacles

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

def create_obstacle():
    """Creates a new obstacle with random width and adds it to the list."""
    obstacle_width = random.randint(20, 80)
    obstacle_height = 30
    x = random.randint(0, WIDTH - obstacle_width)
    y = obstacle_height

    obstacles.append({"x": x, "y": y, "width": obstacle_width, "height": obstacle_height})

def update_obstacles():
    """Moves obstacles downward and removes them when they leave the screen."""
    for obstacle in obstacles:
        obstacle["y"] += game_speed
        if obstacle["y"] > HEIGHT:
            obstacles.remove(obstacle)

def draw_obstacles():
    """Draws all obstacles on the screen."""
    for obstacle in obstacles:
        pygame.draw.rect(screen, OBSTACLE_COLOR, (obstacle["x"], obstacle["y"], obstacle["width"], obstacle["height"]))

def check_collisions():
    global running
    """Checks for collisions between the player and obstacles."""
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)

    # Check collision with obstacles
    for obstacle in obstacles:
        obstacle_rect = pygame.Rect(obstacle['x'], obstacle['y'], obstacle['width'], obstacle["height"])
        if player_rect.colliderect(obstacle_rect):
            print("Collision detected! Game Over.")
            running = False  # End the game on collision

# Clock for FPS control
clock = pygame.time.Clock()

while running:
    screen.fill(BACKGROUND_COLOR)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    handle_player_movement(event)

    # Create a new obstacle at random intervals
    if len(obstacles) < number_of_items and random.randint(1, 50) == 1:  # Random chance to create an obstacle
        create_obstacle()

    # Move the obstacles down the screen
    update_obstacles()

    # Draw all obstacles
    draw_obstacles()

    # Check for collisions
    check_collisions()

    # Drawing a Rectangle (player)
    pygame.draw.rect(screen, PLAYER_COLOR, (player_x, player_y, player_width, player_height))

    pygame.display.flip()  # Update display
    clock.tick(60)  # Limit FPS to 60

pygame.quit()