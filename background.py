import pygame
from settings import HEIGHT

class Background:
    def __init__(self):
        self.bg_ground = pygame.image.load("Imgs/ground.png").convert()
        self.bg_sky = pygame.image.load("Imgs/background.png").convert()
        self.bg_transition = pygame.image.load("Imgs/sky_space.png").convert()
        self.bg_space = pygame.image.load("Imgs/space.png").convert()

        self.backgrounds = [
            self.bg_ground,
            self.bg_sky,
            self.bg_transition
        ]

    def draw(self, screen, scroll):
        index = int(scroll // HEIGHT)
        offset = scroll % HEIGHT

        if index < len(self.backgrounds):
            current_bg = self.backgrounds[index]
        else:
            current_bg = self.bg_space

        if index + 1 < len(self.backgrounds):
            next_bg = self.backgrounds[index + 1]
        else:
            next_bg = self.bg_space

        screen.blit(current_bg, (0, offset))
        screen.blit(next_bg, (0, offset - HEIGHT))