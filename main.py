# main.py
import pygame
from saves import *
from settings import *
from player import Player
from platforms import PlatformManager
from slider import Slider
from ui import draw_text
from ui import draw_text_outline
from button import Button
from bullet import BulletManager
from camera import Camera
from background import Background
from pause import PauseScreen
from powerups import PowerUpManager
from shop import Shop
from monster import MonsterManager
import sound
from spacemonster import SpaceMonsterManager

pygame.init()
icon = pygame.image.load("Imgs/player.png")
pygame.display.set_icon(icon)

settings_screen_fade = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
settings_screen_fade.fill((0, 0, 0, 80))

pause_screen = PauseScreen()

settings_screen = pygame.Surface((WIDTH, HEIGHT))
settings_screen.fill(BLACK)
settings_screen.set_alpha(50)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rise of The Bubblegum")

from powerups import PowerUp
PowerUp.load_images()

menu_bg = pygame.image.load("Imgs/mMenu_bg_new.png").convert()
shop_bg = pygame.image.load("Imgs/ground_new.png").convert()
gameover_bg_norm = pygame.image.load("Imgs/gameover_norm_new.png").convert()
gameover_bg_bitten = pygame.image.load("Imgs/gameover_purtu_new.png").convert()
coin_img = pygame.image.load("Imgs/kolikkokuva.png").convert_alpha()
coin_img = pygame.transform.scale(coin_img, (32, 32))
guide_bg = pygame.image.load("Imgs/guide_bg_new.png").convert()

clock = pygame.time.Clock()

player = Player(13)
platforms = PlatformManager()
bullets = BulletManager()
camera = Camera()
background = Background()
menu_player = Player(9)
menu_player.y = 470
menu_player.jump = True
powerups = PowerUpManager()
shop = Shop()
birds = MonsterManager()
aliens = SpaceMonsterManager()

# napit
restart_button =    Button(WIDTH//2 - 100, HEIGHT//2+50, 200, 50,
                        "RESTART", font_big, GRAY, BLACK)
start_button =      Button(WIDTH//2 - 175, 350, 200, 85,
                        "START", font_big, VAALEAN_PINKKI, KERMA, TUMMAN_PINKKI )
shop_button =    Button(WIDTH//2 - 175, 435, 200, 50,
                        "SHOP", font_big, VAALEAN_RUSKEA, TUMMAN_RUSKEA, TUMMAN_RUSKEA)
menu_button =    Button(WIDTH//2 - 175, HEIGHT-75, 200, 50,
                        "MENU", font_big, GRAY, BLACK)
restart_menu_button =    Button(WIDTH//2 - 100, HEIGHT-75, 200, 50,
                        "MENU", font_big, GRAY, BLACK)
settings_button = Button(WIDTH//2 - 100, HEIGHT//2 + 20, 200, 50,
                        "SETTINGS", font_big, GRAY, BLACK)
pause_menu_button = Button(WIDTH//2 - 100, HEIGHT//2 + 80, 200, 50,
                        "MENU", font_big, GRAY, BLACK)
sound_button = Button(WIDTH//2 - 100, HEIGHT//2 - 60, 200, 50,
                        "TOGGLE SOUND", font_big, GRAY, BLACK)
music_button = Button(WIDTH//2 - 100, HEIGHT//2 + 20, 200, 50,
                        "TOGGLE MUSIC", font_big, GRAY, BLACK)
guide_button = Button(WIDTH//2 - 175, HEIGHT-145, 200, 50,
                        "GUIDE", font_big, GRAY, BLACK)
guide_menu_button =    Button(WIDTH//2 - 175, HEIGHT - 75, 200, 50,
                        "MENU", font_big, GRAY, BLACK)
reset_button = Button(WIDTH//2 - 150, HEIGHT//2 + 100, 300, 50,
                        "RESET PROGRESS", font_big, RED, WHITE)
yes_button = Button(WIDTH//2 - 110, HEIGHT//2 + 50, 100, 50,
                        "YES", font_big, GRAY, BLACK)
no_button = Button(WIDTH//2 + 10, HEIGHT//2 + 50, 100, 50,
                        "NO", font_big, GRAY, BLACK)
quit_button = Button(WIDTH//2 - 175, HEIGHT - 75, 200, 50,
                        "QUIT", font_big, GRAY, BLACK)

# sfx
sound.load_sfx()

