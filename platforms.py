# platforms.py
import pygame
import random
from settings import *
from coin import Coin

class Platform:
    def __init__(self, x, y, width=70, height=10, platform_type="normal", moving=False):
            
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.type = platform_type
        self.visual_offset_x = 8

        self.moving = moving
        self.direction = random.choice([-1, 1])
        self.speed = random.uniform(1.0, 3.0)

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen, images):
        screen.blit(images[self.type], (self.x, self.y))

    def update(self):
        # Broken putoaa
        if self.type == "broken":
            self.y += 8

        # Liikkuva alusta
        if self.moving:
            self.x += self.speed * self.direction

            # Reunat
            if self.x <= 0:
                self.x = 0
                self.direction = 1

            if self.x + self.width >= WIDTH:
                self.x = WIDTH - self.width
                self.direction = -1


class PlatformManager:
    def __init__(self):
        self.coin = None
        self.images = {
            "normal": pygame.image.load("Imgs/normal.png").convert_alpha(),
            "breakable": pygame.image.load("Imgs/breakable.png").convert_alpha(),
            "broken": pygame.image.load("Imgs/broken.png").convert_alpha(),
            "trap": pygame.image.load("Imgs/trap.png").convert_alpha()
        }

        self.initial_data = [
            (175, 480, "normal", False),
            (85 , 370, "normal", False),
            (265, 370, "normal", False),   
            (175, 260, "normal", False),
            (85 , 150, "normal", False),
            (265, 150, "normal", False),
            (175, 40 , "normal", False)
        ]

        self.last_spawn_type = "normal"

        self.normal_weight = 100
        self.breakable_weight = 0
        self.trap_weight = 0

        self.platforms = []
        self.create_initial_platforms()

    def create_initial_platforms(self):
        self.platforms.clear()
        for x, y, p_type, moving in self.initial_data:
            self.platforms.append(
                Platform(x, y, 70, 10, p_type, moving)
            )

    def draw(self, screen):
        for platform in self.platforms:
            platform.draw(screen, self.images)

    def check_collisions(self, player):
        for platform in self.platforms:
            if platform.get_rect().colliderect(
                player.get_collision_rect()
            ) and player.y_change > 0:

                if platform.type == "normal":
                    return True

                if platform.type == "breakable":
                    platform.type = "broken"
                    return True

                if platform.type == "trap":
                    return False

        return False

    def update(self, player):
        score_add = 0

        # Kamera lock
        if player.y <= 200 and player.y_change < 0:
            player.y = 200
            for p in self.platforms:
                p.y -= player.y_change
                if self.coin:
                    self.coin.y = self.coin.platform.y - 50
            score_add = abs(player.y_change) * 0.05

        # Päivitä kaikki alustat
        for p in self.platforms:
            p.update()

        # Respawn
        for i, p in enumerate(self.platforms):
            if p.y > 510:

                if self.coin and self.coin.y > 430:
                    self.coin = None
                highest_y = min(platform.y for platform in self.platforms)

                spawn_x = random.randint(10, 300)
                spawn_y = highest_y - random.randint(
                    MIN_PLATFORM_GAP,
                    MAX_PLATFORM_GAP
                )

                platform_type = random.choices(
                    ["normal", "breakable", "trap"],
                    # Weights = % mahdollisuus alustalle
                    weights=[self.normal_weight, self.breakable_weight, self.trap_weight]
                )[0]

                if self.last_spawn_type == "trap" and platform_type == "trap":
                    platform_type = "normal"
                self.last_spawn_type = platform_type

                # 30% mahdollisuus olla liikkuva
                moving = random.random() < 0.3

                self.platforms[i] = Platform(
                    spawn_x,
                    spawn_y,
                    70,
                    10,
                    platform_type,
                    moving
                )
                if platform_type == "normal" and random.random()<0.1 and not self.coin:
                    coin_x = spawn_x + (p.width // 2) - (80 // 2)
                    coin_y = spawn_y
                    self.coin = Coin(coin_x, coin_y)
                    self.coin.platform = self.platforms[i]


        return score_add
    
    def update_weights(self):
        if self.normal_weight <= 0:
            return
        
        self.normal_weight -= 2.5
        self.breakable_weight += 2
        self.trap_weight += 0.5

    def reset_weights(self):
        self.normal_weight = 100
        self.breakable_weight = 0
        self.trap_weight = 0

    def reset(self):
        self.create_initial_platforms()
        self.coin = None