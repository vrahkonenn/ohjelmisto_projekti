import pygame
from settings import *

class Slider:
    def __init__(self, x, y, width, min_val=0.0, max_val=1.0, start_val=1.0):
        self.rect = pygame.Rect(x, y, width, 6)
        self.handle_radius = 8

        self.min_val = min_val
        self.max_val = max_val
        self.value = start_val

        self.dragging = False

    def draw(self, screen):
        pygame.draw.rect(screen, GRAY, self.rect)

        handle_x = self.rect.x + int((self.value - self.min_val) / (self.max_val - self.min_val) * self.rect.width)
        handle_y = self.rect.y + self.rect.height // 2

        pygame.draw.circle(screen, PURKKA, (handle_x, handle_y), self.handle_radius)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self._handle_rect().collidepoint(event.pos):
                self.dragging = True
        
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self.update_value(event.pos[0])

    def _handle_rect(self):
        handle_x = self.rect.x + int((self.value - self.min_val) / (self.max_val - self.min_val) * self.rect.width)
        handle_y = self.rect.y + self.rect.height // 2
        return pygame.Rect(handle_x - self.handle_radius, handle_y - self.handle_radius, self.handle_radius * 2, self.handle_radius * 2)

    def update_value(self, mouse_x):
        relative_x = mouse_x - self.rect.x
        relative_x = max(0, min(self.rect.width, relative_x))

        self.value = self.min_val + (relative_x / self.rect.width) * (self.max_val - self.min_val)

    def get_value(self):
        return self.value