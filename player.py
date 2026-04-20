# player.py
import pygame
import saves
import sound
from spritesheet import SpriteSheet
from settings import WIDTH

class Player:
    def __init__(self, jump_height):
        data = saves.get_data()
        
        self.scale = 90
        self.x = WIDTH/2 - (self.scale/2)
        self.y = 550
        self.spd = 4
        self.is_immune = False
        self.death_source = "falling"

        self.jump = False
        self.jump_height = jump_height
        self.y_change = 0
        self.x_change = 0

        self.shooting = False
        self.shoot_time = 0
        self.shoot_duration = 150

        self.shoes_charges = 0

        self.jetpack_active = False
        self.jetpack_timer = 0
        self.jetpack_duration = 3000 + data["jetpack_dur"][0]  # ms

        self.umbrella_active = False
        self.umbrella_timer = 0
        self.umbrella_duration = 3000 + data["umbrella_dur"][0]  # ms

        sprite_image = pygame.image.load("Imgs/frame1 (9).png").convert_alpha()
        sprite_sheet = SpriteSheet(sprite_image)

        shoot_sprite = pygame.image.load("Imgs/shooting_frames.png").convert_alpha()
        shoot_sheet = SpriteSheet(shoot_sprite)

        jumpshoes_sprite = pygame.image.load("Imgs/boostit/purkkakengät_frame.png").convert_alpha()
        jumpshoes_sheet = SpriteSheet(jumpshoes_sprite)

        jumpshoes_shoot_sprite = pygame.image.load("Imgs/boostit/purkkakengät_shooting_frame.png").convert_alpha()
        jumpshoes_shoot_sheet = SpriteSheet(jumpshoes_shoot_sprite)

        umbrella_sprite = pygame.image.load("Imgs/boostit/purkkavarjo_frame.png").convert_alpha()
        umbrella_sheet = SpriteSheet(umbrella_sprite)

        umbrella_shoot_sprite = pygame.image.load("Imgs/boostit/purkkavarjo_shooting_frame.png").convert_alpha()
        umbrella_shoot_sheet = SpriteSheet(umbrella_shoot_sprite)

        jetpack_sprite = pygame.image.load("Imgs/boostit/jetpack_framet2.png").convert_alpha()
        jetpack_sheet = SpriteSheet(jetpack_sprite)

        jetpack_shoot_sprite = pygame.image.load("Imgs/boostit/jetpack_shooting_frames.png").convert_alpha()
        jetpack_shoot_sheet = SpriteSheet(jetpack_shoot_sprite)

        jumpshoes_jetpack_sprite = pygame.image.load("Imgs/boostit/purkkakengät_jetpack_frame.png").convert_alpha()
        jumpshoes_jetpack_sheet = SpriteSheet(jumpshoes_jetpack_sprite)

        jumpshoes_jetpack_shoot_sprite = pygame.image.load("Imgs/boostit/purkkakengät_jetpack_shooting_frame.png").convert_alpha()
        jumpshoes_jetpack_shoot_sheet = SpriteSheet(jumpshoes_jetpack_shoot_sprite)

        jumpshoes_umbrella_sprite = pygame.image.load("Imgs/boostit/purkkakengät_purkkavarjo_frame.png").convert_alpha()
        jumpshoes_umbrella_sheet = SpriteSheet(jumpshoes_umbrella_sprite)

        jumpshoes_umbrella_shoot_sprite = pygame.image.load("Imgs/boostit/purkkakengät_purkkavarjo_shooting_frame.png").convert_alpha()
        jumpshoes_umbrella_shoot_sheet = SpriteSheet(jumpshoes_umbrella_shoot_sprite)


        self.animation_list = []
        self.shoot_animation_list = []

        self.jumpshoes_animation_list = []
        self.jumpshoes_shoot_animation_list = []

        self.umbrella_animation_list = []
        self.umbrella_shoot_animation_list = []

        self.jetpack_animation_list = []
        self.jetpack_shoot_animation_list = []

        self.jumpshoes_jetpack_animation_list = []
        self.jumpshoes_jetpack_shoot_animation_list = []

        self.jumpshoes_umbrella_animation_list = []
        self.jumpshoes_umbrella_shoot_animation_list = []

        self.animation_steps = 6
        self.animation_cooldown = 75
        self.last_update = pygame.time.get_ticks()
        self.frame = 0
        self.animating = False

        self.umbrella_open = False

        for x in range(self.animation_steps):
            self.animation_list.append(
                sprite_sheet.get_image(x, 80, 80, 1, (0,0,0))
            )
            self.shoot_animation_list.append(
                shoot_sheet.get_image(x, 80, 80, 1, (0,0,0))
            )
            self.jumpshoes_animation_list.append(
                jumpshoes_sheet.get_image(x, 80, 80, 1, (0,0,0))
            )
            self.jumpshoes_shoot_animation_list.append(
                jumpshoes_shoot_sheet.get_image(x, 80, 80, 1, (0,0,0))
            )
            self.umbrella_animation_list.append(
                umbrella_sheet.get_image(x, 80, 80, 1, (0,0,0))
            )
            self.umbrella_shoot_animation_list.append(
                umbrella_shoot_sheet.get_image(x, 80, 80, 1, (0,0,0))
            )
            self.jetpack_animation_list.append(
                jetpack_sheet.get_image(x, 80, 80, 1, (0,0,0))
            )
            self.jetpack_shoot_animation_list.append(
                jetpack_shoot_sheet.get_image(x, 80, 80, 1, (0,0,0))
            )
            self.jumpshoes_jetpack_animation_list.append(
                jumpshoes_jetpack_sheet.get_image(x, 80, 80, 1, (0,0,0))
            )
            self.jumpshoes_jetpack_shoot_animation_list.append(
                jumpshoes_jetpack_shoot_sheet.get_image(x, 80, 80, 1, (0,0,0))
            )
            self.jumpshoes_umbrella_animation_list.append(
                jumpshoes_umbrella_sheet.get_image(x, 80, 80, 1, (0,0,0))
            )
            self.jumpshoes_umbrella_shoot_animation_list.append(
                jumpshoes_umbrella_shoot_sheet.get_image(x, 80, 80, 1, (0,0,0))
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
        current_time = pygame.time.get_ticks()

        if self.jetpack_active:
            self.is_immune = True
            self.y_change = -10  # jatkuva nousu

            if current_time - self.jetpack_timer > self.jetpack_duration:
                self.jetpack_active = False
                self.is_immune = False
                self.frame = 0

        if self.umbrella_active:
            if current_time - self.umbrella_timer > self.umbrella_duration:
                    self.umbrella_active = False
                    self.umbrella_open = False
        if self.umbrella_active and self.y_change > 0:
            if not self.umbrella_open:
                sound.play_sfx(sound.sfx["umbrella"])
                self.umbrella_open = True
            
        gravity = 0.4

        if self.jump:
            if self.shoes_charges > 0:
                self.y_change = -self.jump_height * 1.5
                self.shoes_charges -= 1
            else:
                self.y_change = -self.jump_height
            self.jump = False

        self.y += self.y_change
        if not self.jetpack_active:
            if self.umbrella_active and self.y_change > 0:
                self.y_change += gravity * 0.2
            else:
                self.y_change += gravity
        self.x += self.x_change

        if self.x > 400 and self.x_change > 0:
            self.x = -25
        if self.x < 0 and self.x_change < 0:
            self.x = 375

    def animate(self):
        current_time = pygame.time.get_ticks()

        # Jetpack-animaatio pyörii jatkuvasti
        if self.jetpack_active:
            if current_time - self.last_update >= self.animation_cooldown:
                self.frame += 1
                self.last_update = current_time

                if self.frame >= len(self.animation_list):
                    self.frame = 0  # loopataan animaatio alusta

        # Normaali hyppyanimaatio
        elif self.animating:
            if current_time - self.last_update >= self.animation_cooldown:
                self.frame += 1
                self.last_update = current_time

                if self.frame >= len(self.animation_list):
                    self.frame = len(self.animation_list) - 1
                    self.animating = False

        # Shooting timeout
        if self.shooting:
            if current_time - self.shoot_time > self.shoot_duration:
                self.shooting = False

    def start_animation(self):
        if not self.animating:
            self.animating = True
            self.frame = 0
            self.last_update = pygame.time.get_ticks()

    def draw(self, screen):
        if self.shooting:
            if self.jetpack_active and self.shoes_charges > 0:
                screen.blit(self.jumpshoes_jetpack_shoot_animation_list[self.frame], (self.x, self.y))
            elif self.jetpack_active:
                screen.blit(self.jetpack_shoot_animation_list[self.frame], (self.x, self.y))
            elif self.umbrella_active and self.shoes_charges > 0:
                screen.blit(self.jumpshoes_umbrella_shoot_animation_list[self.frame], (self.x, self.y))
            elif self.umbrella_active:
                screen.blit(self.umbrella_shoot_animation_list[self.frame], (self.x, self.y))
            elif self.shoes_charges > 0:
                screen.blit(self.jumpshoes_shoot_animation_list[self.frame], (self.x, self.y))
            else:
                screen.blit(self.shoot_animation_list[self.frame], (self.x, self.y))
        else:
            if self.jetpack_active and self.shoes_charges > 0:
                screen.blit(self.jumpshoes_jetpack_animation_list[self.frame], (self.x, self.y))
            elif self.jetpack_active:
                screen.blit(self.jetpack_animation_list[self.frame], (self.x, self.y))
            elif self.umbrella_active and self.shoes_charges > 0:
                screen.blit(self.jumpshoes_umbrella_animation_list[self.frame], (self.x, self.y))
            elif self.umbrella_active:
                screen.blit(self.umbrella_animation_list[self.frame], (self.x, self.y))
            elif self.shoes_charges > 0:
                screen.blit(self.jumpshoes_animation_list[self.frame], (self.x, self.y))
            else:
                screen.blit(self.animation_list[self.frame], (self.x, self.y))

    def get_collision_rect(self):
        return pygame.Rect(self.x + 20, self.y + 60, 35, 5)
    
    def get_hitbox(self):
        return pygame.Rect(self.x + 10, self.y + 10, 70, 70)

    def get_center(self):
        center_x = self.x + self.scale / 2 -5
        center_y = self.y + self.scale / 2 -8
        return (center_x, center_y)

    def get_radius(self):
        return 20

    def reset(self):
        self.x = WIDTH/2 - (self.scale/2)
        self.y = 550
        self.x_change = 0
        self.y_change = 0
        self.jump = True

        self.jetpack_active = False
        self.jetpack_timer = 0
    
        self.umbrella_active = False
        self.umbrella_timer = 0
    
        self.shoes_charges = 0
        self.death_source = "falling"