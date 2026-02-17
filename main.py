import pygame
from settings import *
import player
import platforms as platform_module
from utils import draw_text
import spritesheet

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TEMP_Hyppypeli_TEMP")

sprite_sheet_image = pygame.image.load("Imgs/frame1 (9).png").convert_alpha()
sprite_sheet = spritesheet.SpriteSheet(sprite_sheet_image)

player_image = pygame.image.load("Imgs/frame1 (9).png").convert_alpha()

platform_images = {
    0: pygame.image.load("Imgs/normal.png").convert_alpha(),
    1: pygame.image.load("Imgs/breakable.png").convert_alpha(),
    2: pygame.image.load("Imgs/broken.png").convert_alpha(),
    3: pygame.image.load("Imgs/trap.png").convert_alpha()
}

sprite_sheet = spritesheet.SpriteSheet(player_image)
animation_list = []
animation_steps = 6
animation_cooldown = 75
last_update = pygame.time.get_ticks()
frame = 0
animating = False

for x in range(animation_steps):
    animation_list.append(
        sprite_sheet.get_image(x, 80, 80, 1, (0, 0, 0))
    )

timer = pygame.time.Clock()

background = WHITE
game_over = False
score = 0

# Fontit
font_small = pygame.font.SysFont('Lucida Sans', 20)
font_big = pygame.font.SysFont('Lucida Sans', 24)

# Pelaajan alkuarvot
player_x = WIDTH / 2 - (PLAYER_SCALE / 2)
player_y = 400

# Alustat
initial_platforms = [
    [175, 480, 70 , 10, 0],
    [85 , 370, 70 , 10, 1],
    [265, 370, 70 , 10, 0],
    [175, 260, 70 , 10, 0],
    [85 , 150, 70 , 10, 1],
    [265, 150, 70 , 10, 0],
    [175, 40 , 70 , 10, 0]
]

platforms = initial_platforms.copy()

running = True
while running:

    timer.tick(FPS)

    if not game_over:

        screen.fill(background)

        player_x += player.x_change
        player_y = player.update_player(player_y)

        if player_x > WIDTH and player.x_change > 0:
            player_x = -25
        if player_x < 0 and player.x_change < 0:
            player_x = WIDTH - 25

        blocks = []
        for p in platforms:
            block = pygame.Rect(p[0], p[1], p[2], p[3])
            blocks.append(block)

        player.jump = platform_module.check_collisions(
            blocks,
            player_x,
            player_y,
            player.y_change,
            platforms
        )
        if player.jump and not animating:
            animating = True
            frame = 0
            last_update = pygame.time.get_ticks()

        if player_y <= 200 and player.y_change < 0:
            player_y = 200
            for p in platforms:
                p[1] -= player.y_change
            score += abs(player.y_change) * 0.05

        platforms = platform_module.updatePlatforms(
            platforms,
            player_y,
            player.y_change,
            player_x,
            score
        )

        for p in platforms:
            image = platform_images[p[4]]
            screen.blit(image, (p[0], p[1]))

        current_time = pygame.time.get_ticks()

        if animating:
            if current_time - last_update >= animation_cooldown:
                frame += 1
                last_update = current_time

                if frame >= len(animation_list):
                    frame = len(animation_list) - 1
                    animating = False

        screen.blit(animation_list[frame], (player_x, player_y))

        if player_y > HEIGHT:
            game_over = True

    else:
        draw_text(screen, 'GAME OVER!', font_big, BLACK, 130, 200)
        draw_text(screen, 'SCORE: ' + str(int(score)), font_big, BLACK, 130, 250)
        draw_text(screen, 'PRESS SPACE TO PLAY AGAIN', font_big, BLACK, 40, 300)

        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            game_over = False
            score = 0
            player_x = WIDTH / 2 - (PLAYER_SCALE / 2)
            player_y = 400
            player.y_change = 0
            player.x_change = 0
            player.jump = True
            platforms = initial_platforms.copy()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            player.move_to_side(event)

        if event.type == pygame.KEYUP:
            player.key_check()

    pygame.display.flip()

pygame.quit()
