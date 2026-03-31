# powerups.py
import pygame
import saves

class PowerUp:
    def __init__(self, platform, p_type):
        self.platform = platform
        self.type = p_type

        self.width = 40
        self.height = 40

        self.active = True

    def get_position(self):
        x = (
            self.platform.x
            + self.platform.width // 2
            + self.platform.visual_offset_x
            - self.width // 2
        )
        y = self.platform.y + 10 - self.height
        return x, y

    def get_rect(self):
        x, y = self.get_position()
        return pygame.Rect(x, y, self.width, self.height)

    def trigger(self):
        self.active = False

    def update(self):
        # poista jos menee ruudun ulkopuolelle
        if self.platform.y > 510:
            self.active = False

    def draw(self, screen):
        if not self.active:
            return

        x, y = self.get_position()

        if self.type == "jumpboost":
            color = (255, 0, 0)
        elif self.type == "jetpack":
            color = (0, 255, 0)
        elif self.type == "shoes":
            color = (0, 0, 255)
        elif self.type == "umbrella":
            color = (255, 255, 0)
        else:
            color = (255, 255, 255)


        # POWERUP HITBOX
        pygame.draw.rect(screen, color, (x, y, self.width, self.height), 2)



class PowerUpManager:
    def __init__(self):
        upgrades = saves.get_data()
        self.nothing = 90 - (upgrades["jumpboost"] + upgrades["jetpack"] + upgrades["shoes"] + upgrades["umbrella"])
        self.powerups = []
        self.spawn_chances = {
        "jumpboost": 2.5 + upgrades["jumpboost"],
        "jetpack": 2.5 + upgrades["jetpack"],
        "shoes": 2.5 + upgrades["shoes"],
        "umbrella": 2.5 + upgrades["umbrella"],
        None: self.nothing
}

    def spawn_on_platform(self, platform):
        import random

        if hasattr(platform, "has_powerup"):
            return

        total_weight = sum(self.spawn_chances.values())

        roll = random.uniform(0, total_weight)

        current = 0

        for p_type, weight in self.spawn_chances.items():
            current += weight
            if roll <= current:
                chosen_type = p_type
                break

        if chosen_type is None:
            return

        p = PowerUp(platform, chosen_type)
        self.powerups.append(p)
        platform.has_powerup = True

    def update(self):
        for p in self.powerups:
            p.update()

        self.powerups = [p for p in self.powerups if p.active]

    def reset(self):
        self.powerups.clear()

    def draw(self, screen):
        for p in self.powerups:
            p.draw(screen)

    def check_collision(self, player):
        for p in self.powerups:
            if p.get_rect().colliderect(player.get_collision_rect()):
                p.trigger()
                return p.type
        return None