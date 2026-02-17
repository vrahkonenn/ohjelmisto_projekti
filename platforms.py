# platforms.py
import random
import pygame
from settings import *

def check_collisions(rect_list, player_x, player_y, y_change, platforms):
    for i in range(len(rect_list)):
        if rect_list[i].colliderect([player_x + 20, player_y + 60, 35, 5]) and y_change > 0:
            
            if platforms[i][4] == 0:
                return True
            
            if platforms[i][4] == 1:
                platforms[i][4] = 2
                return True
            
            if platforms[i][4] == 3:
                return False
    return False


def updatePlatforms(my_list, y_pos, y_change, player_x, score):

    for i in range(len(my_list)):
        if my_list[i][4] == 2:
            my_list[i][1] += 8

    for item in range(len(my_list)):
        if my_list[item][1] > 510:

            highest_y = min(p[1] for p in my_list)
            spawn_x = random.randint(10, 300)
            spawn_y = highest_y - random.randint(MIN_PLATFORM_GAP, MAX_PLATFORM_GAP)

            platform_type = random.choices([0,1,3], weights=[75,20,5])[0]

            my_list[item] = [spawn_x, spawn_y, 70, 10, platform_type]

    return my_list
