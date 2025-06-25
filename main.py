import pygame
import random

# ============================== CONSTANTS & INITIALIZATION ============================== #

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 400, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bubble Dash")

# Colors
WHITE = (199, 199, 199)
PLAYER_COLOR = (0, 0, 255)  # Blue
OBSTACLE_COLOR = (255, 0, 0)  # Red
COIN_COLOR = (255, 215, 0)  # Gold
BACKGROUND_COLOR = (199, 199, 199)

# Game variables
game_speed = 3
score = 0
running = True
number_of_items = 5 # Number of obstacles/coins on the screen at a time

# Sound Effects
background_music = pygame.mixer.Sound("assets/background.mp3")
background_music.set_volume(0.2)
coin_collect = pygame.mixer.Sound("assets/coin_collect.mp3")
game_over = pygame.mixer.Sound("assets/game_over.mp3")

# Clock for FPS control
clock = pygame.time.Clock()

# Font for text
font = pygame.font.Font(None, 30)
title_font = pygame.font.Font(None, 80)

# ============================== PLAYER HANDLING ============================== #

# Player properties
player_width, player_height = 35, 55
player_x = (WIDTH - player_width) // 2
player_y = (HEIGHT - player_width) // 1.5 
dragging = False
offset_x = 0
last_update_time = pygame.time.get_ticks()
isAlive = False
high_score = 0

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

obstacles = []

def spawn_obstacle():
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

# ============================== COIN HANDLING ============================== #

coins = []

def spawn_coin():
    """Creates a new coin at a random position and adds it to the list."""
    coin_width = 20
    coin_height = 20
    x = random.randint(0, WIDTH - coin_width)
    y = -coin_height

    coins.append({"x": x, "y": y, "width": coin_width, "height": coin_height})

def update_coins():
    """Moves coins downward and removes them when they leave the screen."""
    for coin in coins:
        coin["y"] += game_speed
        if coin["y"] > HEIGHT:
            coins.remove(coin)

def draw_coins():
    """Draws all coins on the screen."""
    for coin in coins:
        pygame.draw.rect(screen, COIN_COLOR, (coin["x"], coin["y"], coin["width"], coin["height"]))

# ============================== COLLISION DETECTION ============================== #

def check_collisions():
    """Checks for collisions between the player and obstacles/coins."""
    global running, score, isAlive, high_score

    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)

    # Check collision with obstacles
    for obstacle in obstacles:
        obstacle_rect = pygame.Rect(obstacle['x'], obstacle['y'], obstacle['width'], obstacle["height"])
        if player_rect.colliderect(obstacle_rect):
            isAlive = False
            background_music.stop()  # Stop background music
            game_over.play()
            # Update highscore
            if score > high_score:
                save_highscore()
            break

    # Check collision with coins
    for coin in coins:
        coin_rect = pygame.Rect(coin['x'], coin['y'], coin['width'], coin["height"])
        if player_rect.colliderect(coin_rect):
            coins.remove(coin)
            score += 10
            coin_collect.play()

# ============================== DRAW PANEL / UI AND INCREASE SPEED ============================== #

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
    highscore_text = font.render(f"Highscore: {high_score}", True, text_color)
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
    global isAlive, score, game_speed, obstacles, coins, player_x, player_y, last_update_time, running, high_score

    screen.fill((30, 30, 30))
    # Title text
    title_text = title_font.render("Bubble Dash", True, (255, 255, 255))
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))
    
    play_button = pygame.Rect(WIDTH // 2 - 75, HEIGHT // 2 - 50, 150, 50)
    quit_button = pygame.Rect(WIDTH // 2 - 75, HEIGHT // 2 + 20, 150, 50)

    draw_button(play_button, "Play", (0, 200, 0))
    draw_button(quit_button, "Quit", (200, 0, 0))

    high_score = get_highscore()
    high_text = font.render(f"Highscore: {high_score}", True, (255, 255, 255))
    screen.blit(high_text, (WIDTH // 2 - high_text.get_width() // 2, HEIGHT // 2 + 100))

    mouse_pos, click = pygame.mouse.get_pos(), pygame.mouse.get_pressed()
    if click[0]:  # Left click
        if play_button.collidepoint(mouse_pos):
            isAlive, score, game_speed = True, 0, 3
            obstacles.clear(), coins.clear()
            player_x = (WIDTH - player_width) // 2
            player_y = (HEIGHT - player_width) // 1.5
            last_update_time = pygame.time.get_ticks()
            background_music.play(-1)
        elif quit_button.collidepoint(mouse_pos):
            running = False
            
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

while running:
    screen.fill(BACKGROUND_COLOR)  # Clear screen
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if score > high_score:
                save_highscore()
            running = False
        handle_player_movement(event)
    
    # Display Play button if player is not alive
    if not isAlive:
        display_start_screen()
    else:
        # Spawn obstacles randomly
        if random.randint(1, 50) == 1 and len(obstacles) < number_of_items:
            spawn_obstacle()

        # Spawn coins randomly
        if random.randint(1, 50) == 1 and len(coins) < number_of_items:
            spawn_coin()

        # Update and draw everything
        update_obstacles()
        update_coins()
        check_collisions()

        draw_obstacles()
        draw_coins()

        # Draw player
        pygame.draw.rect(screen, PLAYER_COLOR, (player_x, player_y, player_width, player_height))

        draw_panel()  # Draw score panel
        increase_difficulty()  # Increase game speed

    pygame.display.flip()  # Update display
    clock.tick(60)  # Limit FPS

pygame.quit()
