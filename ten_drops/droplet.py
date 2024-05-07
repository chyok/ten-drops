import math

from pygame.transform import rotate
from ten_drops import SCREEN
from ten_drops import PLAYGROUND
from ten_drops import DROPLET_IMAGES


class Direction:
    Down = (1, 0)
    Up = (-1, 0)
    Left = (0, -1)
    Right = (0, 1)


class Droplet:
    def __init__(self, row, col, direction):
        self.row = row
        self.col = col
        self.direction = direction
        self.speed = 0.02
        self.radius = 5

    def draw(self):
        stable_image = DROPLET_IMAGES[0].stable
        if self.direction == Direction.Up:
            stable_image = rotate(stable_image, 90)
        elif self.direction == Direction.Left:
            stable_image = rotate(stable_image, 90 * 2)
        elif self.direction == Direction.Down:
            stable_image = rotate(stable_image, 90 * 3)
        rect = stable_image.get_rect()

        rect.x = self.col * (PLAYGROUND.get_height() // 10) + (PLAYGROUND.get_height() // 10 // 2) - rect.width // 2
        rect.y = self.row * (PLAYGROUND.get_width() // 10) + (PLAYGROUND.get_width() // 10 // 2) - rect.height // 2

        SCREEN.blit(stable_image, rect)

    def move(self, grid, droplets: list):
        self.row += self.direction[0] * self.speed
        self.col += self.direction[1] * self.speed
        if self.row < 0 or self.row > 10 or self.col < 0 or self.col > 10:
            return None
        if self.direction in (Direction.Up, Direction.Left):
            row, col = math.ceil(self.row), math.ceil(self.col)
        else:
            row, col = math.floor(self.row), math.floor(self.col)

        if (ele := grid[row][col]) is not None:
            if ele.update():
                grid[row][col] = None
                droplets.extend(Droplet.diffusion(row, col))
            return None
        return self

    @classmethod
    def diffusion(cls, row, col) -> list["Droplet"]:
        droplets = []
        for direction in [Direction.Down, Direction.Up, Direction.Left, Direction.Right]:
            droplets.append(Droplet(row, col, direction))
        return droplets
