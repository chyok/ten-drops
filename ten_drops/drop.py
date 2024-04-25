from ten_drops import Screen
from ten_drops.asset import DropImage
from pygame.sprite import Sprite


class Drop(Sprite):
    def __init__(self, row, col, *groups):
        Sprite.__init__(self, *groups)
        self.row = row
        self.col = col
        self.state = 0
        self.radius = 10

    def draw(self):
        image = DropImage[self.state].stable
        rect = image.get_rect()
        rect.x = self.col * (Screen.get_height() // 10) + (Screen.get_height() // 10 // 2) - rect.width // 2
        rect.y = self.row * (Screen.get_width() // 10) + (Screen.get_width() // 10 // 2) - rect.height // 2

        Screen.blit(image, rect)

    def update(self):
        self.state = self.state + 1
        if self.state >= len(DropImage):
            self.radius = 0
            return True
        else:
            self.radius = (Screen.get_width() // 10 // 2 // 2) + self.state * 5
        return False
