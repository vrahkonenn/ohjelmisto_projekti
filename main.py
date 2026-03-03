# main.py
import pygame
from saves import *
from settings import *
from player import Player
from platforms import PlatformManager
from ui import draw_text
from button import Button

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TEMP_Hyppypeli_TEMP")

clock = pygame.time.Clock()

player = Player()
platforms = PlatformManager()

restart_button = Button(WIDTH//2 - 100, HEIGHT//2+50, 200, 50,
                        "RESTART", font_big, GRAY, BLACK)

score = 0
game_over = False
running = True
coins = 0
data = get_data()
highscore = data["highscore"]
total_coins = data["currency"]  

while running:
    clock.tick(FPS)

    if not game_over:
        screen.fill(WHITE)

        player.update()
        player.animate()

        score += platforms.update(player)

        player.jump = platforms.check_collisions(player)

        if player.jump:
            player.start_animation()

        platforms.draw(screen)
        player.draw(screen)

        draw_text(screen, f"Korkeus: {score:.2f}",
                  font_small, BLACK, 0, 0)

        if player.y > HEIGHT:
            game_over = True

    else:
        screen.fill(WHITE)
        draw_text(screen, "GAME OVER", font_big, BLACK,
                  WIDTH//2 - 80, HEIGHT//2 - 60)
        draw_text(screen, f"SCORE: {score:.2f}",
                  font_big, BLACK, WIDTH//2 - 80, HEIGHT//2 - 20)
        restart_button.draw(screen)
        if score > highscore:
            data["highscore"] = score
        save(data, total_coins, coins)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            player.move_to_side(event.key)

            if game_over and event.key == pygame.K_SPACE:
                player.reset()
                platforms.reset()
                score = 0
                game_over = False

        if event.type == pygame.KEYUP:
            player.key_check()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_over and restart_button.is_clicked(event.pos):
                player.reset()
                platforms.reset()
                score = 0
                game_over = False

    pygame.display.flip()

pygame.quit()