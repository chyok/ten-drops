import math

from pygame.sprite import Group, Sprite
from pygame.transform import rotate

from ten_drops import DROPLET_IMAGES
from ten_drops import PLAYGROUND
from ten_drops import SCREEN


class Direction:
    Down = (1, 0)
    Up = (-1, 0)
    Left = (0, -1)
    Right = (0, 1)


class Droplet(Sprite):
    def __init__(self, row, col, direction, *groups):
        super().__init__(*groups)
        self.row = row
        self.col = col
        self.direction = direction
        self.speed = 0.05
        self.radius = 5

    def draw(self):
        image = DROPLET_IMAGES[0].static
        if self.direction == Direction.Up:
            image = rotate(image, 90)
        elif self.direction == Direction.Left:
            image = rotate(image, 90 * 2)
        elif self.direction == Direction.Down:
            image = rotate(image, 90 * 3)
        rect = image.get_rect()

        rect.x = self.col * (PLAYGROUND.get_height() // 10) + (PLAYGROUND.get_height() // 10 // 2) - rect.width // 2
        rect.y = self.row * (PLAYGROUND.get_width() // 10) + (PLAYGROUND.get_width() // 10 // 2) - rect.height // 2

        SCREEN.blit(image, rect)

    def update(self, drops: Group, droplets: Group):
        self.row += self.direction[0] * self.speed
        self.col += self.direction[1] * self.speed
        if self.row < 0 or self.row > 10 or self.col < 0 or self.col > 10:
            droplets.remove(self)
            return
        if self.direction in (Direction.Up, Direction.Left):
            row, col = math.ceil(self.row), math.ceil(self.col)
        else:
            row, col = math.floor(self.row), math.floor(self.col)

        for i in drops:
            if i.row == row and i.col == col:
                i.hit()
                droplets.remove(self)
                return

        self.draw()

    @classmethod
    def diffusion(cls, row, col) -> list["Droplet"]:
        droplets = []
        for direction in [Direction.Down, Direction.Up, Direction.Left, Direction.Right]:
            droplets.append(Droplet(row, col, direction))
        return droplets
