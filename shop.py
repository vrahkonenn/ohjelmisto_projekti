from settings import *
from button import Button
import saves

class Shop:
    def __init__(self):
        self.jumpboost = 0
        self.jetpack = 0
        self.shoes = 0
        self.umbrella = 0

        self.jumpboost_button = Button(WIDTH//2 - 175, 20, 200, 50, "JUMPBOOST", font_big, GRAY, BLACK)
        self.jetpack_button = Button(WIDTH//2 - 175, 80, 200, 50, "JETPACK", font_big, GRAY, BLACK)
        self.shoe_button = Button(WIDTH//2 - 175, 140, 200, 50, "SHOE", font_big, GRAY, BLACK)
        self.umbrella_button = Button(WIDTH//2 - 175, 200, 200, 50, "UBMBRELLA", font_big, GRAY, BLACK)

        self.limit = 4    
        self.cost = 10

    def draw_shop(self, screen):
        self.jumpboost_button.draw(screen)
        self.jetpack_button.draw(screen)
        self.shoe_button.draw(screen)
        self.umbrella_button.draw(screen) 
    
    def transaction(self, data, button):
        if data["currency"] >= self.cost:
            if data[button]<self.limit:
                data["currency"] -= self.cost
                data[button] += 1
                saves.save(data, data["currency"])
                
                
            
           
        