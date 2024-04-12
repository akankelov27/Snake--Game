import pygame
import sys
import random
import time

# Initialize Pygame
pygame.init()

# Window size
frame_size_x = 720
frame_size_y = 480
game_window = pygame.display.set_mode((frame_size_x, frame_size_y))
pygame.display.set_caption('Snake Game')

# Colors
colors = {
    'black': pygame.Color(0, 0, 0),
    'white': pygame.Color(255, 255, 255),
    'green': pygame.Color(0, 255, 0),
    'blue': pygame.Color(0, 0, 255),
    'orange': pygame.Color(255, 165, 0),
    'brown': pygame.Color(165, 42, 42),
    'red': pygame.Color(255, 0, 0)
}

# Difficulty settings
difficulties = {
    'green': 10,
    'blue': 20,
    'orange': 30,
    'brown': 40,
    'red': 50
}

# FPS controller
fps_controller = pygame.time.Clock()  # Ensure this is correctly defined

# Game fonts
font = pygame.font.SysFont('Arial', 25)

# Score function
def show_score(color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score : ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    score_rect.midtop = (frame_size_x / 10, 15)
    game_window.blit(score_surface, score_rect)

# Game over function
def game_over():
    my_font = pygame.font.SysFont('Arian', 50)
    game_over_surface = my_font.render('Your Score is ' + str(score), True, colors['red'])
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (frame_size_x / 2, frame_size_y / 4)
    game_window.fill(colors['black'])
    game_window.blit(game_over_surface, game_over_rect)
    show_score(colors['red'], 'times', 20)
    pygame.display.flip()

    # Restart mechanism
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    main()

# Main logic of the snake game
def main():
    global score
    snake_color, snake_speed = choose_difficulty()
    snake_pos = [100, 50]
    snake_body = [[100, 50], [90, 50], [80, 50]]
    direction = 'RIGHT'
    change_to = direction
    food_pos = [random.randrange(1, (frame_size_x // 10)) * 10, random.randrange(1, (frame_size_y // 10)) * 10]
    food_spawn = True
    score = 0

    while True:
        for event in pygame.event.get():
            if event.type is pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != 'DOWN':
                    change_to = 'UP'
                elif event.key == pygame.K_DOWN and direction != 'UP':
                    change_to = 'DOWN'
                elif event.key == pygame.K_LEFT and direction != 'RIGHT':
                    change_to = 'LEFT'
                elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                    change_to = 'RIGHT'

        # Validating direction change
        if change_to == 'UP' and direction != 'DOWN':
            direction = 'UP'
        elif change_to == 'DOWN' and direction != 'UP':
            direction = 'DOWN'
        elif change_to == 'LEFT' and direction != 'RIGHT':
            direction = 'LEFT'
        elif change_to == 'RIGHT' and direction != 'LEFT':
            direction = 'RIGHT'

        # Moving the snake
        if direction == 'UP':
            snake_pos[1] -= 10
        elif direction == 'DOWN':
            snake_pos[1] += 10
        elif direction == 'LEFT':
            snake_pos[0] -= 10
        elif direction == 'RIGHT':
            snake_pos[0] += 10

        # Snake body mechanism
        snake_body.insert(0, list(snake_pos))
        if snake_pos == food_pos:
            score += 1
            food_spawn = False
        else:
            snake_body.pop()

        # Food spawn
        if not food_spawn:
            food_pos = [random.randrange(1, (frame_size_x // 10)) * 10, random.randrange(1, (frame_size_y // 10)) * 10]
            food_spawn = True

        # GFX
        game_window.fill(colors['black'])
        for pos in snake_body:
            pygame.draw.rect(game_window, snake_color, pygame.Rect(pos[0], pos[1], 10, 10))
        pygame.draw.rect(game_window, colors['white'], pygame.Rect(food_pos[0], food_pos[1], 10, 10))

        # Game Over conditions
        if snake_pos[0] < 0 or snake_pos[0] > frame_size_x - 10 or snake_pos[1] < 0 or snake_pos[1] > frame_size_y - 10:
            game_over()
        for block in snake_body[1:]:
            if snake_pos == block:
                game_over()

        show_score(colors['white'], 'arial', 25)
        pygame.display.update()
        fps_controller.tick(snake_speed)

# Choose difficulty
def choose_difficulty():
    custom_font = pygame.font.SysFont('comic sans ms', 25, bold=True)
    running = True
    while running:
        game_window.fill(colors['black'])
        draw_text('Choose difficulty by pressing the number:', custom_font, colors['white'], game_window, 10, 15)
# Define a new font, maybe larger and bold
        custom_font = pygame.font.SysFont('comic sans ms', 30, bold=True)

# Usage in your existing function calls
        draw_text('1 - Easy (Green)', custom_font, colors['green'], game_window, 20, 100)
        draw_text('2 - Medium (Blue)', custom_font, colors['blue'], game_window, 20, 140)
        draw_text('3 - Hard (Orange)', custom_font, colors['orange'], game_window, 20, 180)
        draw_text('4 - Harder (Brown)', custom_font, colors['brown'], game_window, 20, 220)
        draw_text('5 - Impossible (Red)', custom_font, colors['red'], game_window, 20, 260)
        pygame.display.update()


        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return colors['green'], difficulties['green']
                elif event.key == pygame.K_2:
                    return colors['blue'], difficulties['blue']
                elif event.key == pygame.K_3:
                    return colors['orange'], difficulties['orange']
                elif event.key == pygame.K_4:
                    return colors['brown'], difficulties['brown']
                elif event.key == pygame.K_5:
                    return colors['red'], difficulties['red']

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

if __name__ == "__main__":
    main()
