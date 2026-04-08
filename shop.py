from settings import *
from button import Button
import saves

class Shop:
    def __init__(self):
       
        self.jumpboost_button = Button(WIDTH//2 - 175, 20, 200, 50, "JUMPBOOST", font_big, VAALEAN_RUSKEA, TUMMAN_RUSKEA)
        self.jetpack_button = Button(WIDTH//2 - 175, 80, 200, 50, "JETPACK", font_big, VAALEAN_RUSKEA, TUMMAN_RUSKEA)
        self.shoe_button = Button(WIDTH//2 - 175, 140, 200, 50, "SHOE", font_big, VAALEAN_RUSKEA, TUMMAN_RUSKEA)
        self.umbrella_button = Button(WIDTH//2 - 175, 200, 200, 50, "UMBRELLA", font_big, VAALEAN_RUSKEA, TUMMAN_RUSKEA)

        self.limit = 4    
        self.cost = 10

    def draw_shop(self, screen):
        self.jumpboost_button.draw(screen)
        self.jetpack_button.draw(screen)
        self.shoe_button.draw(screen)
        self.umbrella_button.draw(screen) 
        draw_text_with_outline(screen, font_big, f"Upgrades cost {self.cost} coins.", (8, 260), WHITE, BLACK)
        draw_text_with_outline(screen, font_big, f"They increase spawn rate.", (8, 290), WHITE, BLACK)

    def transaction(self, data, button):
        if data["currency"] >= self.cost:
            if data[button]<self.limit:
                data["currency"] -= self.cost
                data[button] += 1
                saves.save(data, data["currency"])
                
                
            
           
        