import pygame
import random
from spritesheet import SpriteSheet
from settings import *

class SpaceMonster:
    def __init__(self, x, y, moving):
        self.scale = 90
        self.x = x
        self.y = y

        self.y_change = 0
        self.x_change = 0

        self.width = self.scale
        self.height = self.scale

        monster_image = pygame.image.load("Imgs/alien.png").convert_alpha()
        sprite_sheet = SpriteSheet(monster_image)

        self.animation_list = []
        self.shoot_animation_list = []
        self.animation_steps = 5
        self.animation_cooldown = 75
        self.last_update = pygame.time.get_ticks()
        self.frame = 0
        self.animating = False

        self.moving = moving
        self.direction = random.choice([-1,1])
        self.speed = random.uniform(1.0, 3.0)

        for x in range(self.animation_steps):
            self.animation_list.append(
                sprite_sheet.get_image(x, 90, 90, 1, (0,0,0))
            )

        def get_collision_rect(self):
            return pygame.Rect(self.x, self.y, self.width, self.height)
        

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

    def update(self, player):
        # Kamera lock
        if player.y <= 200 and player.y_change < 0:
            self.y -= player.y_change
        
        if self.moving:
            self.x += self.speed * self.direction

            if self.x <= 0:
                self.x = 0
                self.direction = 1

            if self.x + self.width >= WIDTH:
                self.x = WIDTH - self.width
                self.direction = -1
    

class SpaceMonsterManager:
    def __init__(self):
        self.monsters = []
        self.last_monster_spawn = 0 #tallentaa ajan jollon vika monsteri spawnattu
        self.monster_spawn_delay = 4000
        self.min_score = 1000
        self.max_score = 20000

    def update(self, player, score):
        current_time = pygame.time.get_ticks()

        if self.min_score <= score:
            if current_time - self.last_monster_spawn > self.monster_spawn_delay:
                spawn_x = random.randint(50, 250)
                spawn_y = -100 #reunan ulkopuolella

                moving = random.random() < 0.5

                self.monsters.append(SpaceMonster(spawn_x, spawn_y, moving))
                self.monsters[-1].start_animation()
                self.last_monster_spawn = current_time
                self.monster_spawn_delay = random.randint(6000, 15000)
        
        for monster in self.monsters:
            monster.update(player)
            monster.animate()

        # poistaa monsterit, jotka ovat ruudun ulkopuolella
        self.monsters = [m for m in self.monsters if m.y < HEIGHT + 100]

    def draw(self, screen):
        for monster in self.monsters:
            monster.draw(screen)

    def check_player_collision(self, player):
        for monster in self.monsters:
            if player.get_hitbox().colliderect(monster.get_collision_rect()):
                return True
        return False
    
    def reset(self):
        self.monsters = []