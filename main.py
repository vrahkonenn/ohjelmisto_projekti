import pygame
import random

pygame.init()

WIDTH  = 400
HEIGHT = 500

FPS = 60

white = (255, 255, 255)
black = (0, 0, 0)
gray = (128, 128, 128)

timer = pygame.time.Clock()

background = white

screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("TEMP_Hyppypeli_TEMP")

player_scale= 90
player = pygame.transform.scale(pygame.image.load("Imgs\player.png"), (player_scale, player_scale))
#pygame.transform.scale(, (90, 70))
player_x = WIDTH/2 - (player_scale/2)
player_y = 400
player_spd = 3

platforms = [[175, 480, 70 , 10],
             [85 , 370, 70 , 10],
             [265, 370, 70 , 10],
             [175, 260, 70 , 10],
             [85 , 150, 70 , 10],
             [265, 150, 70 , 10],
             [175, 40 , 70 , 10]]
jump = False
y_change = 0
x_change = 0

def update_player(y_pos):
    global jump
    global y_change
    gravity = .4
    jump_height = 10
    if jump:
        y_change = -jump_height
        jump = False
    y_pos += y_change
    y_change += gravity
    return y_pos

def check_collisions(rect_list, j):
    global player_x
    global player_y
    global y_change
    for i in range(len(rect_list)):
        if rect_list[i].colliderect([player_x + 20, player_y + 60, 35, 5]) and jump == False and y_change > 0:
            j = True
    return j

def updatePlatforms(my_list, y_pos, y_change):
    if y_pos < 250 and y_change < 0:
        for i in range(len(my_list)):
            my_list[i][1] -= y_change
    else:
        pass
    for item in range(len(my_list)):
        if my_list[item][1] > 500:
            my_list[item] = [random.randint(10, 300), random.randint(-50, -10), 70, 10]
    return my_list


running = True
while running == True:
    timer.tick(FPS)
    screen.fill(background)
    screen.blit(player, (player_x, player_y))
    blocks = []

    for i in range(len(platforms)):
        block = pygame.draw.rect(screen, black, platforms[i], 0, 3)
        blocks.append(block)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                x_change = -player_spd
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                x_change = player_spd
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                x_change = 0
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                x_change = 0

    player_x += x_change
    player_y = update_player(player_y)
    jump = check_collisions(blocks, jump)

    platforms = updatePlatforms(platforms, player_y, y_change)

    pygame.display.flip()
    if player_y > HEIGHT + 50:
        running = False
pygame.quit()