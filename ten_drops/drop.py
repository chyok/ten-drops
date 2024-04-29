from pygame.sprite import Sprite

from ten_drops import SCREEN, PLAYGROUND, DROP_IMAGES


class Drop(Sprite):
    def __init__(self, row, col, *groups):
        Sprite.__init__(self, *groups)
        self.row = row
        self.col = col
        self.state = 0
        self.radius = 10

    def draw(self):
        stable_image = DROP_IMAGES[self.state].stable
        rect = stable_image.get_rect()
        rect.x = self.col * (PLAYGROUND.get_height() // 10) + (PLAYGROUND.get_height() // 10 // 2) - rect.width // 2
        rect.y = self.row * (PLAYGROUND.get_width() // 10) + (PLAYGROUND.get_width() // 10 // 2) - rect.height // 2

        SCREEN.blit(stable_image, rect)

    def update(self):
        self.state = self.state + 1
        if self.state >= len(DROP_IMAGES):
            self.radius = 0
            return True
        else:
            self.radius = (PLAYGROUND.get_width() // 10 // 2 // 2) + self.state * 5
        return False
