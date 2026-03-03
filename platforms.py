# platforms.py
import pygame
import random
from settings import *

class PlatformManager:
    def __init__(self):
        self.initial_platforms = [
            [175, 480, 70 , 10, 0],
            [85 , 370, 70 , 10, 1],
            [265, 370, 70 , 10, 0],
            [175, 260, 70 , 10, 0],
            [85 , 150, 70 , 10, 1],
            [265, 150, 70 , 10, 0],
            [175, 40 , 70 , 10, 0]
        ]
        self.platforms = self.initial_platforms.copy()

        self.images = {
            0: pygame.image.load("Imgs/normal.png").convert_alpha(),
            1: pygame.image.load("Imgs/breakable.png").convert_alpha(),
            2: pygame.image.load("Imgs/broken.png").convert_alpha(),
            3: pygame.image.load("Imgs/trap.png").convert_alpha()
        }

    def draw(self, screen):
        blocks = []
        for p in self.platforms:
            screen.blit(self.images[p[4]], (p[0], p[1]))
            blocks.append(pygame.Rect(p[0], p[1], p[2], p[3]))
        return blocks

    def check_collisions(self, player):
        for i in range(len(self.platforms)):
            if pygame.Rect(self.platforms[i][0], self.platforms[i][1],
                           self.platforms[i][2], self.platforms[i][3]).colliderect(
                           player.get_collision_rect()) and player.y_change > 0:

                if self.platforms[i][4] == 0:
                    return True

                if self.platforms[i][4] == 1:
                    self.platforms[i][4] = 2
                    return True

                if self.platforms[i][4] == 3:
                    return False
        return False

    def update(self, player):
        score_add = 0

        if player.y <= 200 and player.y_change < 0:
            player.y = 200
            for p in self.platforms:
                p[1] -= player.y_change
            score_add = abs(player.y_change) * 0.05

        for p in self.platforms:
            if p[4] == 2:
                p[1] += 8

        for i in range(len(self.platforms)):
            if self.platforms[i][1] > 510:
                highest_y = min(p[1] for p in self.platforms)
                spawn_x = random.randint(10, 300)
                spawn_y = highest_y - random.randint(MIN_PLATFORM_GAP, MAX_PLATFORM_GAP)
                platform_type = random.choices([0,1,3], weights=[75,20,5])[0]
                self.platforms[i] = [spawn_x, spawn_y, 70, 10, platform_type]

        return score_add

    def reset(self):
        self.platforms = self.initial_platforms.copy()