# main.py
import pygame
from saves import *
from settings import *
from player import Player
from platforms import PlatformManager
from ui import draw_text
from button import Button
from bullet import BulletManager
from camera import Camera
from background import Background

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TEMP_Hyppypeli_TEMP")

clock = pygame.time.Clock()

player = Player()
platforms = PlatformManager()
bullets = BulletManager()
camera = Camera()
background = Background()
menu_player = Player()
menu_player.y = 250
menu_player.jump = True

restart_button =    Button(WIDTH//2 - 100, HEIGHT//2+50, 200, 50,
                        "RESTART", font_big, GRAY, BLACK)
start_button =      Button(WIDTH//2 - 100, 70, 200, 50,
                        "START", font_big, GRAY, BLACK)


score = 0

# game states
GAME_MENU="menu"
GAME_PLAYING="playing"
GAME_OVER="game_over"

game_state=GAME_MENU
running = True
coins = 0
data = get_data()
highscore = data["highscore"]
total_coins = data["currency"]  

while running:
    clock.tick(FPS)

    # Päävalikko
    if game_state == GAME_MENU:
        screen.fill(WHITE)
        menu_player.update()
        menu_player.animate()

        if menu_player.y > 300:
            menu_player.jump = True

        menu_player.draw(screen)

        draw_text(screen, "HYPPYPELI", font_big, BLACK,
                  WIDTH//2 - 120, 20)
        
        start_button.draw(screen)

    # Peli käynnissä
    if game_state == GAME_PLAYING:
        screen.fill(WHITE)
        player.update()

        camera.update(player)
        background.draw(screen, camera.scroll)

        player.animate()

        score += platforms.update(player)

        player.jump = platforms.check_collisions(player)

        if player.jump:
            player.start_animation()

        platforms.draw(screen)
        player.draw(screen)
        bullets.update()
        bullets.draw(screen)

        draw_text(screen, f"Korkeus: {score:.2f}",
                  font_small, BLACK, 0, 0)

        if player.y > HEIGHT:
            game_state = GAME_OVER

    # game over
    elif game_state == GAME_OVER:
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
            if game_state == GAME_PLAYING:
                player.move_to_side(event.key)

            if event.key == pygame.K_SPACE and game_state == GAME_PLAYING:
                bullets.shoot(player)
                player.shoot_animation()

            if game_state == GAME_OVER and event.key == pygame.K_SPACE:
                player.reset()
                platforms.reset()
                camera.reset()
                score = 0
                game_state = GAME_PLAYING

        if event.type == pygame.KEYUP:
            if game_state == GAME_PLAYING:
                player.key_check()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_state == GAME_MENU and start_button.is_clicked(event.pos):
                player.reset()
                platforms.reset()
                score = 0
                game_state = GAME_PLAYING

            if game_state == GAME_OVER and restart_button.is_clicked(event.pos):
                player.reset()
                platforms.reset()
                score = 0
                game_state = GAME_PLAYING

    pygame.display.flip()

pygame.quit()