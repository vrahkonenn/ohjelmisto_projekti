import pygame

GAME_MENU="menu"
GAME_PLAYING="playing"
GAME_OVER="game_over"
GAME_PAUSED="paused"
GAME_RESUME="resume"

def play_music(state):
    pygame.mixer.music.stop()
    if state == GAME_MENU:
        pygame.mixer.music.load("./music/Main_menu.wav")
    elif state == GAME_PLAYING:
        pygame.mixer.music.load("./music/Purkkapallo.wav")
    elif state == GAME_OVER:
        pygame.mixer.music.load("./music/game_over.wav")
    
    pygame.mixer.music.play(-1, 0.0)

def pause_music(state):
    if state == GAME_PAUSED:
        pygame.mixer.music.pause()

def unpause_music(state):
    if state == GAME_RESUME:
        pygame.mixer.music.unpause