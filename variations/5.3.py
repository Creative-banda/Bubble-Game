# 5.3 In this code, We will detect the player click on Play button and start the game.

import pygame
import random

# Initialize Pygame
pygame.init()

# Game variables
running = True
game_speed = 5  # Speed of the game, controls how fast the obstacle falls
number_of_items = 5 # Number of obstacles
obstacles = []  # List to store obstacle data
coins = []  # List to store coin data
last_update_time = pygame.time.get_ticks()  # Track time for speed increase
isAlive = False # Variable to check if the player is alive

# Screen dimensions
WIDTH, HEIGHT = 400, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bubble Dash")

# Colors
PLAYER_COLOR = (0, 0, 255)  # Blue
BACKGROUND_COLOR = (199, 199, 199)
OBSTACLE_COLOR = (255, 0, 0)  # Red for obstacles
COIN_COLOR = (255, 215, 0)  # Gold for coins

# Score variables
score = 0
highscore = 0

# Player properties
player_width, player_height = 35, 55
player_x = (WIDTH - player_width) // 2
player_y = (HEIGHT - player_height) // 1.5
dragging = False
offset_x = 0

# Images
player_img = pygame.image.load("assets/player.PNG")
player_img = pygame.transform.scale(player_img, (player_width, player_height))
obstacle_img = pygame.image.load("assets/obs_1.PNG")
coin_img = pygame.image.load("assets/coin.PNG")


# Load sound effects
background_music = pygame.mixer.Sound("assets/background.mp3")
coin_collect = pygame.mixer.Sound("assets/coin_collect.mp3")


# Clock for FPS control
clock = pygame.time.Clock()

# Font for text
font = pygame.font.Font(None, 30)
title_font = pygame.font.Font(None, 80)

# ============================== PLAYER HANDLING ============================== #

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

# ============================== OBSTACLE HANDLING ============================== #

def create_obstacle():
    """Creates a new obstacle with random width and adds it to the list."""
    obstacle_width = random.randint(20, 80)
    obstacle_height = 30
    x = random.randint(0, WIDTH - obstacle_width)
    y = -obstacle_height
    img = pygame.transform.scale(obstacle_img, (obstacle_width, obstacle_height))

    obstacles.append({"x": x, "y": y, "img": img, "width": obstacle_width, "height": obstacle_height})

def update_obstacles():
    """Moves obstacles downward and removes them when they leave the screen."""
    for obstacle in obstacles:
        obstacle["y"] += game_speed
        if obstacle["y"] > HEIGHT:
            obstacles.remove(obstacle)

def draw_obstacles():
    """Draws all obstacles on the screen."""
    for obstacle in obstacles:
        screen.blit(obstacle["img"], (obstacle["x"], obstacle["y"]))

# ============================== COIN HANDLING ============================== #

def spawn_coin():
    """Creates a new coin at a random position and adds it to the list."""
    coin_width = 20
    coin_height = 20
    x = random.randint(0, WIDTH - coin_width)
    y = -coin_height
    img = pygame.transform.scale(coin_img, (coin_width, coin_height))

    coins.append({"x": x, "y": y, "img": img, "width": coin_width, "height": coin_height})

def update_coins():
    """Moves coins downward and removes them when they leave the screen."""
    for coin in coins:
        coin["y"] += game_speed
        if coin["y"] > HEIGHT:
            coins.remove(coin)

def draw_coins():
    """Draws all coins on the screen."""
    for coin in coins:
        screen.blit(coin["img"], (coin["x"], coin["y"]))


# ============================== COLLISION DETECTION ============================== #

def check_collisions():
    global running, coins, score, isAlive, highscore
    """Checks for collisions between the player and obstacles."""
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)

    # Check collision with obstacles
    for obstacle in obstacles:
        obstacle_rect = pygame.Rect(obstacle['x'], obstacle['y'], obstacle['width'], obstacle["height"])
        if player_rect.colliderect(obstacle_rect):
            print("Collision detected! Game Over.")
            isAlive = False  # Make the player not alive

    # Check collision with coins
    for coin in coins:
        coin_rect = pygame.Rect(coin['x'], coin['y'], coin['width'], coin["height"])
        if player_rect.colliderect(coin_rect):
            coins.remove(coin)
            score += 10
            coin_collect.play()  # Play coin collect sound effect

# ============================== DRAW PANEL / INCREASE SPEED ============================== #

def draw_panel():
    """Draws the score and highscore panel on the screen."""
    panel_height = 50
    panel_color = (50, 50, 50)
    text_color = (255, 255, 255)

    # Draw panel background
    pygame.draw.rect(screen, panel_color, (0, 0, WIDTH, panel_height))

    # Render score text
    score_text = font.render(f"Score: {score}", True, text_color)
    screen.blit(score_text, (10, 10))

    # Render highscore text
    highscore_text = font.render(f"Highscore: {highscore}", True, text_color)
    screen.blit(highscore_text, (WIDTH - highscore_text.get_width() - 10, 10))

def increase_difficulty():
    """Increases the game speed over time."""
    global game_speed, last_update_time, number_of_items

    current_time = pygame.time.get_ticks()
    if current_time - last_update_time > 7000:  # Increase speed every 7 seconds
        game_speed += 1
        number_of_items += 1
        last_update_time = current_time

def draw_button(rect, text, color):
    pygame.draw.rect(screen, color, rect, border_radius=20)
    txt_surface = font.render(text, True, (255, 255, 255))
    screen.blit(txt_surface, (
        rect.centerx - txt_surface.get_width() // 2,
        rect.centery - txt_surface.get_height() // 2
    ))

def display_start_screen():
    global high_score

    screen.fill((30, 30, 30))
    # Title text
    title_text = title_font.render("Bubble Dash", True, (255, 255, 255))
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))
    
    play_button = pygame.Rect(WIDTH // 2 - 75, HEIGHT // 2 - 50, 150, 50)

    draw_button(play_button, "Play", (0, 200, 0))

    high_text = font.render(f"Highscore: {high_score}", True, (255, 255, 255))
    screen.blit(high_text, (WIDTH // 2 - high_text.get_width() // 2, HEIGHT // 2 + 100))


background_music.play(-1)  # Play background music in a loop

# ============================== HIGH SCORE HANDLING ============================== #

def get_highscore():
    """Returns the highscore from the file."""
    try:
        with open("highscore.txt", "r") as file:
            return int(file.read())
    except FileNotFoundError:
        return 0

def save_highscore():
    """Saves the highscore to a file."""
    with open("highscore.txt", "w") as file:
        file.write(str(score))

# ============================== MAIN GAME LOOP ============================== #

high_score = get_highscore()

while running:
    screen.fill(BACKGROUND_COLOR) # Clear the screen

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        handle_player_movement(event)

    # Display Play button if player is not alive
    if not isAlive:
        display_start_screen()
    else:
        # Spawn obstacles randomly
        if random.randint(1, 50) == 1 and len(obstacles) < number_of_items:
            create_obstacle()

        # Spawn coins randomly
        if random.randint(1, 50) == 1 and len(coins) < number_of_items:
            spawn_coin()

        # Update and draw obstacles
        update_obstacles()
        draw_obstacles()

        # Update and draw coins
        update_coins()
        draw_coins()

        # Check for collisions
        check_collisions()

        # Drawing a Rectangle (player)
        screen.blit(player_img, (player_x, player_y))

        # Draw the PANEL
        draw_panel()

    pygame.display.flip()  # Update display
    clock.tick(60)  # Limit FPS to 60

pygame.quit()