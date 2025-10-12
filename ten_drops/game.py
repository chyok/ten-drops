import random

import pygame
from pygame.sprite import Group, GroupSingle, groupcollide

from ten_drops import (
    BACKGROUND,
    CELL,
    GRID_SIZE,
    GROW_SOUND,
    HP_SOUND,
    PLAYGROUND,
    PLAYGROUND_OFFSET,
    PLAYGROUND_RECT,
    SCREEN,
    cell_center,
)
from ten_drops.button import Button
from ten_drops.cover import make_cover
from ten_drops.drop import Drop
from ten_drops.droplet import Droplet
from ten_drops.notification import Notice, NoticeType
from ten_drops.panel import draw_panel

# number of drops in each state (smallest to largest) per level
LEVELS = [
    (2, 5, 8, 9),
    (2, 6, 7, 8),
    (3, 7, 7, 7),
    (3, 7, 6, 6),
    (4, 7, 6, 5),
    (4, 8, 6, 5),
    (4, 8, 5, 5),
    (5, 9, 3, 5),
    (6, 9, 4, 5),
]

ABOUT_TEXT = (
    "The game and water drop assets are \n"
    'from the Flash game "Splash Back".\n'
    "\n\n\nAuthor: chyok\n"
    "Email : chyok@hotmail.com\nGithub: https://github.com/chyok\n"
    "\nImplemented using pygame-ce."
)


class Game:
    def __init__(self):
        self.start_game = False
        self.run = True

        self.drops = Group()
        self.droplets = Group()
        self.buttons = Group()
        self.notifications = GroupSingle()

        Button("start", PLAYGROUND_OFFSET * 13.5, self._new_game, self.buttons)
        Button("about", PLAYGROUND_OFFSET * 15.5, self._about, self.buttons)
        Button("exit", PLAYGROUND_OFFSET * 17.5, self._exit, self.buttons)

        # clicking near the centre of an empty cell places a new drop
        self.cells = {
            (row, col): pygame.Rect(0, 0, CELL // 2, CELL // 2).move_to(
                center=cell_center(row, col)
            )
            for row in range(GRID_SIZE)
            for col in range(GRID_SIZE)
        }
        self.hovered = pygame.Rect(0, 0, 0, 0)
        self.cover = make_cover()
        self.clock = pygame.time.Clock()
        self._init_game_data()

    def _init_game_data(self):
        self.level = 1
        self.score = 0
        self.hp = 10
        self.combo = 1

    def _init_grid(self):
        if self.level <= len(LEVELS):
            counts = LEVELS[self.level - 1]
        else:
            counts = random.choice(LEVELS[-5:])
        states = [state for state, count in enumerate(counts) for _ in range(count)]
        cells = random.sample(list(self.cells), len(states))
        for (row, col), state in zip(cells, states):
            Drop(row, col, state, self.drops)

    def _new_game(self):
        self.drops.empty()
        self.droplets.empty()
        self._init_game_data()
        self._init_grid()
        self.start_game = True

    def _about(self):
        self.notify(NoticeType.about)

    def _exit(self):
        self.run = False

    def notify(self, kind):
        if kind == NoticeType.success:
            text = "     Well Done!\n     + 2 drops\n\n     Next Level"
        elif kind == NoticeType.failed:
            text = f"You Lost\nYour Score: {self.score}"
        else:
            text = ABOUT_TEXT
        Notice(kind, text, self.notifications)

    def _on_click(self, pos):
        if self.notifications:
            self.notifications.empty()
            return

        if self.start_game and not self.droplets:
            self._click_board(pos)

        for button in self.buttons:
            if button.rect.collidepoint(pos):
                button.action()

    def _click_board(self, pos):
        drop = next((d for d in self.drops if d.rect.collidepoint(pos)), None)
        if drop:
            if drop.click():
                self.combo = 1
                self.hp -= 1
                if drop.need_diffuse:
                    self.score += 10
                    Droplet.diffusion(drop.row, drop.col, self.droplets)
            return

        occupied = {(d.row, d.col) for d in self.drops}
        for cell, rect in self.cells.items():
            if rect.collidepoint(pos) and cell not in occupied:
                GROW_SOUND.play()
                Drop(*cell, 0, self.drops)
                self.hp -= 1

    def _on_motion(self, pos):
        # start the hover animation once when the mouse enters a drop
        if not self.hovered.collidepoint(pos):
            self.hovered = pygame.Rect(0, 0, 0, 0)
            for drop in self.drops:
                if drop.rect.collidepoint(pos):
                    drop.mouse_hover()
                    self.hovered = drop.rect
                    break

        for button in self.buttons:
            button.set_hover(button.rect.collidepoint(pos))

    def _resolve_collisions(self):
        hits = groupcollide(self.drops, self.droplets, False, False)
        for drop, droplets in hits.items():
            drop.hit()
            droplets[0].kill()  # many droplets hit same drop, only delete one

            if drop.need_diffuse:
                self.score += 10
                self.combo += 1
                if self.combo % 3 == 0 or self.combo > 21:
                    HP_SOUND.play()
                    self.hp += 1
                Droplet.diffusion(drop.row, drop.col, self.droplets)

    def _check_progress(self):
        if not self.drops and not self.droplets:
            self.level += 1
            self.hp += 2
            self.notify(NoticeType.success)
            self._init_grid()

        if not self.droplets and self.hp <= 0:
            self.notify(NoticeType.failed)
            self.start_game = False

    def _draw_board(self, paused):
        SCREEN.blit(PLAYGROUND, PLAYGROUND_RECT)
        rect = PLAYGROUND_RECT
        pygame.draw.lines(
            SCREEN,
            "white",
            True,
            [rect.topleft, rect.bottomleft, rect.bottomright, rect.topright],
        )
        if not paused:
            self.drops.draw(SCREEN)
            self.droplets.draw(SCREEN)
        draw_panel(self.level, self.score, self.hp)

    def start(self):
        while self.run:
            self.clock.tick(30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                    break
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self._on_click(event.pos)
                elif event.type == pygame.MOUSEMOTION:
                    self._on_motion(event.pos)

            SCREEN.blit(BACKGROUND, (0, 0))
            self.buttons.draw(SCREEN)
            self.notifications.update()

            if not self.start_game:
                SCREEN.blit(self.cover, (0, 0))
                self.notifications.draw(SCREEN)
                pygame.display.update()
                continue

            # freeze the board while a notification is shown
            paused = bool(self.notifications)
            if not paused:
                self.drops.update()
                self.droplets.update()
            self._draw_board(paused)
            self.notifications.draw(SCREEN)
            if not paused:
                self._resolve_collisions()
            pygame.display.update()

            self._check_progress()

        pygame.quit()
