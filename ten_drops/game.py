import pygame
import random

from collections import namedtuple
from pygame.sprite import Group

from ten_drops import SCREEN, PLAYGROUND, BACKGROUND
from ten_drops.drop import Drop

Level = namedtuple("Level", "state0, state1, state2, state3")
Levels = [Level(2, 5, 8, 10),
          Level(2, 5, 8, 8)]


class Game:
    def __init__(self):
        self.drops: Group = Group()
        self.run = True
        self.droplets: Group = Group()
        self.clock = pygame.time.Clock()
        self.level = 1
        self.hp = 10

    def _init_grid(self):
        used_positions = set()

        for state, count in enumerate(Levels[self.level - 1]):
            for _ in range(count):
                while True:
                    row = random.randint(0, 9)
                    col = random.randint(0, 9)
                    if (row, col) not in used_positions:
                        used_positions.add((row, col))
                        self.drops.add(Drop(row, col, state))
                        break

    def start(self):
        self._init_grid()
        mouse_hover_pos = (-1, -1)

        while self.run:
            self.clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()

                    row = mouse_y // (PLAYGROUND.get_height() // 10)
                    col = mouse_x // (PLAYGROUND.get_width() // 10)

                    for i in self.drops:
                        if i.row == row and i.col == col:
                            i.click()

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

            self.drops.update(self.drops, self.droplets)

            self.drops.draw(SCREEN)

            self.droplets.update(self.drops, self.droplets)

            pygame.display.update()

            all_exploded = False

            if len(self.drops) <= 0:
                all_exploded = True

            if all_exploded:
                print("win!")
                self.run = False

        pygame.quit()
