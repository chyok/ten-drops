import pygame
from ten_drops import Screen

BLUE = (0, 0, 255)


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
        self.color = BLUE
        self.radius = 5

    def draw(self):
        x = self.col * (Screen.get_height() // 10) + (Screen.get_height() // 10 // 2)
        y = self.row * (Screen.get_width() // 10) + (Screen.get_width() // 10 // 2)
        pygame.draw.circle(Screen, self.color, (x, y), self.radius)

    def move(self, grid, droplets: list):
        self.row += self.direction[0] * self.speed
        self.col += self.direction[1] * self.speed
        if self.row < 0 or self.row >= 10 or self.col < 0 or self.col >= 10:
            return None
        row, col = int(self.row), int(self.col)
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
