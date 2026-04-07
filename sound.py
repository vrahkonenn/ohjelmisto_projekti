import pygame
import random

GAME_MENU="menu"
GAME_PLAYING="playing"
GAME_OVER="game_over"
GAME_PAUSED="paused"
GAME_RESUME="resume"

sound_on = True
music_on = True

sfx = {}

def play_music(state):
    if not music_on:
        return
    
    pygame.mixer.music.stop()
    if state == GAME_MENU:
        pygame.mixer.music.load("./music/Main_menu.wav")
    elif state == GAME_PLAYING:
        pygame.mixer.music.load("./music/Purkkapallo.wav")
    elif state == GAME_OVER:
        pygame.mixer.music.load("./music/game_over.wav")
    
    pygame.mixer.music.play(-1, 0.0)

def toggle_sound():
    global sound_on
    sound_on = not sound_on
    if not sound_on:
        pygame.mixer.music.set_volume(0)
    else:
        pygame.mixer.music.set_volume(1)

def toggle_music():
    global music_on
    music_on = not music_on
    if not music_on:
        pygame.mixer.music.set_volume(0)
    else:
        pygame.mixer.music.set_volume(1)

def pause_music(state):
    if state == GAME_PAUSED:
        pygame.mixer.music.pause()

def unpause_music(state):
    if state == GAME_RESUME:
        pygame.mixer.music.unpause()

def load_sfx():
    global sfx
    sfx = {
        "shoot": [pygame.mixer.Sound("sfx/Bop1.wav"),
                 pygame.mixer.Sound("sfx/Bop2.wav"),
                 pygame.mixer.Sound("sfx/Bop3.wav"),],
        "jump": [pygame.mixer.Sound("./sfx/hop1.wav"),
                pygame.mixer.Sound("./sfx/hop2.wav"),
                pygame.mixer.Sound("./sfx/hop3.wav"),],
        "click": pygame.mixer.Sound("./sfx/click.wav"),
        "buy": pygame.mixer.Sound("./sfx/buy.wav"),
        "game_over": pygame.mixer.Sound("./sfx/ded_norm.wav"),
        "pickup_coin": pygame.mixer.Sound("./sfx/pickupCoin.wav"),
        "umbrella": pygame.mixer.Sound("./sfx/chute.wav"),
    }
    for sounds in sfx.values():
        if isinstance(sounds, list):
            for sound in sounds:
                sound.set_volume(0.5)
        else:
            sounds.set_volume(0.8)

def toggle_sfx():
    global sound_on
    sound_on = not sound_on

def play_sfx(sound):
    if isinstance(sound, list):
        random.choice(sound).play()
    else:
        sound.play()

