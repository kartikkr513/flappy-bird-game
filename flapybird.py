import pygame as pg
import sys
import random

pg.init()

# DISPLAY
WIDTH = 400
HEIGHT = 600
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Flappy Bird")

# COLORS
WHITE = (255, 255, 255)

# CLOCK
clock = pg.time.Clock()

# BIRD
bird = pg.Surface((30, 30))
bird.fill((255, 255, 0))
bird_rect = bird.get_rect(center=(100, HEIGHT//2))
bird_movement = 0
gravity = 0.5

# PIPES
pipe_list = []
PIPE_HEIGHT = [200, 300, 400]
pipe_surface = pg.Surface((60, 400))
pipe_surface.fill((0, 255, 0))

# SCORE
score = 0
font = pg.font.Font(None, 40)

# FUNCTIONS

def draw_pipes(pipes):
    for pipe in pipes:
        pg.draw.rect(screen, (0,255,0), pipe)

def create_pipe():
    random_height = random.choice(PIPE_HEIGHT)
    bottom_pipe = pg.Rect(WIDTH, random_height, 60, 400)
    top_pipe = pg.Rect(WIDTH, random_height - 550, 60, 400)
    return bottom_pipe, top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes

def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False
    if bird_rect.top <= 0 or bird_rect.bottom >= HEIGHT:
        return False
    return True

def display_score(score):
    score_surface = font.render(f"Score: {score}", True, (255,255,255))
    screen.blit(score_surface, (10, 10))

# TIMER
SPAWNPIPE = pg.USEREVENT
pg.time.set_timer(SPAWNPIPE, 1200)

# GAME LOOP
game_active = True

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE and game_active:
                bird_movement = -10
            if event.key == pg.K_SPACE and not game_active:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100, HEIGHT//2)
                bird_movement = 0
                score = 0

        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

    screen.fill((0, 0, 0))

    if game_active:
        # BIRD
        bird_movement += gravity
        bird_rect.centery += int(bird_movement)
        screen.blit(bird, bird_rect)

        # PIPES
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        # COLLISION
        game_active = check_collision(pipe_list)

        # SCORE
        for pipe in pipe_list:
            if pipe.centerx == bird_rect.centerx:
                score += 1

        display_score(score)

    else:
        game_over = font.render("GAME OVER", True, (255, 0, 0))
        screen.blit(game_over, (120, 250))

    pg.display.update()
    clock.tick(60) 