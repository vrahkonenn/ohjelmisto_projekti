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
from coin import Coin
from pause import PauseScreen
from powerups import PowerUpManager
import sound

pygame.init()
icon = pygame.image.load("Imgs/player.png")
pygame.display.set_icon(icon)

pause_screen = PauseScreen()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rise of The Bubblegum")

menu_bg = pygame.image.load("Imgs/mMenu_bg.png").convert()
gameover_bg_norm = pygame.image.load("Imgs/gameover_norm.png").convert()

clock = pygame.time.Clock()

coin = Coin(80, 200)
player = Player(13)
platforms = PlatformManager()
bullets = BulletManager()
camera = Camera()
background = Background()
menu_player = Player(9)
menu_player.y = 320
menu_player.jump = True
powerups = PowerUpManager()

restart_button =    Button(WIDTH//2 - 100, HEIGHT//2+50, 200, 50,
                        "RESTART", font_big, GRAY, BLACK)
start_button =      Button(WIDTH//2 - 175, 250, 200, 50,
                        "START", font_big, GRAY, BLACK)


score = 0

# game states
GAME_MENU="menu"
GAME_PLAYING="playing"
GAME_OVER="game_over"
GAME_PAUSED="paused"
GAME_RESUME="resume"

game_state=GAME_MENU
previous_state = None
running = True
coins = 0
data = get_data()

sound.play_music(game_state)


while running:
    clock.tick(FPS)
    highscore = data["highscore"]
    total_coins = data["currency"]  
    # Päävalikko
    if game_state == GAME_MENU:
        screen.blit(menu_bg, (0, 0))
        menu_player.update()
        menu_player.animate()
        menu_player.x = 270

        if menu_player.y > 370:
            menu_player.jump = True
            menu_player.start_animation()

        menu_player.draw(screen)
        
        start_button.draw(screen)

    # Peli käynnissä
    if game_state == GAME_PLAYING:
        screen.fill(WHITE)
        player.update()
        coin.start_animation()
        camera.update(player)
        background.draw(screen, camera.scroll)

        player.animate()
        coin.animate()

        score += platforms.update(player)

        # spawnataan powerupeja platformeille
        for p in platforms.platforms:
            if hasattr(p, "has_powerup") is False:
                powerups.spawn_on_platform(p)
                p.has_powerup = True

        player.jump = platforms.check_collisions(player)

        if player.jump:
            player.start_animation()

        power = powerups.check_collision(player)

        if power == "jumpboost":
            player.y_change = -20

        if power == "jetpack":
            player.jetpack_active = True
            player.jetpack_timer = pygame.time.get_ticks()

        if power == "shoes":
            player.shoes_charges = 5

        if power == "umbrella":
            player.umbrella_active = True
            player.umbrella_timer = pygame.time.get_ticks()

        platforms.draw(screen)
        player.draw(screen)
        coin.draw(screen)
        bullets.update()
        bullets.draw(screen)
        powerups.update()
        powerups.draw(screen)

        korkeusvari=BLACK if score < 900 else WHITE

        draw_text(screen, f"Korkeus: {score:.2f}",
                  font_small, korkeusvari, 0, 0)

        if player.y > HEIGHT:
            game_state = GAME_OVER

    # peli pausella
    elif game_state == GAME_PAUSED:
        background.draw(screen, camera.scroll)
        platforms.draw(screen)
        player.draw(screen)
        bullets.draw(screen)
        coin.draw(screen)

        pause_screen.draw(screen)

    # peli jatkuu
    elif game_state == GAME_RESUME:
        current_time = pygame.time.get_ticks()
        elapsed = current_time - resume_timer
        remaining = max(0, (resume_wait - elapsed) // 1000 + 1)

        background.draw(screen, camera.scroll)
        platforms.draw(screen)
        player.draw(screen)
        bullets.draw(screen)
        coin.draw(screen)

        pause_screen.draw_countdown(screen, remaining)

        if elapsed >= resume_wait:
            game_state = GAME_PLAYING

    # game over
    elif game_state == GAME_OVER:
        screen.blit(gameover_bg_norm, (0, 0))
        text_surf = font_large.render(f"{highscore:.2f}", True, BLACK)
        text_rect = text_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 60))
        screen.blit(text_surf, text_rect)
        draw_text(screen, f"SCORE: {score:.2f}",
                  font_big, BLACK, WIDTH//2 - 80, HEIGHT//2 - 20)
        restart_button.draw(screen)
        if score > highscore:
            data["highscore"] = score
        save(data, total_coins, coins)
    
    if game_state != previous_state:
        sound.play_music(game_state)
        previous_state = game_state

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if game_state == GAME_PLAYING:
                player.move_to_side(event.key)

            if event.key == pygame.K_SPACE and game_state == GAME_PLAYING:
                bullets.shoot(player)
                player.shoot_animation()

            if event.key == pygame.K_ESCAPE:
                if game_state == GAME_PLAYING:
                    game_state = GAME_PAUSED

                elif game_state == GAME_PAUSED:
                    game_state = GAME_RESUME
                    resume_timer = pygame.time.get_ticks()

            if game_state == GAME_OVER and event.key == pygame.K_SPACE  or game_state == GAME_MENU and event.key == pygame.K_SPACE:
                player.reset()
                platforms.reset()
                camera.reset()
                powerups.reset()
                score = 0
                game_state = GAME_PLAYING

        if event.type == pygame.KEYUP:
            if game_state == GAME_PLAYING:
                player.key_check()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_state == GAME_MENU and start_button.is_clicked(event.pos):
                player.reset()
                platforms.reset()
                camera.reset()
                powerups.reset()
                score = 0
                game_state = GAME_PLAYING

            if game_state == GAME_OVER and restart_button.is_clicked(event.pos):
                player.reset()
                platforms.reset()
                camera.reset()
                powerups.reset()
                score = 0
                game_state = GAME_PLAYING

    pygame.display.flip()

pygame.quit()