import pygame
from ten_drops import WINDOW

BLUE = (0, 0, 255)


class Direction:
    Down = (1, 0)
    Up = (-1, 0)
    Left = (0, -1)
    Right = (0, 1)


class Droplet:
    def __init__(self, row, col, direction, speed):
        self.row = row
        self.col = col
        self.direction = direction
        self.speed = speed
        self.color = BLUE
        self.radius = 5

    def draw(self):
        x = self.col * 40 + 20
        y = self.row * 40 + 20
        pygame.draw.circle(WINDOW, self.color, (x, y), self.radius)

    def move(self, grid):
        self.row += self.direction[0] * self.speed
        self.col += self.direction[1] * self.speed
        if self.row < 0 or self.row >= 10 or self.col < 0 or self.col >= 10:
            return None
        if ele := grid[int(self.row)][int(self.col)] is not None:
            if ele.update():
                grid[int(self.row)][int(self.col)] = None
            return None
        return self
