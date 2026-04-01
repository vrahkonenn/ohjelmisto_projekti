# powerups.py
import pygame
import saves

class PowerUp:
    images = {
        "jumpboost": None,
        "jetpack": None,
        "shoes": None,
        "umbrella": None, 
    }

    offsets = {
        "jumpboost": {
            "normal": (-6, 22),
            "breakable": (-6, 34),
            "trap": (0,0),
            "broken": (0,0)
        },
        "jetpack": {
            "normal": (-8, 0),
            "breakable": (-6, 8),
            "trap": (0,0),
            "broken": (0,0)
        },
        "shoes": {
            "normal": (-6, 8),
            "breakable": (-6, 15),
            "trap": (0,0),
            "broken": (0,0)
        },
        "umbrella": {
            "normal": (-8, -10),
            "breakable": (-6, -4),
            "trap": (0,0),
            "broken": (0,0)
        },
    }

    def load_images():
        PowerUp.images = {
            "jumpboost": load_image("Imgs/boostit/boost.png"),
            "jetpack": load_image("Imgs/boostit/purkkapack.png"),
            "shoes": load_image("Imgs/boostit/kengat.png"),
            "umbrella": load_image("Imgs/boostit/varjo.png"),
        }

    def __init__(self, platform, p_type):

        self.platform = platform
        self.type = p_type

        self.width = 40
        self.height = 40

        self.active = True

    def get_position(self):
        base_x = (
            self.platform.x
            + self.platform.width // 2
            + self.platform.visual_offset_x
            - self.width // 2
        )

        base_y = self.platform.y - self.height

        offset_x, offset_y = PowerUp.offsets[self.type][self.platform.type]

        x = base_x + offset_x
        y = base_y + offset_y

        return x, y

    def get_rect(self):
        x, y = self.get_position()
        return pygame.Rect(x, y, self.width, self.height)

    def trigger(self):
        self.active = False

    def update(self):
        if self.platform.y > 510:
            self.active = False

    def draw(self, screen):
        if not self.active:
            return

        x, y = self.get_position()

        # piirrä kuva
        if self.type in PowerUp.images:
            image = PowerUp.images[self.type]
            screen.blit(image, (x, y))
        else:
            # fallback jos kuva puuttuu
            pygame.draw.rect(screen, (255, 255, 255), (x, y, self.width, self.height), 2)

        # DEBUG: hitbox (voit poistaa myöhemmin)
        # pygame.draw.rect(screen, (255, 0, 0), (x, y, self.width, self.height), 1)

def load_image(path):
    img = pygame.image.load(path).convert_alpha()
    return pygame.transform.scale(img, (60, 64))



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