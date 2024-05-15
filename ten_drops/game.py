import random
from collections import namedtuple

import pygame
from pygame import Rect
from pygame.sprite import Group, groupcollide

from ten_drops import SCREEN, PLAYGROUND, BACKGROUND, GRID_SIZE, PLAYGROUND_OFFSET, PLAYGROUND_LENGTH, NOTIFICATION
from ten_drops.button import StartButton, AboutButton, ExitButton
from ten_drops.cover import Cover
from ten_drops.drop import Drop
from ten_drops.droplet import Droplet
from ten_drops.notification import Notification, NotificationType
from ten_drops.panel import Level, Score, HP

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
        self.notifications: Group = Group()

        self.cover = Cover()

        self.clock = pygame.time.Clock()
        self.level = 1
        self.score = 0
        self.hp = 10

        self.combo = 1

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
        StartButton(self.buttons)
        AboutButton(self.buttons)
        ExitButton(self.buttons)

    def _init_panel(self):
        Level(self.level, self.panel)
        Score(self.score, self.panel)
        HP(self.hp, self.panel)

    def _init_notification(self):
        Notification(NotificationType.about, self.notifications)

    def start(self):
        self._init_grid()
        self._init_button()
        self._init_panel()
        self._init_notification()

        last_hover_rect = Rect(0, 0, 0, 0)

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
                            self.combo = 1
                            i.click()
                            self.hp = self.hp - 1
                            if i.need_diffuse:
                                self.score += 10
                                Droplet.diffusion(i.row, i.col, self.droplets)

                    for i in self.buttons:
                        if i.rect.collidepoint(mouse_x, mouse_y):
                            if isinstance(i, StartButton):
                                self.level = 1
                                self.start_game = True
                            elif isinstance(i, AboutButton):
                                self.start_game = False
                            elif isinstance(i, ExitButton):
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
            self.notifications.update()
            self.buttons.draw(SCREEN)

            if not self.start_game:
                self.cover.draw()
                pygame.display.update()
                continue

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
            self.panel.update(self)

            self.drops.draw(SCREEN)
            self.droplets.draw(SCREEN)
            self.panel.draw(SCREEN)
            self.notifications.draw(SCREEN)

            for drop, droplets in groupcollide(self.drops, self.droplets, dokilla=False, dokillb=False).items():
                drop.hit()

                droplets[0].kill()  # many droplets hit same drop, only delete one

                if drop.need_diffuse:
                    self.score += 10
                    self.combo += 1
                    if self.combo in (3, 6, 9, 11, 13, 15, 17, 19, 21):
                        self.hp += 1
                    elif self.combo > 21:
                        self.hp += 1
                    Droplet.diffusion(drop.row, drop.col, self.droplets)

            pygame.display.update()

            if len(self.drops) <= 0 and len(self.droplets) == 0:
                self.level += 1
                self.hp += 2
                self._init_grid()

        pygame.quit()
