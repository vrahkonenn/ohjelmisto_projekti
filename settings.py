# settings.py
import pygame

pygame.init()

WIDTH = 400
HEIGHT = 500
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
RED = (128, 0, 0)
ORANGE = (255, 165, 0)
PURKKA = (252,149,235)
TUMMA_PURKKA = (77,0,77)
KELTAINEN = (255,242,0)

MIN_PLATFORM_GAP = 60
MAX_PLATFORM_GAP = 100
MIN_PLATFORM_SEPARATION = 60
HORIZ_REACH = 120
MAX_PLAYER_HEIGHT = 150

resume_timer = 0
resume_wait = 3000 # 3 sekuntia

font_small = pygame.font.Font('fonts/BoldPixels.ttf', 24)
font_big = pygame.font.Font('fonts/BoldPixels.ttf', 32)
font_large = pygame.font.Font('fonts/BoldPixels.ttf', 40)

#font_big = pygame.font.SysFont('fonts/BoldPixels.ttf', 32)
#font_large = pygame.font.SysFont('Fonts/PressStart2P.ttf', 44)

def draw_text_with_outline(screen, font, text, pos, text_color, outline_color):
    x, y = pos

    base = font.render(text, True, text_color)
    outline = font.render(text, True, outline_color)

    # Piirrä outline (8 suuntaa)
    for dx in range(-2, 3):
            for dy in range(-2, 3):
                if dx != 0 or dy != 0:
                    screen.blit(outline, (x + dx, y + dy))

    # Piirrä pääteksti
    screen.blit(base, (x, y))