import random
import pygame

from collections import namedtuple
from pygame.sprite import Group, groupcollide, GroupSingle

from ten_drops import (
    SCREEN,
    PLAYGROUND,
    BACKGROUND,
    GRID_SIZE,
    PLAYGROUND_OFFSET,
    PLAYGROUND_LENGTH,
    HP_SOUND,
    GROW_SOUND,
)
from ten_drops.button import StartButton, AboutButton, ExitButton
from ten_drops.cover import Cover
from ten_drops.drop import Drop, DummyDrop
from ten_drops.droplet import Droplet
from ten_drops.notification import Notice, NoticeType
from ten_drops.panel import Level, Score, HP

LevelDesign = namedtuple("LevelDesign", "state0, state1, state2, state3")
Levels = [
    LevelDesign(2, 5, 8, 9),
    LevelDesign(2, 6, 7, 8),
    LevelDesign(3, 7, 7, 7),
    LevelDesign(3, 7, 6, 6),
    LevelDesign(4, 7, 6, 5),
    LevelDesign(4, 8, 6, 5),
    LevelDesign(4, 8, 5, 5),
    LevelDesign(5, 9, 3, 5),
    LevelDesign(6, 9, 4, 5),
]


class Game:
    level: int
    score: int
    hp: int
    combo: int

    def __init__(self):
        self.start_game = False
        self.run = True

        self.drops: Group = Group()
        self.dummy_drops: Group = Group()
        self.droplets: Group = Group()
        self.panel: Group = Group()
        self.buttons: Group = Group()
        self.notifications: GroupSingle = GroupSingle()

        self.cover = Cover()

        self.clock = pygame.time.Clock()

    def _init_game_data(self):
        self.level = 1
        self.score = 0
        self.hp = 10
        self.combo = 1

    def _init_grid(self):
        used_positions = set()

        if self.level - 1 >= len(Levels):
            level = Levels[random.randint(-5, -1)]
        else:
            level = Levels[self.level - 1]

        for state, count in enumerate(level):
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

    def _init_dummy_drops(self):
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                DummyDrop(i, j, self.dummy_drops)

    def notify(self, _type):
        if _type == NoticeType.success:
            text = "     Well Done!\n     + 2 drops\n\n     Next Level"
        elif _type == NoticeType.failed:
            text = f"You Lost\nYour Score: {self.score}"
        else:
            text = (
                "The game and water drop assets are \n"
                'from the Flash game "Splash Back".\n'
                "\n\n\nAuthor: chyok\n"
                "Email : chyok@hotmail.com\nGithub: https://github.com/chyok\n"
                "\nImplemented using pygame-ce."
            )

        Notice(_type, text, self.notifications)

    def start(self):
        self._init_game_data()
        self._init_button()
        self._init_panel()
        self._init_dummy_drops()

        last_hover_rect = pygame.Rect(0, 0, 0, 0)

        while self.run:
            self.clock.tick(30)

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self.run = False
                    break

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if len(self.notifications) > 0:
                        self.notifications.empty()
                        continue

                    for i in self.drops:
                        if (
                            i.rect.collidepoint(mouse_x, mouse_y)
                            and len(self.droplets) == 0
                        ):
                            self.combo = 1
                            i.click()
                            self.hp = self.hp - 1
                            if i.need_diffuse:
                                self.score += 10
                                Droplet.diffusion(i.row, i.col, self.droplets)

                    if len(self.droplets) == 0 and self.start_game:
                        for j in self.dummy_drops:
                            if j.rect.collidepoint(mouse_x, mouse_y):
                                if (j.row, j.col) not in (
                                    (i.row, i.col) for i in self.drops
                                ):
                                    GROW_SOUND.play()
                                    Drop(j.row, j.col, 0, self.drops)
                                    self.hp -= 1
                                break

                    for i in self.buttons:
                        if i.rect.collidepoint(mouse_x, mouse_y):
                            if isinstance(i, StartButton):
                                self.drops.empty()
                                self.droplets.empty()
                                self._init_game_data()
                                self._init_grid()
                                self.start_game = True
                            elif isinstance(i, AboutButton):
                                self.notify(NoticeType.about)
                            elif isinstance(i, ExitButton):
                                self.run = False
                                break

                if event.type == pygame.MOUSEMOTION:
                    mouse_x, mouse_y = pygame.mouse.get_pos()

                    if not last_hover_rect.collidepoint(mouse_x, mouse_y):
                        last_hover_rect = pygame.Rect(0, 0, 0, 0)

                    for i in self.drops:
                        if i.rect.collidepoint(
                            mouse_x, mouse_y
                        ) and not last_hover_rect.collidepoint(mouse_x, mouse_y):
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
            self.notifications.update()

            if not self.start_game:
                self.cover.draw()
                self.notifications.draw(SCREEN)
                pygame.display.update()
                continue

            SCREEN.blit(
                PLAYGROUND,
                (PLAYGROUND_OFFSET, PLAYGROUND_OFFSET),
                pygame.Rect(
                    PLAYGROUND_OFFSET,
                    PLAYGROUND_OFFSET,
                    PLAYGROUND_LENGTH,
                    PLAYGROUND_LENGTH,
                ),
            )

            pygame.draw.lines(
                SCREEN,
                (255, 255, 255),
                True,
                [
                    (PLAYGROUND_OFFSET, PLAYGROUND_OFFSET),
                    (PLAYGROUND_OFFSET, PLAYGROUND_LENGTH + PLAYGROUND_OFFSET),
                    (
                        PLAYGROUND_LENGTH + PLAYGROUND_OFFSET,
                        PLAYGROUND_LENGTH + PLAYGROUND_OFFSET,
                    ),
                    (PLAYGROUND_LENGTH + PLAYGROUND_OFFSET, PLAYGROUND_OFFSET),
                ],
                1,
            )

            self.drops.update()
            self.droplets.update()
            self.panel.update(self)

            if len(self.notifications) == 0:
                self.drops.draw(SCREEN)
                self.droplets.draw(SCREEN)
            self.panel.draw(SCREEN)
            self.notifications.draw(SCREEN)

            for drop, droplets in groupcollide(
                self.drops, self.droplets, dokilla=False, dokillb=False
            ).items():
                drop.hit()

                droplets[0].kill()  # many droplets hit same drop, only delete one

                if drop.need_diffuse:
                    self.score += 10
                    self.combo += 1
                    if self.combo in (3, 6, 9, 12, 15, 18, 20):
                        HP_SOUND.play()
                        self.hp += 1
                    elif self.combo > 21:
                        HP_SOUND.play()
                        self.hp += 1
                    Droplet.diffusion(drop.row, drop.col, self.droplets)

            pygame.display.update()

            if len(self.drops) <= 0 and len(self.droplets) == 0:
                self.level += 1
                self.hp += 2
                self.notify(NoticeType.success)
                self._init_grid()

            if len(self.droplets) == 0 and self.hp <= 0:
                self.notify(NoticeType.failed)
                self.start_game = False

        pygame.quit()
