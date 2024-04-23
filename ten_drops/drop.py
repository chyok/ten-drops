import pygame
from ten_drops import WINDOW

COLORS = [(0, 0, 255), (0, 255, 0), (255, 0, 0), (255, 255, 0)]


class Drop:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.state = 0
        self.color = COLORS[self.state]
        self.radius = 10

    def draw(self):
        x = self.col * 40 + 20
        y = self.row * 40 + 20
        pygame.draw.circle(WINDOW, self.color, (x, y), self.radius)

    def update(self):
        self.state = self.state + 1
        if self.state >= len(COLORS):
            self.color = None
            self.radius = 0
            return True
        else:
            self.color = COLORS[self.state]
            self.radius = 10 + self.state * 5
        return False
