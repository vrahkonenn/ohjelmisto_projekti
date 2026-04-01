# main.py
import pygame
from saves import *
from settings import *
from player import Player
from platforms import PlatformManager
from slider import Slider
from ui import draw_text
from button import Button
from bullet import BulletManager
from camera import Camera
from background import Background
from pause import PauseScreen
from powerups import PowerUpManager
from monster import MonsterManager
import sound

pygame.init()
icon = pygame.image.load("Imgs/player.png")
pygame.display.set_icon(icon)

settings_screen_fade = pygame.Surface((WIDTH, HEIGHT))
settings_screen_fade.fill((0, 0, 0))
settings_screen_fade.set_alpha(50)

pause_screen = PauseScreen()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rise of The Bubblegum")

from powerups import PowerUp
PowerUp.load_images()

menu_bg = pygame.image.load("Imgs/mMenu_bg.png").convert()
gameover_bg_norm = pygame.image.load("Imgs/gameover_norm.png").convert()
coin_img = pygame.image.load("Imgs/kolikkokuva.png").convert_alpha()
coin_img = pygame.transform.scale(coin_img, (32, 32))

clock = pygame.time.Clock()

player = Player(13)
platforms = PlatformManager()
bullets = BulletManager()
camera = Camera()
background = Background()
menu_player = Player(9)
menu_player.y = 320
menu_player.jump = True
powerups = PowerUpManager()
birds = MonsterManager()

# napit
restart_button =    Button(WIDTH//2 - 100, HEIGHT//2+50, 200, 50,
                        "RESTART", font_big, GRAY, BLACK)
start_button =      Button(WIDTH//2 - 175, 250, 200, 50,
                        "START", font_big, GRAY, BLACK)
settings_button = Button(WIDTH//2 - 100, HEIGHT//2 + 20, 200, 50,
                        "SETTINGS", font_big, GRAY, BLACK)

sound_button = Button(WIDTH//2 - 100, HEIGHT//2 - 60, 200, 50,
                        "TOGGLE SOUND", font_big, GRAY, BLACK)
music_button = Button(WIDTH//2 - 100, HEIGHT//2 + 20, 200, 50,
                        "TOGGLE MUSIC", font_big, GRAY, BLACK)

