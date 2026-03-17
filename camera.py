from settings import HEIGHT

class Camera:
    def __init__(self):
        self.scroll = 0

    def update(self, player):
        if player.y <= 200 and player.y_change < 0:
            self.scroll += -player.y_change*0.25
    
    def reset(self):
        self.scroll = 0