import pygame
import sys
import random
import os

# Constants
TILE_SIZE = 30
GRID_SIZE = 40
WIDTH = HEIGHT = TILE_SIZE * GRID_SIZE
FPS = 10

# Colors
BLUE = (0, 0, 255)
GREEN = (144, 238, 144)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (200, 200, 200)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont('Arial', 24)
big_font = pygame.font.SysFont('Arial', 48)

snake_img = pygame.Surface((TILE_SIZE, TILE_SIZE))
snake_img.fill(BLUE)

# Automatically get current script folder
game_folder = os.path.dirname(os.path.abspath(__file__))

# Full path to banana and apple
banana_path = os.path.join(game_folder, "banana.png")
apple_path = os.path.join(game_folder, "apple.png")

banana_img = pygame.image.load(banana_path).convert_alpha()
apple_img = pygame.image.load(apple_path).convert_alpha()
def draw_score(score):
    text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(text, (10, 10))

def random_position(snake):
    while True:
        max_x = screen.get_width() // TILE_SIZE
        max_y = screen.get_height() // TILE_SIZE
        pos = (random.randint(0, max_x - 1), random.randint(0, max_y - 1))
        if pos not in snake:
            return pos

def reset_game():
    snake = [(5, 5), (4, 5), (3, 5), (2, 5)]
    direction = (1, 0)
    banana = random_position(snake)
    apple = None
    score = 0
    bananas_eaten = 0  # 🍌 <-- NEW LINE
    return snake, direction, banana, apple, score, bananas_eaten

def show_game_over():
    screen.fill(GREEN)

    # Title text
    current_w = screen.get_width()
    current_h = screen.get_height()

    game_over_text = big_font.render("GAME OVER", True, RED)
    text_rect = game_over_text.get_rect(center=(current_w // 2, current_h // 2 - 100))
    screen.blit(game_over_text, text_rect)

    # Define buttons as rectangles
    restart_button = pygame.Rect(current_w // 2 - 100, current_h // 2 - 30, 200, 50)
    quit_button = pygame.Rect(current_w // 2 - 100, current_h // 2 + 40, 200, 50)

    # Draw buttons
    pygame.draw.rect(screen, GRAY, restart_button)
    pygame.draw.rect(screen, GRAY, quit_button)

    # Button texts
    restart_text = font.render("Restart", True, BLACK)
    quit_text = font.render("Quit", True, BLACK)
    screen.blit(restart_text, (restart_button.x + 60, restart_button.y + 12))
    screen.blit(quit_text, (quit_button.x + 75, quit_button.y + 12))

    pygame.display.flip()

    # Button event loop
    while True:
        for event in pygame.event.get():       
            if event.type == pygame.QUIT:
                return 'quit'
            
           
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                print("Mouse clicked at:", mouse_pos)  # 👈 Add this line

                if restart_button.collidepoint(mouse_pos):
                    print("Restart button clicked")  # 👈 Debug print
                    return 'restart'
                elif quit_button.collidepoint(mouse_pos):
                    print("Quit button clicked")  # 👈 Debug print
                    return 'quit'

snake, direction, banana, apple, score, bananas_eaten = reset_game()
action = None  # to keep track of restart or quit action

swipe_start = None  # 👆 Finger swipe start position

while True:
    for event in pygame.event.get():
                # 👆 Swipe gesture control for Android
        if event.type == pygame.MOUSEBUTTONDOWN:
            swipe_start = pygame.mouse.get_pos()

        elif event.type == pygame.MOUSEBUTTONUP and swipe_start:
            swipe_end = pygame.mouse.get_pos()
            dx = swipe_end[0] - swipe_start[0]
            dy = swipe_end[1] - swipe_start[1]

            if abs(dx) > abs(dy):  # Horizontal swipe
                if dx > 0 and direction != (-1, 0):
                    direction = (1, 0)
                elif dx < 0 and direction != (1, 0):
                    direction = (-1, 0)
            else:  # Vertical swipe
                if dy > 0 and direction != (0, -1):
                    direction = (0, 1)
                elif dy < 0 and direction != (0, 1):
                    direction = (0, -1)

            swipe_start = None
            
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

  
    head = (snake[0][0] + direction[0], snake[0][1] + direction[1])

    # Game Over conditions
    max_x = screen.get_width() // TILE_SIZE
    max_y = screen.get_height() // TILE_SIZE
    if head in snake or not (0 <= head[0] < max_x and 0 <= head[1] < max_y):
        action = show_game_over()

        if action == 'restart':
            snake, direction, banana, apple, score, bananas_eaten = reset_game()
            continue
        elif action == 'quit':
            pygame.quit()
            sys.exit()

    # Move snake
    snake = [head] + snake[:-1]

    # Eat banana
    if head == banana:
        score += 3
        bananas_eaten +=1 # 🍌 Count how many bananas were eaten
        banana = random_position(snake)

        # Every 3 bananas, drop an apple
        if bananas_eaten % 6 == 0 and not apple:
            apple = random_position(snake)

    # Eat apple
    elif apple and head == apple:
        score += 5
        apple = None

    screen.fill(GREEN)
    draw_score(score)

    for pos in snake:
        screen.blit(snake_img, (pos[0] * TILE_SIZE, pos[1] * TILE_SIZE))

    # Draw banana centered
    banana_rect = banana_img.get_rect(center=(
        banana[0] * TILE_SIZE + TILE_SIZE // 2,
        banana[1] * TILE_SIZE + TILE_SIZE // 2))
    screen.blit(banana_img, banana_rect)

    # Draw apple centered
    if apple:
        apple_rect = apple_img.get_rect(center=(
            apple[0] * TILE_SIZE + TILE_SIZE // 2,
            apple[1] * TILE_SIZE + TILE_SIZE // 2))
        screen.blit(apple_img, apple_rect)

    pygame.display.flip()
    clock.tick(FPS)
    current_width, current_height = screen.get_size()
    visible_grid_width = current_width // TILE_SIZE
    visible_grid_height = current_height // TILE_SIZE
