import pygame
import random

from ten_drops import SCREEN, PLAYGROUND, BACKGROUND
from ten_drops.drop import Drop
from ten_drops.droplet import Droplet


class Game:
    def __init__(self):
        self.grid: list[list[None | Drop]] = [[None for _ in range(10)] for _ in range(10)]
        self.run = True
        self.all_droplets = []
        self.clock = pygame.time.Clock()

    def _init_grid(self):
        for row in range(10):
            for col in range(10):
                if random.random() < 0.3:
                    self.grid[row][col] = Drop(row, col)

    def start(self):
        self._init_grid()

        while self.run:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    col = mouse_x // (PLAYGROUND.get_width() // 10)
                    row = mouse_y // (PLAYGROUND.get_height() // 10)
                    if self.grid[row][col] is not None:
                        if self.grid[row][col].update():
                            self.all_droplets.extend(Droplet.diffusion(row, col))
                            self.grid[row][col] = None

            SCREEN.blits([
                (BACKGROUND, (0, 0)),
                (PLAYGROUND, (0, 0))
            ])

            for row in range(10):
                for col in range(10):
                    if self.grid[row][col] is not None:
                        self.grid[row][col].draw()

            for droplet in self.all_droplets[:]:
                new_droplet = droplet.move(self.grid, self.all_droplets)
                if new_droplet is not None:
                    new_droplet.draw()
                else:
                    self.all_droplets.remove(droplet)

            pygame.display.update()

            all_exploded = True
            for row in self.grid:
                for drop in row:
                    if drop is not None:
                        all_exploded = False
                        break
            if all_exploded:
                print("win!")
                self.run = False

        pygame.quit()
