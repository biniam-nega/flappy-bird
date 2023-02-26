from sys import exit
import time

import pygame


def display_score(score, add_score):
    score_text = font.render('Score: ' + str(score), False, (64, 64, 64))
    score_rect = score_text.get_rect(center=(400, 30))
    screen.blit(score_text, score_rect)
    if (player_rect.bottomleft[0] > lower_pipe_rect.bottomright[0]) and add_score:
        score += 1
    return score, False


pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Flappy Bird')
font = pygame.font.Font('assets/font/Pixeltype.ttf', 50)
clock = pygame.time.Clock()
game_state = False
gravity = 0
score = 0
add_score = True

sky_surface = pygame.image.load('assets/Sky.png')
ground_surface = pygame.image.load('assets/ground.png')

pipe_surface = pygame.image.load('assets/pipe.png')
pipe_x = 600
upper_pipe_rect = pygame.Rect(pipe_x, 0, 52, 100)
lower_pipe_rect = pygame.Rect(pipe_x, 205, 52, 100)

player_surface = pygame.image.load('assets/bird2.png').convert_alpha()
player_rect = player_surface.get_rect(midbottom=(40, 180))

# intro screen
start_surface = pygame.image.load('assets/replay.png')
start_rect = start_surface.get_rect(center=(400, 180))
title_text = font.render('Flappy Bird', True, (64, 64, 64))
title_rect = title_text.get_rect(center=(400, 70))
inst_text = font.render('Press Space to Start', False, (64, 64, 64))
inst_rect = inst_text.get_rect(center=(400, 270))

while True:
    # Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if game_state:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and game_state:
                    gravity = -10
        else:
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE) \
                    or (event.type == pygame.MOUSEBUTTONDOWN and start_rect.collidepoint((pygame.mouse.get_pos()))):
                game_state = True
                gravity = -10
                pipe_x = 600
                player_rect.bottom = 180
                score = 0

    screen.blit(sky_surface, (0, 0))
    screen.blit(ground_surface, (0, 300))
    screen.blit(player_surface, player_rect)
    
    if game_state:
        player_rect.y += gravity
        if gravity >= 0:
            gravity = 4
        gravity += 1

        # Pipes
        for i in range(95):
            screen.blit(pipe_surface, (pipe_x, i))
            screen.blit(pipe_surface, (pipe_x, 300-i))

        score, add_score = display_score(score, add_score)

        pipe_x -= 3
        upper_pipe_rect.x = pipe_x
        lower_pipe_rect.x = pipe_x
        if pipe_x < -50:
            pipe_x = 800
            add_score = True

        # collisions
        if player_rect.top < 0:
            player_rect.top = 0
        if player_rect.colliderect(upper_pipe_rect) or player_rect.colliderect(lower_pipe_rect):
            game_state = False
            time.sleep(1)
        if player_rect.bottom >= 300:
            game_state = False
            time.sleep(1)

    else:
        screen.blit(start_surface, start_rect)
        screen.blit(title_text, title_rect)
        if score:
            score_text = font.render('Your score is ' + str(score), False, (64, 64, 64))
            score_rect = score_text.get_rect(center=(400, 270))
            screen.blit(score_text, score_rect)
        else:
            screen.blit(inst_text, inst_rect)

    pygame.display.update()
    clock.tick(60)
