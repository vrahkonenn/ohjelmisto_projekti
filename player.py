# player.py
import pygame
from spritesheet import SpriteSheet
from settings import WIDTH

class Player:
    def __init__(self):
        self.scale = 90
        self.x = WIDTH/2 - (self.scale/2)
        self.y = 400
        self.spd = 4

        self.jump = False
        self.y_change = 0
        self.x_change = 0

        self.shooting = False
        self.shoot_time = 0
        self.shoot_duration = 150

        sprite_image = pygame.image.load("Imgs/frame1 (9).png").convert_alpha()
        sprite_sheet = SpriteSheet(sprite_image)

        shoot_sprite = pygame.image.load("Imgs/shooting_frames.png").convert_alpha()
        shoot_sheet = SpriteSheet(shoot_sprite)

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
            self.shoot_animation_list.append(
                shoot_sheet.get_image(x, 80, 80, 1, (0,0,0))
            )

    def shoot_animation(self):
        self.shooting = True
        self.shoot_time = pygame.time.get_ticks()

    def move_to_side(self, key):
        if key == pygame.K_a or key == pygame.K_LEFT:
            self.x_change = -self.spd
        if key == pygame.K_d or key == pygame.K_RIGHT:
            self.x_change = self.spd

    def key_check(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x_change = -self.spd
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x_change = self.spd
        else:
            self.x_change = 0

    def update(self):
        gravity = 0.4
        jump_height = 13

        if self.jump:
            self.y_change = -jump_height
            self.jump = False

        self.y += self.y_change
        #self.y_change += gravity

        self.x += self.x_change

        if self.x > 400 and self.x_change > 0:
            self.x = -25
        if self.x < 0 and self.x_change < 0:
            self.x = 375

    def animate(self):
        if self.animating:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_update >= self.animation_cooldown:
                self.frame += 1
                self.last_update = current_time

                if self.frame >= len(self.animation_list):
                    self.frame = len(self.animation_list) - 1
                    self.animating = False

        if self.shooting:
            now = pygame.time.get_ticks()
            if now - self.shoot_time > self.shoot_duration:
                self.shooting = False

    def start_animation(self):
        if not self.animating:
            self.animating = True
            self.frame = 0
            self.last_update = pygame.time.get_ticks()

    def draw(self, screen):

        if self.shooting:
            screen.blit(self.shoot_animation_list[self.frame], (self.x, self.y))
        else:
            screen.blit(self.animation_list[self.frame], (self.x, self.y))

    def get_collision_rect(self):
        return pygame.Rect(self.x + 20, self.y + 60, 35, 5)

    def reset(self):
        self.x = WIDTH/2 - (self.scale/2)
        self.y = 400
        self.x_change = 0
        self.y_change = 0
        self.jump = True