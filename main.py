import pygame
import random
import spritesheet

pygame.init()

WIDTH  = 400
HEIGHT = 500

FPS = 60

white = (255, 255, 255)
black = (0, 0, 0)
gray = (128, 128, 128)

timer = pygame.time.Clock()

background = white

# Alustojen min ja max väli
MIN_PLATFORM_GAP = 60
MAX_PLATFORM_GAP = 100
#Min korkeusväli alustojen välillä
MIN_PLATFORM_SEPARATION = 40
# sivusuuntainen raja, että pelaaja ylettää
HORIZ_REACH = 120

screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("TEMP_Hyppypeli_TEMP")

player_scale= 90
player = pygame.image.load("Imgs/frame1 (9).png").convert_alpha()

###sprite
sprite_sheet = spritesheet.SpriteSheet(player)

animation_list = []
animating = False
animation_steps = 6
animation_cooldown = 75
last_update = pygame.time.get_ticks()
frame = 0

for x in range(animation_steps):
    animation_list.append(
        sprite_sheet.get_image(x, 80, 80, 1, (0,0,0))
    )
###

#pygame.transform.scale(, (90, 70))
player_x = WIDTH/2 - (player_scale/2)
player_y = 400
player_spd = 3

# Platform [x, y, width, height, type]
platforms = [[175, 480, 70 , 10, 0],
             [85 , 370, 70 , 10, 1],
             [265, 370, 70 , 10, 0],
             [175, 260, 70 , 10, 0],
             [85 , 150, 70 , 10, 1],
             [265, 150, 70 , 10, 0],
             [175, 40 , 70 , 10, 0]]
jump = False
y_change = 0
x_change = 0
score = 0

#Liikkumis koodi
def move_to_side():
    if event.key == pygame.K_a or event.key == pygame.K_LEFT:
        x_change = -player_spd
    if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
        x_change = player_spd
    return x_change    

#Näppäimen pohjassa pito
def key_check():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] == True:
        x_change = -player_spd
    if keys[pygame.K_RIGHT] == True:
        x_change = player_spd
    if sum(keys) == 0:
        x_change = 0
    return x_change

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

def check_collisions(rect_list):
    global player_x
    global player_y
    global y_change
    global platforms 
    
    for i in range(len(rect_list)):
        if rect_list[i].colliderect([player_x + 20, player_y + 60, 35, 5]) and y_change > 0:
            
            # Normaali alusta
            if platforms[i][4] == 0:
                return True
            
            # Hajoava
            if platforms[i][4] == 1:
                platforms[i][4] = 2
                return True
            
            if platforms[i][4] == 3:
                return False
    return False

def updatePlatforms(my_list, y_pos, y_change):
    for i in range(len(my_list)):
        if my_list[i][4] == 2:  # jos rikki
            my_list[i][1] += 8  # putoamisnopeus

    global score
    if y_pos < 250 and y_change < 0:
        for i in range(len(my_list)):
            my_list[i][1] -= y_change
            score += 0.05
    else:
        pass
    for item in range(len(my_list)):
        if my_list[item][1] > 510:
            # Alustojen spawnaus mahdollisuus (0 = normaali, 1 = hajoava, 3 = ansa)
            # Spawnaa uusi alusta oikealle välille (ei liian lähellä tai kaukana muista alustoista)
            highest_y = min(p[1] for p in my_list)
            spawn_x = random.randint(10, 300)
            gap = random.randint(MIN_PLATFORM_GAP, MAX_PLATFORM_GAP)
            spawn_y = highest_y - gap
            # varmista ettei uusi alusta ole liian lähellä olemassa olevaa alustaa
            tries = 0
            placed = False
            spawn_y = highest_y - random.randint(MIN_PLATFORM_GAP, MAX_PLATFORM_GAP)
            while tries < 10 and not placed:
                spawn_y = highest_y - random.randint(MIN_PLATFORM_GAP, MAX_PLATFORM_GAP)
                if not any(abs(spawn_y - p[1]) < MIN_PLATFORM_SEPARATION for p in my_list):
                    placed = True
                    break
                tries += 1
            if not placed:
                # fallback: max sallittu väli (pitää hypyt mahdollisina)
                spawn_y = highest_y - MAX_PLATFORM_GAP
            platform_type = random.choices([0,1,3], weights=[75,20,5])[0]
            # Älä spawnaa ansa-alustaa liian lähelle pelaajan nykyistä pystysuuntaista sijaintia
            if platform_type == 3 and abs(y_pos - spawn_y) < 120:
                # fallback normaaliin tai hajoavaan alustaan
                platform_type = random.choices([0,1], weights=[80,20])[0]
            # Varmista että väh. 1 ei ansa alusta on mahdollista saavuttaa
            # varsinkin kun pelaaja on ruudun alalaidassa (ei "boostia
            # alaspäin liikkuvista alustoista")
            reachable_top = y_pos - 200
            reachable_bottom = y_pos + 100
            player_center = player_x + (player_scale / 2)
            def horiz_dist(a, b):
                d = abs(a - b)
                return min(d, WIDTH - d)
            has_non_trap = any(
                p[4] != 3
                and reachable_top <= p[1] <= reachable_bottom
                and horiz_dist(p[0] + (p[2] / 2), player_center) <= HORIZ_REACH
                for p in my_list
            )
            if not has_non_trap and platform_type == 3:
                platform_type = random.choices([0,1], weights=[80,20])[0]
            my_list[item] = [spawn_x, spawn_y, 70, 10, platform_type]
    return my_list

#platform grafiikat
platform_images = {
    0: pygame.image.load("Imgs/normal.png").convert_alpha(),
    1: pygame.image.load("Imgs/breakable.png").convert_alpha(),
    2: pygame.image.load("Imgs/broken.png").convert_alpha(),
    3: pygame.image.load("Imgs/trap.png").convert_alpha()
}

running = True
while running == True:
    timer.tick(FPS)
    screen.fill(background)
    screen.blit(animation_list[frame], (player_x, player_y))
    blocks = []

    ##sprite
    current_time = pygame.time.get_ticks()
    if animating:
        current_time = pygame.time.get_ticks()
        if current_time - last_update >= animation_cooldown:
            frame += 1
            last_update = current_time

            if frame >= len(animation_list):
                frame = len(animation_list) - 1
                animating = False  # pysähdy viimeiseen frameen
    ##

    # Alustojen grafiikat (normaali, harmaa rikki menevä, ansa)
    for i in range(len(platforms)):
        platform_type = platforms[i][4]
        image = platform_images[platform_type]

        screen.blit(image, (platforms[i][0], platforms[i][1]))

        block = pygame.Rect(platforms[i][0], platforms[i][1], platforms[i][2], platforms[i][3])
        blocks.append(block)

    # Nappi tapahtumat
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            x_change = move_to_side()
        if event.type == pygame.KEYUP:
            x_change = key_check()         

    player_x += x_change
    #Rajat
    if player_x > 400 and x_change>0:
        player_x = -25
    if player_x < 0 and x_change<0:
        player_x = 375
    player_y = update_player(player_y)
    jump = check_collisions(blocks)

    ##sprite
    if jump and not animating:
        animating = True
        frame = 0
        last_update = pygame.time.get_ticks()
    ##

    platforms = updatePlatforms(platforms, player_y, y_change)
    print(score) #score testi
    pygame.display.flip()
    #if player_y > HEIGHT + 50:
    #    running = False
pygame.quit()