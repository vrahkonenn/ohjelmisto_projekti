from settings import *
from button import Button
import sound
import saves

class Shop:
    def __init__(self):
       
        #Left buttons
        self.jumpboost_button = Button(WIDTH//2 - 190, 60, 175, 50, "JUMPBOOST", font_big, VAALEAN_RUSKEA, TUMMAN_RUSKEA)
        self.jetpack_button = Button(WIDTH//2 - 190, 120, 175, 50, "JETPACK", font_big, VAALEAN_RUSKEA, TUMMAN_RUSKEA)
        self.shoe_button = Button(WIDTH//2 - 190, 180, 175, 50, "SHOE", font_big, VAALEAN_RUSKEA, TUMMAN_RUSKEA)
        self.umbrella_button = Button(WIDTH//2 - 190, 240, 175, 50, "UMBRELLA", font_big, VAALEAN_RUSKEA, TUMMAN_RUSKEA)

        #Right buttons
        self.jumpboost_button_r = Button(WIDTH - 185, 60, 175, 50, "JUMPBOOST", font_big, VAALEAN_RUSKEA, TUMMAN_RUSKEA)
        self.jetpack_button_r = Button(WIDTH - 185, 120, 175, 50, "JETPACK", font_big, VAALEAN_RUSKEA, TUMMAN_RUSKEA)
        self.shoe_button_r = Button(WIDTH - 185, 180, 175, 50, "SHOE", font_big, VAALEAN_RUSKEA, TUMMAN_RUSKEA)
        self.umbrella_button_r = Button(WIDTH - 185, 240, 175, 50, "UMBRELLA", font_big, VAALEAN_RUSKEA, TUMMAN_RUSKEA)

        self.limit = 4    
        self.cost = 10

    def draw_shop(self, screen):
        #Left buttons
        self.jumpboost_button.draw(screen)
        self.jetpack_button.draw(screen)
        self.shoe_button.draw(screen)
        self.umbrella_button.draw(screen) 

        #Right buttons
        self.jumpboost_button_r.draw(screen)
        self.jetpack_button_r.draw(screen)
        self.shoe_button_r.draw(screen)
        self.umbrella_button_r.draw(screen)
        
        draw_text_with_outline(screen, font_big, f"Spawn %", (WIDTH//2 - 170, 300), WHITE, BLACK)
        draw_text_with_outline(screen, font_big, f"Power", (WIDTH - 170, 300), WHITE, BLACK)

        draw_text_with_outline(screen, font_big, f"Upgrades cost {self.cost} coins.", (8, 330), WHITE, BLACK)

    def transaction(self, data, button, value):
        if data["currency"] >= self.cost:
            if data[button][1] < self.limit:
                sound.play_sfx(sound.sfx["buy"])
                data["currency"] -= self.cost
                data[button][1] += 1
                data[button][0] += value
                saves.save(data, data["currency"])
                
                
            
           
        