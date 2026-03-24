# settings.py
import pygame

pygame.init()

WIDTH = 400
HEIGHT = 500
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)

MIN_PLATFORM_GAP = 60
MAX_PLATFORM_GAP = 100
MIN_PLATFORM_SEPARATION = 60
HORIZ_REACH = 120
MAX_PLAYER_HEIGHT = 150

resume_timer = 0
resume_wait = 3000 # 3 sekuntia

font_small = pygame.font.SysFont('Lucida Sans', 20)
font_big = pygame.font.SysFont('Lucida Sans', 24)
font_large = pygame.font.SysFont('Fonts/PressStart2P.ttf', 44)