# sliderit
sound_slider = Slider(WIDTH//2 - 100, HEIGHT//2 - 40, 200, 0.0, 1.0, 1.0)
music_slider = Slider(WIDTH//2 - 100, HEIGHT//2 + 20, 200, 0.0, 1.0, 1.0)

score = 0

# game states
GAME_MENU="menu"
GAME_PLAYING="playing"
GAME_OVER="game_over"
GAME_PAUSED="paused"
GAME_RESUME="resume"
GAME_SETTINGS="settings"

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
        camera.update(player)
        background.draw(screen, camera.scroll)

        player.animate()
        if platforms.coin is not None:
            platforms.coin.start_animation()
            platforms.coin.animate()
            platforms.coin.draw(screen)
            if player.get_collision_rect().colliderect(platforms.coin.get_collision_rect()):
                coins += 1
                platforms.coin = None

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
        bullets.update()
        bullets.draw(screen)
        powerups.update()
        powerups.draw(screen)
        birds.update(player, score)
        birds.draw(screen)

        korkeusvari=BLACK if score < 900 else WHITE

        draw_text_with_outline(screen, font_small, f"KORKEUS: {score:.2f}", (4, 8), PURKKA, TUMMA_PURKKA)

        coin_x = WIDTH - 70
        coin_y = 5

        # piirrä numero
        if total_coins + coins >= 1000:
            coin_padding = 40
        elif total_coins + coins >= 100:
            coin_padding = 25
        elif total_coins + coins >= 10:
            coin_padding = 9
        elif total_coins + coins >= 0:
            coin_padding = -10
        draw_text_with_outline(screen, font_big, f"{total_coins+coins}", (coin_x-coin_padding, coin_y+2), WHITE, BLACK)

        # piirrä kolikon kuva numeron jälkeen
        screen.blit(coin_img, (coin_x + 34, coin_y))
        
        if player.y > HEIGHT:
            game_state = GAME_OVER

    # peli pausella
    elif game_state == GAME_PAUSED:
        background.draw(screen, camera.scroll)
        platforms.draw(screen)
        player.draw(screen)
        bullets.draw(screen)

        pause_screen.draw(screen)
        settings_button.draw(screen)

    # settings-valikko
    elif game_state == GAME_SETTINGS:
        screen.blit(settings_screen_fade, (0, 0))
        draw_text(screen, "SETTINGS", font_large, WHITE, WIDTH//2, HEIGHT//2 - 140, center=True)
        draw_text(screen, "sound (sfx) volume:", font_big, WHITE, WIDTH//2, HEIGHT//2 - 60, center=True)
        draw_text(screen, "music volume:", font_big, WHITE, WIDTH//2, HEIGHT//2, center=True)
        draw_text(screen, "Paina ESC palataksesi", font_small, WHITE, WIDTH//2, HEIGHT//2 + 60, center=True)

        sound_slider.draw(screen)
        music_slider.draw(screen)

    # peli jatkuu
    elif game_state == GAME_RESUME:
        current_time = pygame.time.get_ticks()
        elapsed = current_time - resume_timer
        remaining = max(0, (resume_wait - elapsed) // 1000 + 1)

        background.draw(screen, camera.scroll)
        platforms.draw(screen)
        player.draw(screen)
        bullets.draw(screen)

        pause_screen.draw_countdown(screen, remaining)

        if elapsed >= resume_wait:
            game_state = GAME_PLAYING

    # game over
    elif game_state == GAME_OVER:
        screen.blit(gameover_bg_norm, (0, 0))
        text_surf = font_large.render(f"{highscore:.2f}", True, RED)
        text_rect = text_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 60))
        screen.blit(text_surf, text_rect)
        draw_text_with_outline(screen, font_big, f"SCORE: {score:.2f}", (WIDTH//2 - 80, HEIGHT//2 - 20), RED, ORANGE)
        #draw_text(screen, f"SCORE: {score:.2f}",
        #          font_big, BLACK, WIDTH//2 - 80, HEIGHT//2 - 20)
        restart_button.draw(screen)
        if score > highscore:
            data["highscore"] = score
        save(data, total_coins, coins)
        coins = 0
    
    if game_state != previous_state:
        if game_state not in (GAME_PAUSED, GAME_RESUME, GAME_SETTINGS):
            sound.play_music(game_state)
            pygame.mixer.music.set_volume(music_slider.get_value())
            #pygame.mixer.sound.set_volume(sound_slider.get_value())
        previous_state = game_state

    for event in pygame.event.get():
        
        if game_state == GAME_SETTINGS:
            music_slider.handle_event(event)
            sound_slider.handle_event(event)

        if event.type == pygame.QUIT:
            running = False
            save(data, total_coins, coins)
            coins = 0

        if event.type == pygame.KEYDOWN:
            if game_state == GAME_PLAYING:
                player.move_to_side(event.key)

            if event.key == pygame.K_SPACE and game_state == GAME_PLAYING:
                bullets.shoot(player)
                player.shoot_animation()

            if event.key == pygame.K_ESCAPE:
                if game_state == GAME_PLAYING:
                    game_state = GAME_PAUSED
                    sound.pause_music(game_state)

                elif game_state == GAME_PAUSED:
                    game_state = GAME_RESUME
                    resume_timer = pygame.time.get_ticks()
                    sound.unpause_music(game_state)

                elif game_state == GAME_SETTINGS:
                    game_state = GAME_PAUSED

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

            if game_state == GAME_PAUSED and settings_button.is_clicked(event.pos):
                game_state = GAME_SETTINGS
            if game_state == GAME_SETTINGS and sound_button.is_clicked(event.pos):
                sound.toggle_sound()
            if game_state == GAME_SETTINGS and music_button.is_clicked(event.pos):
                sound.toggle_music()

    pygame.display.flip()

pygame.quit()