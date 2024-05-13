import random
import time

import pygame

from collections import namedtuple

from pygame import Rect
from pygame.sprite import Group, groupcollide

from ten_drops import SCREEN, PLAYGROUND, BACKGROUND, GRID_SIZE, PLAYGROUND_OFFSET, PLAYGROUND_LENGTH, FONT_PATH
from ten_drops.drop import Drop
from ten_drops.droplet import Droplet
from ten_drops.panel import Title, Level, Score, HP
from ten_drops.button import Start, About, Exit

LevelDesign = namedtuple("LevelDesign", "state0, state1, state2, state3")
Levels = [LevelDesign(2, 5, 8, 9),
          LevelDesign(2, 5, 8, 8)]


class Game:
    def __init__(self):
        self.start_game = False
        self.run = True

        self.drops: Group = Group()
        self.droplets: Group = Group()
        self.panel: Group = Group()
        self.buttons: Group = Group()

        self.clock = pygame.time.Clock()
        self.level = 1
        self.score = 0
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
                        Drop(row, col, state, self.drops)
                        break

    def _init_button(self):
        Start(self.buttons)
        About(self.buttons)
        Exit(self.buttons)

    def _init_panel(self):
        self.panel.empty()
        Level(self.level, self.panel)
        Score(self.score, self.panel)
        HP(self.hp, self.panel)

    def start(self):
        last_hover_rect = Rect(0, 0, 0, 0)
        self._init_grid()
        self._init_button()

        while self.run:
            self.clock.tick(30)

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self.run = False
                    break

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    for i in self.drops:
                        if i.rect.collidepoint(mouse_x, mouse_y) and len(self.droplets) == 0:
                            i.click()
                            self.hp = self.hp - 1
                            if i.need_diffuse:
                                Droplet.diffusion(i.row, i.col, self.droplets)

                    for i in self.buttons:
                        if i.rect.collidepoint(mouse_x, mouse_y):
                            if isinstance(i, Start):
                                self.start_game = True
                            elif isinstance(i, About):
                                self.start_game = False
                            elif isinstance(i, Exit):
                                self.run = False
                                break

                if event.type == pygame.MOUSEMOTION:
                    mouse_x, mouse_y = pygame.mouse.get_pos()

                    if not last_hover_rect.collidepoint(mouse_x, mouse_y):
                        last_hover_rect = Rect(0, 0, 0, 0)

                    for i in self.drops:
                        if i.rect.collidepoint(mouse_x, mouse_y) and not last_hover_rect.collidepoint(mouse_x,
                                                                                                      mouse_y):
                            i.mouse_hover()
                            last_hover_rect = i.rect
                            break

                    for i in self.buttons:
                        if i.rect.collidepoint(mouse_x, mouse_y):
                            i.mouse_hover()
                        else:
                            i.mouse_leave()

            SCREEN.blit(BACKGROUND, (0, 0))
            self.buttons.draw(SCREEN)

            if not self.start_game:
                pygame.display.update()
                continue

            self._init_panel()

            SCREEN.blit(PLAYGROUND, (PLAYGROUND_OFFSET, PLAYGROUND_OFFSET),
                        Rect(PLAYGROUND_OFFSET, PLAYGROUND_OFFSET,
                             PLAYGROUND_LENGTH, PLAYGROUND_LENGTH))

            pygame.draw.lines(SCREEN, (255, 255, 255), True, [
                (PLAYGROUND_OFFSET, PLAYGROUND_OFFSET),
                (PLAYGROUND_OFFSET, PLAYGROUND_LENGTH + PLAYGROUND_OFFSET),
                (PLAYGROUND_LENGTH + PLAYGROUND_OFFSET, PLAYGROUND_LENGTH + PLAYGROUND_OFFSET),
                (PLAYGROUND_LENGTH + PLAYGROUND_OFFSET, PLAYGROUND_OFFSET),
            ], 1)

            self.drops.update()
            self.droplets.update()

            self.drops.draw(SCREEN)
            self.droplets.draw(SCREEN)
            self.panel.draw(SCREEN)

            for drop, droplets in groupcollide(self.drops, self.droplets, dokilla=False, dokillb=False).items():
                drop.hit()

                droplets[0].kill()  # many droplets hit same drop, only delete one

                if drop.need_diffuse:
                    Droplet.diffusion(drop.row, drop.col, self.droplets)

            pygame.display.update()

            if len(self.drops) <= 0 and len(self.droplets) == 0:
                print("win!")
                self.level += 1
                self._init_grid()

        pygame.quit()
