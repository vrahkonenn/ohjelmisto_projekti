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

current_track = None

def play_music(state):
    global current_track

    if not music_on:
        return

    track = None

    if state == GAME_MENU:
        track = "./music/Main_menu.wav"
    elif state == GAME_PLAYING:
        track = "./music/Purkkapallo.wav"
    elif state == GAME_OVER:
        track = "./music/game_over.wav"

    # jos sama älä tee mitään
    if track == current_track:
        return

    current_track = track

    pygame.mixer.music.load(track)
    pygame.mixer.music.play(-1)

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

def pause_music():
    pygame.mixer.music.pause()

def unpause_music():
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
        "jetpack": pygame.mixer.Sound("./sfx/jetpack_3s.wav"),
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

jetpack_channel = None
def jetpack_playing():
    sfx["jetpack"].play(loops=-1)

def stop_jetpack():
    sfx["jetpack"].stop()