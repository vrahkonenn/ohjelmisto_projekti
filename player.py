# player.py
import pygame
from settings import PLAYER_SPEED

jump = False
y_change = 0
x_change = 0

def move_to_side(event):
    global x_change
    if event.key == pygame.K_a or event.key == pygame.K_LEFT:
        x_change = -PLAYER_SPEED
    if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
        x_change = PLAYER_SPEED
    return x_change

def key_check():
    global x_change
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        x_change = -PLAYER_SPEED
    if keys[pygame.K_RIGHT]:
        x_change = PLAYER_SPEED
    if sum(keys) == 0:
        x_change = 0
    return x_change

def update_player(y_pos):
    global jump, y_change
    gravity = .4
    jump_height = 13

    if jump:
        y_change = -jump_height
        jump = False

    y_pos += y_change
    y_change += gravity
    return y_pos
