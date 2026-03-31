# ui.py
from settings import *

def draw_text(screen, text, font, text_col, x, y, center=False):
    img = font.render(text, True, text_col)
    if center:
        rect = img.get_rect(center=(x, y))
    else:
        rect = img.get_rect(topleft=(x, y))
    screen.blit(img, rect)

def draw_text_outline(screen, text, font, text_col, x, y, center=False, outline_col=BLACK):
    # render base to get rect
    base = font.render(text, True, text_col)

    if center:
        rect = base.get_rect(center=(x, y))
    else:
        rect = base.get_rect(topleft=(x, y))

    # draw outline using original function
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx != 0 or dy != 0:
                draw_text(screen, text, font, outline_col,
                          rect.x + dx, rect.y + dy)

    # draw main text on top
    draw_text(screen, text, font, text_col, rect.x, rect.y)