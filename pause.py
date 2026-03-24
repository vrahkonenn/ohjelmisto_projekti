from ui import draw_text, draw_text_outline
from settings import *

class PauseScreen:
    def draw(self, screen):
        draw_text_outline(screen, "PAUSE", font_large, WHITE, WIDTH//2, HEIGHT//2 - 140, center=True)
        draw_text_outline(screen, "Paina ESC jatkaaksesi", font_small, WHITE, WIDTH//2, HEIGHT//2 - 90, center=True)

    def draw_countdown(self, screen, number):
        draw_text_outline(screen, str(number), font_large, WHITE, WIDTH//2, HEIGHT//2, center=True)