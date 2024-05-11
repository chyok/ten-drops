import random
import pygame

from collections import namedtuple

from pygame import Rect
from pygame.sprite import Group

from ten_drops import SCREEN, PLAYGROUND, BACKGROUND, GRID_SIZE, PLAYGROUND_OFFSET, PLAYGROUND_LENGTH
from ten_drops.drop import Drop

Level = namedtuple("Level", "state0, state1, state2, state3")
Levels = [Level(2, 5, 8, 9),
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
                    row = random.randint(0, GRID_SIZE - 1)
                    col = random.randint(0, GRID_SIZE - 1)
                    if (row, col) not in used_positions:
                        used_positions.add((row, col))
                        self.drops.add(Drop(row, col, state))
                        break

    def start(self):
        mouse_hover_pos = (-1, -1)
        self._init_grid()

        while self.run:
            self.clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    row = (mouse_y - PLAYGROUND_OFFSET) // (PLAYGROUND_LENGTH // GRID_SIZE)
                    col = (mouse_x - PLAYGROUND_OFFSET) // (PLAYGROUND_LENGTH // GRID_SIZE)

                    for i in self.drops:
                        if i.row == row and i.col == col and len(self.droplets) == 0:
                            i.click()

                if event.type == pygame.MOUSEMOTION:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    row = (mouse_y - PLAYGROUND_OFFSET) // (PLAYGROUND_LENGTH // GRID_SIZE)
                    col = (mouse_x - PLAYGROUND_OFFSET) // (PLAYGROUND_LENGTH // GRID_SIZE)
                    for i in self.drops:
                        if i.row == row and i.col == col and (row, col) != mouse_hover_pos:
                            i.mouse_hover()
                    mouse_hover_pos = (row, col)

            SCREEN.blit(BACKGROUND, (0, 0))

            SCREEN.blit(PLAYGROUND, (PLAYGROUND_OFFSET, PLAYGROUND_OFFSET),
                        Rect(PLAYGROUND_OFFSET, PLAYGROUND_OFFSET,
                             PLAYGROUND_LENGTH, PLAYGROUND_LENGTH))

            pygame.draw.lines(SCREEN, (255, 255, 255), True, [
                (PLAYGROUND_OFFSET, PLAYGROUND_OFFSET),
                (PLAYGROUND_OFFSET, PLAYGROUND_LENGTH + PLAYGROUND_OFFSET),
                (PLAYGROUND_LENGTH + PLAYGROUND_OFFSET, PLAYGROUND_LENGTH + PLAYGROUND_OFFSET),
                (PLAYGROUND_LENGTH + PLAYGROUND_OFFSET, PLAYGROUND_OFFSET),
            ], 1)

            self.drops.update(self.drops, self.droplets)

            self.drops.draw(SCREEN)

            self.droplets.update(self.drops, self.droplets)

            pygame.display.update()

            all_exploded = False

            if len(self.drops) <= 0:
                all_exploded = True

            if all_exploded and len(self.droplets) == 0:
                print("win!")
                self.level += 1
                self._init_grid()

        pygame.quit()
