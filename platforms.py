# platforms.py
import pygame
import random
from settings import *

class Platform:
    def __init__(self, x, y, width=70, height=10, platform_type="normal", moving=False):

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.type = platform_type

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

        self.images = {
            "normal": pygame.image.load("Imgs/normal.png").convert_alpha(),
            "breakable": pygame.image.load("Imgs/breakable.png").convert_alpha(),
            "broken": pygame.image.load("Imgs/broken.png").convert_alpha(),
            "trap": pygame.image.load("Imgs/trap.png").convert_alpha()
        }

        self.initial_data = [
            (175, 480, "normal", False),
            (85 , 370, "breakable", False),
            (265, 370, "normal", False),   
            (175, 260, "normal", False),
            (85 , 150, "breakable", False),
            (265, 150, "normal", False),
            (175, 40 , "normal", False)
        ]

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
            score_add = abs(player.y_change) * 0.05

        # Päivitä kaikki alustat
        for p in self.platforms:
            p.update()

        # Respawn
        for i, p in enumerate(self.platforms):
            if p.y > 510:

                highest_y = min(platform.y for platform in self.platforms)

                spawn_x = random.randint(10, 300)
                spawn_y = highest_y - random.randint(
                    MIN_PLATFORM_GAP,
                    MAX_PLATFORM_GAP
                )

                platform_type = random.choices(
                    ["normal", "breakable", "trap"],
                    # Weights = % mahdollisuus alustalle
                    weights=[70, 20, 10]
                )[0]

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

        return score_add

    def reset(self):
        self.create_initial_platforms()