# sliderit
sound_slider = Slider(WIDTH//2 - 100, HEIGHT//2 - 40, 200, 0.0, 1.0, 0.8)
music_slider = Slider(WIDTH//2 - 100, HEIGHT//2 + 20, 200, 0.0, 1.0, 1.0)
sound_slider = Slider(WIDTH//2 - 100, HEIGHT//2 - 40, 200, 0.0, 1.0, 0.8)
music_slider = Slider(WIDTH//2 - 100, HEIGHT//2 + 20, 200, 0.0, 1.0, 1.0)

score = 0
last_updated_score = 0

# game states
GAME_MENU="menu"
GAME_PLAYING="playing"
GAME_OVER="game_over"
GAME_PAUSED="paused"
GAME_RESUME="resume"
GAME_SHOP="shop"
GAME_SETTINGS="settings"
HOW_TO_PLAY = "guide"
GAME_RESET = "reset"

game_state=GAME_MENU
previous_state = None
running = True
coins = 0
data = get_data()
coin_x = WIDTH - 70
coin_y = 5

sound.play_music(game_state)
sound.pause_music()
sound.unpause_music()

def draw_game(screen):
    background.draw(screen, camera.scroll)
    platforms.draw(screen)
    player.draw(screen)
    bullets.draw(screen)
    powerups.draw(screen)
    birds.draw(screen)
    aliens.draw(screen)

def reset_game():
    global score, last_updated_score, game_state
    player.reset()
    platforms.reset()
    platforms.reset_difficulty()
    camera.reset()
    powerups.reset()
    birds.reset()
    aliens.reset()
    score = 0
    last_updated_score = 0
    game_state = GAME_PLAYING

while running:
    clock.tick(FPS)
    highscore = data["highscore"]
    total_coins = data["currency"]  
    jumpboost = data["jumpboost"]
    jumpboost_str = data["jumpboost_str"]
    jetpack = data["jetpack"]
    jetpack_dur = data["jetpack_dur"]
    shoes = data["shoes"]
    extra_jumps = data["extra_jumps"]
    umbrella = data["umbrella"]
    umbrella_dur = data["umbrella_dur"]

    # Päävalikko
    if game_state == GAME_MENU:
        screen.blit(menu_bg, (0, 0))
        menu_player.update()
        menu_player.animate()
        menu_player.x = 270

        if menu_player.y > 520:
            menu_player.jump = True
            menu_player.start_animation()

        menu_player.draw(screen)
        shop_button.draw(screen)
        start_button.draw_image(screen)
        guide_button.draw(screen)
        quit_button.draw(screen)


    # Peli käynnissä
    if game_state == GAME_PLAYING:
        screen.fill(WHITE)
        player.update()
        camera.update(player)
        background.draw(screen, camera.scroll)

        player.animate()

        score += platforms.update(player)

        if score - 100 >= last_updated_score:
            last_updated_score = score
            platforms.update_difficulty()

        player.jump = platforms.check_collisions(player)

        if player.jump:
            sound.play_sfx(sound.sfx["jump"])
            player.start_animation()

        # spawnataan powerupeja platformeille
        for p in platforms.platforms:
            if hasattr(p, "has_powerup") is False:
                powerups.spawn_on_platform(p)

        power = powerups.check_collision(player)

        if power == "jumpboost":
            player.y_change = -20 - jumpboost_str[0]

        if power == "jetpack":
            player.jetpack_active = True
            player.jetpack_timer = pygame.time.get_ticks()

        if power == "shoes":
            player.shoes_charges = 5 + extra_jumps[0]

        if power == "umbrella":
            player.umbrella_active = True
            player.umbrella_timer = pygame.time.get_ticks()

        draw_game(screen)

        if platforms.coin is not None:
            platforms.coin.start_animation()
            platforms.coin.animate()
            platforms.coin.draw(screen)
            if player.get_collision_rect().colliderect(platforms.coin.get_collision_rect()):
                sound.play_sfx(sound.sfx["pickup_coin"])
                coins += 1
                platforms.coin = None

        bullets.update()
        powerups.update()
        birds.update(player, score)
        aliens.update(player, score)
        
        coins += birds.coins_earned + aliens.coins_earned + bullets.coins_earned 
        bullets.coins_earned = 0
        birds.coins_earned = 0
        aliens.coins_earned = 0

        bullets.check_hits(birds.monsters)
        bullets.check_hits(aliens.monsters)

        if birds.check_player_collision(player) or aliens.check_player_collision(player):
            if player.is_immune == False:
                player.death_source = "monster"
                game_state = GAME_OVER
                sound.play_sfx(sound.sfx["game_over"])

        korkeusvari=BLACK if score < 900 else WHITE

        draw_text_with_outline(screen, font_small, f"KORKEUS: {score:.2f}", (4, 8), PURKKA, TUMMA_PURKKA)

        

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
            player.death_source = "falling"
            game_state = GAME_OVER
            sound.play_sfx(sound.sfx["game_over"])

    # peli pausella
    elif game_state == GAME_PAUSED:
        draw_game(screen)
        
        screen.blit(settings_screen_fade, (0, 0))
        

        pause_screen.draw(screen)
        settings_button.draw(screen)
        pause_menu_button.draw(screen)

    # settings-valikko
    elif game_state == GAME_SETTINGS:
        screen.fill(BLACK)
        draw_text(screen, "SETTINGS", font_large, WHITE, WIDTH//2, HEIGHT//2 - 140, center=True)
        draw_text(screen, "sound (sfx): on/off", font_big, WHITE, WIDTH//2, HEIGHT//2 - 60, center=True)
        draw_text(screen, "music: on/off", font_big, WHITE, WIDTH//2, HEIGHT//2, center=True)
        draw_text(screen, "Paina ESC palataksesi", font_small, WHITE, WIDTH//2, HEIGHT//2 + 60, center=True)

        sound_slider.draw(screen)
        music_slider.draw(screen)

        reset_button.draw(screen)

    # peli jatkuu
    elif game_state == GAME_RESUME:
        current_time = pygame.time.get_ticks()
        elapsed = current_time - resume_timer
        remaining = max(0, (resume_wait - elapsed) // 1000 + 1)

        draw_game(screen)

        pause_screen.draw_countdown(screen, remaining)

        if elapsed >= resume_wait:
            game_state = GAME_PLAYING

    # game over
    elif game_state == GAME_OVER:
        if player.death_source == "monster":
            screen.blit(gameover_bg_bitten, (0,0))
        else:
            screen.blit(gameover_bg_norm, (0, 0))

        text_surf = font_large.render(f"{highscore:.2f}", True, RED)
        text_rect = text_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 60))
        screen.blit(text_surf, text_rect)
        draw_text_with_outline(screen, font_big, f"SCORE: {score:.2f}", (WIDTH//2 - 80, HEIGHT//2 - 20), RED, ORANGE)
        #draw_text(screen, f"SCORE: {score:.2f}",
        #          font_big, BLACK, WIDTH//2 - 80, HEIGHT//2 - 20)
        restart_button.draw(screen)
        restart_menu_button.draw(screen)
        if score > highscore:
            data["highscore"] = score
        currency = total_coins + coins
        save(data, currency)
        coins = 0

    # game reset
    elif game_state == GAME_RESET:
        screen.fill(BLACK)
        draw_text_outline(screen, "Are you sure?", font_large, RED, WIDTH//2, HEIGHT//2 - 20, center=True, outline_col=WHITE)
        draw_text_outline(screen, "This will reset all your progress!", font_small, GRAY, WIDTH//2, HEIGHT//2 + 20, center=True, outline_col=BLACK)
        yes_button.draw(screen)
        no_button.draw(screen)

    # Shopping
    elif game_state == GAME_SHOP:
        screen.blit(shop_bg, (0, 0))
        menu_button.draw(screen)
        shop.draw_shop(screen)
        
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
        screen.blit(coin_img, (coin_x + 34, coin_y))
     
             #Left
        draw_text_with_outline(screen, font_small, f"{jumpboost[1]}/{shop.limit}", (10 + 175//2 , coin_y + 48), WHITE, BLACK)
        draw_text_with_outline(screen, font_small, f"{jetpack[1]}/{shop.limit}", (10 + 175//2 , coin_y + 108), WHITE, BLACK)
        draw_text_with_outline(screen, font_small, f"{shoes[1]}/{shop.limit}", (10 + 175//2 , coin_y + 168), WHITE, BLACK)
        draw_text_with_outline(screen, font_small, f"{umbrella[1]}/{shop.limit}", (10 + 175//2 , coin_y + 228), WHITE, BLACK)

        #Right
        draw_text_with_outline(screen, font_small, f"{jumpboost_str[1]}/{shop.limit}", (10 +WIDTH//2 + 175//2, coin_y + 48), WHITE, BLACK)
        draw_text_with_outline(screen, font_small, f"{jetpack_dur[1]}/{shop.limit}", (10 + WIDTH//2 + 175//2, coin_y + 108), WHITE, BLACK)
        draw_text_with_outline(screen, font_small, f"{extra_jumps[1]}/{shop.limit}", (10 +WIDTH//2 + 175//2, coin_y + 168), WHITE, BLACK)
        draw_text_with_outline(screen, font_small, f"{umbrella_dur[1]}/{shop.limit}", (10 +WIDTH//2 + 175//2, coin_y + 228), WHITE, BLACK)

    elif game_state == HOW_TO_PLAY:
        screen.blit(guide_bg, (0, 0))
        guide_menu_button.draw(screen)

    if game_state != previous_state:
        if not (previous_state == GAME_RESUME and game_state == GAME_PLAYING):
            if game_state in (GAME_MENU, GAME_PLAYING, GAME_OVER):
                sound.play_music(game_state)

        pygame.mixer.music.set_volume(music_slider.get_value())

        for s in sound.sfx.values():
            if isinstance(s, list):
                for sound_effect in s:
                    sound_effect.set_volume(sound_slider.get_value())
            else:
                s.set_volume(sound_slider.get_value())

        previous_state = game_state

    # eventit
    for event in pygame.event.get():
        
        if game_state == GAME_SETTINGS:
            music_slider.handle_event(event)
            sound_slider.handle_event(event)

        if event.type == pygame.QUIT:
            running = False
            currency = total_coins + coins
            save(data, currency)
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
                    sound.pause_music()

                elif game_state == GAME_PAUSED:
                    game_state = GAME_RESUME
                    resume_timer = pygame.time.get_ticks()
                    sound.unpause_music()

                elif game_state == GAME_SETTINGS:
                    game_state = GAME_PAUSED

            if game_state == GAME_OVER and event.key == pygame.K_SPACE  or game_state == GAME_MENU and event.key == pygame.K_SPACE:
                reset_game()

        if event.type == pygame.KEYUP:
            if game_state == GAME_PLAYING:
                player.key_check()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if game_state == GAME_MENU:
                if start_button.is_clicked(event.pos):
                    reset_game()
                elif shop_button.is_clicked(event.pos):
                    game_state = GAME_SHOP
                elif guide_button.is_clicked(event.pos):
                    game_state = HOW_TO_PLAY
                elif quit_button.is_clicked(event.pos):
                    running = False
            elif game_state == HOW_TO_PLAY:
                if guide_menu_button.is_clicked(event.pos):
                    data = get_data()
                    game_state = GAME_MENU

            if game_state == GAME_SHOP:
                currency = total_coins + coins
                save(data, currency)
                coins = 0
                if menu_button.is_clicked(event.pos):
                    game_state = GAME_MENU
                    player = Player(13)
                # Left side
                elif shop.jumpboost_button.is_clicked(event.pos):
                    shop.transaction(data, "jumpboost", 0.5)
                    powerups.update_spawn_chances()
                elif shop.jetpack_button.is_clicked(event.pos):
                    shop.transaction(data, "jetpack", 0.5)
                    powerups.update_spawn_chances()
                elif shop.shoe_button.is_clicked(event.pos):
                    shop.transaction(data, "shoes", 0.5)
                    powerups.update_spawn_chances()
                elif shop.umbrella_button.is_clicked(event.pos):
                    shop.transaction(data, "umbrella", 0.5)
                    powerups.update_spawn_chances()
                # Right side
                elif shop.jumpboost_button_r.is_clicked(event.pos):
                    shop.transaction(data, "jumpboost_str", 2)
                    powerups.update_spawn_chances()
                elif shop.jetpack_button_r.is_clicked(event.pos):
                    shop.transaction(data, "jetpack_dur", 250)
                    powerups.update_spawn_chances()
                elif shop.shoe_button_r.is_clicked(event.pos):
                    shop.transaction(data, "extra_jumps", 1)
                    powerups.update_spawn_chances()
                elif shop.umbrella_button_r.is_clicked(event.pos):
                    shop.transaction(data, "umbrella_dur", 250)
                    powerups.update_spawn_chances()
                
                else:
                    pass

            if game_state == GAME_OVER and restart_button.is_clicked(event.pos):
                reset_game()

            if game_state == GAME_OVER and restart_menu_button.is_clicked(event.pos):
                game_state = GAME_MENU

            if game_state == GAME_PAUSED and settings_button.is_clicked(event.pos):
                game_state = GAME_SETTINGS
            if game_state == GAME_PAUSED and pause_menu_button.is_clicked(event.pos):
                game_state = GAME_MENU
            if game_state == GAME_SETTINGS:
                if not (sound_slider._handle_rect().collidepoint(event.pos) or 
                        music_slider._handle_rect().collidepoint(event.pos)):
                    if sound_button.is_clicked(event.pos):
                        sound.toggle_sound()
                    elif music_button.is_clicked(event.pos):
                        sound.toggle_music()

            
            if game_state == GAME_SETTINGS and reset_button.is_clicked(event.pos) and event.type == pygame.MOUSEBUTTONDOWN:
                game_state = GAME_RESET

            if game_state == GAME_RESET:
                if yes_button.is_clicked(event.pos) and event.type == pygame.MOUSEBUTTONDOWN:
                    data = reset_data()
                    game_state = GAME_MENU
                elif no_button.is_clicked(event.pos) and event.type == pygame.MOUSEBUTTONDOWN:
                    game_state = GAME_MENU

    pygame.display.flip()

pygame.quit()