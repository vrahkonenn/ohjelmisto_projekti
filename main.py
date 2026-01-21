import pygame

pygame.init()

WIDTH  = 400
HEIGHT = 500

FPS = 60

timer = pygame.time.Clock()

background = (255,255,255)

screen = pygame.display.set_mode([WIDTH, HEIGHT])

running = True
while running == True:
    timer.tick(FPS)
    screen.fill(background)
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
pygame.quit()