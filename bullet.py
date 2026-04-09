import pygame
from settings import HEIGHT

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


class BulletManager:
    def __init__(self):
        self.bullets = []
        self.image = pygame.image.load("Imgs/ammus.png").convert_alpha()
        self.cooldown = 250  # millisekuntia
        self.last_shot = 0

    def shoot(self, player):
        # cooldown tarkistus
        now = pygame.time.get_ticks()
        if now - self.last_shot < self.cooldown:
            return
        
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
                if bullet.get_collision_rect().colliderect(monster.get_collision_rect()):
                    self.bullets.remove(bullet)
                    monsters.remove(monster)
                    break