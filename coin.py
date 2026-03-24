# coin.py
import pygame
from spritesheet import SpriteSheet


class Coin:
    def __init__(self, x, y):
        self.scale = 90
        self.x = x
        self.y = y
     

        self.y_change = 0
        self.x_change = 0


        sprite_image = pygame.image.load("Imgs/coin.png").convert_alpha()
        sprite_sheet = SpriteSheet(sprite_image)


        self.animation_list = []
        self.shoot_animation_list = []
        self.animation_steps = 6
        self.animation_cooldown = 75
        self.last_update = pygame.time.get_ticks()
        self.frame = 0
        self.animating = False

        for x in range(self.animation_steps):
            self.animation_list.append(
                sprite_sheet.get_image(x, 80, 80, 1, (0,0,0))
            )

    def animate(self):
        if self.animating:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_update >= self.animation_cooldown:
                self.frame += 1
                self.last_update = current_time

                if self.frame >= len(self.animation_list):
                    self.frame = 0
                    
    def start_animation(self):
        if not self.animating:
            self.animating = True
            self.frame = 0
            self.last_update = pygame.time.get_ticks()

    def draw(self, screen):
        screen.blit(self.animation_list[self.frame], (self.x, self.y))

    def get_collision_rect(self):
        return pygame.Rect(self.x, self.y, 80, 80)

