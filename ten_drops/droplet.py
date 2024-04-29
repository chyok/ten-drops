import math
import pygame

from ten_drops import SCREEN
from ten_drops import PLAYGROUND


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
        self.color = (0, 0, 255)
        self.radius = 5

    def draw(self):
        x = self.col * (PLAYGROUND.get_height() // 10) + (PLAYGROUND.get_height() // 10 // 2)
        y = self.row * (PLAYGROUND.get_width() // 10) + (PLAYGROUND.get_width() // 10 // 2)
        pygame.draw.circle(SCREEN, self.color, (x, y), self.radius)

    def move(self, grid, droplets: list):
        self.row += self.direction[0] * self.speed
        self.col += self.direction[1] * self.speed
        if self.row < 0 or self.row >= 10 or self.col < 0 or self.col >= 10:
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
