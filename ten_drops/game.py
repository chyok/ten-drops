import pygame
import random

from pygame.sprite import Group

from ten_drops import SCREEN, PLAYGROUND, BACKGROUND
from ten_drops.drop import Drop
from ten_drops.droplet import Droplet


class Game:
    def __init__(self):
        self.grid: list[list[None | Drop]] = [[None for _ in range(10)] for _ in range(10)]
        self.drops: Group = Group()
        self.run = True
        self.all_droplets = []
        self.clock = pygame.time.Clock()

    def _init_grid(self):
        for row in range(10):
            for col in range(10):
                if random.random() < 0.3:
                    self.drops.add(Drop(row, col))

    def start(self):
        self._init_grid()
        mouse_hover_pos = (-1, -1)

        while self.run:
            self.clock.tick(20)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()

                    row = mouse_y // (PLAYGROUND.get_height() // 10)
                    col = mouse_x // (PLAYGROUND.get_width() // 10)

                    for i in self.drops:
                        if i.row == row and i.col == col:
                            if i.click():
                                self.all_droplets.extend(Droplet.diffusion(row, col))
                                self.drops.remove(i)

                if event.type == pygame.MOUSEMOTION:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    col = mouse_x // (PLAYGROUND.get_width() // 10)
                    row = mouse_y // (PLAYGROUND.get_height() // 10)
                    for i in self.drops:
                        if i.row == row and i.col == col and (row, col) != mouse_hover_pos:
                            i.mouse_hover()
                    mouse_hover_pos = (row, col)

            SCREEN.blits([
                (BACKGROUND, (0, 0)),
                (PLAYGROUND, (0, 0))
            ])

            self.drops.update()

            self.drops.draw(SCREEN)

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
                pass
                # print("win!")
                # self.run = False

        pygame.quit()
