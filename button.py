import pygame
import sound

class Button:
    def __init__(self, x, y, width, height, text, font, bg_color, text_color, outline_color = (0,0,0)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.bg_color = bg_color
        self.text_color = text_color
        self.outline_color = outline_color

    def draw(self, surface):
        #tausta
        pygame.draw.rect(surface, self.bg_color, self.rect)
        #kehys
        pygame.draw.rect(surface, self.outline_color, self.rect, 2)
        #teksti keskelle
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
    
    def is_clicked(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            sound.play_sfx(sound.sfx["click"])
            return True
        return False