import pygame
from settings import HEIGHT
import sound

class Bullet:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.speed = 10

        self.width = image.get_width()
        self.height = image.get_height()

    def update(self):
        self.y -= self.speed

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def off_screen(self):
        return self.y < -self.height
    
    def get_collision_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def get_center(self):
        center_x = self.x + self.width / 2
        center_y = self.y + self.height / 2
        return (center_x, center_y)

    def get_radius(self):
        return self.width / 2


class BulletManager:
    def __init__(self):
        self.bullets = []
        self.image = pygame.image.load("Imgs/ammus.png").convert_alpha()
        self.cooldown = 250  # millisekuntia
        self.last_shot = 0
        self.coins_earned = 0

    def shoot(self, player):
        # cooldown tarkistus
        now = pygame.time.get_ticks()
        if now - self.last_shot < self.cooldown:
            return
        
        sound.play_sfx(sound.sfx["shoot"])
        
        self.last_shot = now
        
        bullet_x = player.x + (player.scale / 2) - (self.image.get_width() / 2)
        bullet_y = player.y + (player.scale / 2) - (self.image.get_height() / 2)

        bullet = Bullet(bullet_x, bullet_y, self.image)
        self.bullets.append(bullet)

    def update(self):
        for bullet in self.bullets:
            bullet.update()

        self.bullets = [b for b in self.bullets if not b.off_screen()]

    def draw(self, screen):
        for bullet in self.bullets:
            bullet.draw(screen)

    def check_hits(self, monsters):
        for bullet in self.bullets[:]:
            for monster in monsters[:]:
                bx, by = bullet.get_center()
                br = bullet.get_radius()

                mx, my = monster.get_center()
                mr = monster.get_radius() + 10

                dx = mx - bx
                dy = my - by

                if dx*dx + dy*dy < (mr + br)**2:
                    self.bullets.remove(bullet)
                    monster.die()
                    self.coins_earned = 2
                    break