import pygame
from pygame.sprite import Sprite

from ten_drops import (
    DROP_IMAGES,
    GRID_SIZE,
    PLAYGROUND_OFFSET,
    PLAYGROUND_LENGTH,
    GROW_SOUND,
)


class ActionType:
    hover = "hover"
    change = "change"
    static = "static"


class Drop(Sprite):
    def __init__(self, row, col, state=0, *groups):
        super().__init__(*groups)
        self.row = row
        self.col = col
        self.state = state
        self.action_type = ActionType.static
        self.action_count = 0
        self.need_diffuse = False
        self._update_image(DROP_IMAGES[self.state].static)

    def _update_image(self, image):
        self.image = image
        rect = self.image.get_rect()
        rect.x = (
            self.col * (PLAYGROUND_LENGTH // GRID_SIZE)
            + (PLAYGROUND_LENGTH // GRID_SIZE // 2)
            - rect.width // 2
            + PLAYGROUND_OFFSET
        )
        rect.y = (
            self.row * (PLAYGROUND_LENGTH // GRID_SIZE)
            + (PLAYGROUND_LENGTH // GRID_SIZE // 2)
            - rect.height // 2
            + PLAYGROUND_OFFSET
        )
        self.rect = rect

    def click(self):
        if self.action_type == ActionType.change:
            # ignore click when changing
            return

        GROW_SOUND.play()

        if self.state >= len(DROP_IMAGES) - 1:
            self.kill()
            self.need_diffuse = True
            return

        self.state = self.state + 1

        self.action_type = ActionType.change

    def hit(self):
        if self.state > len(DROP_IMAGES) - 1:
            # if many droplets hit same drop, ignore the out of bounds
            return

        elif self.state == len(DROP_IMAGES) - 1:
            self.kill()
            self.need_diffuse = True
            return

        self.state = self.state + 1

        self.action_type = ActionType.change
        return

    def update(self):
        if self.action_type == ActionType.hover:
            all_count = len(DROP_IMAGES[self.state].action)
            if self.action_count < all_count:
                self._update_image(DROP_IMAGES[self.state].action[self.action_count])
                self.action_count += 1
            else:
                self.action_count = 0
                self.action_type = ActionType.static

        elif self.action_type == ActionType.change:
            all_count = len(DROP_IMAGES[self.state - 1].change_action)
            if self.action_count < all_count:
                self._update_image(
                    DROP_IMAGES[self.state - 1].change_action[self.action_count]
                )
                self.action_count += 1
            else:
                self.action_count = 0
                self.action_type = ActionType.hover
        else:
            self._update_image(DROP_IMAGES[self.state].static)

    def mouse_hover(self):
        if self.action_type != ActionType.change:
            self.action_type = ActionType.hover


class DummyDrop(Sprite):
    def __init__(self, row, col, *groups):
        super().__init__(*groups)
        self.row = row
        self.col = col
        self.image = pygame.Surface(
            (
                (PLAYGROUND_LENGTH // GRID_SIZE // 2),
                (PLAYGROUND_LENGTH // GRID_SIZE // 2),
            ),
            pygame.SRCALPHA,
        )
        rect = self.image.get_rect()
        rect.x = (
            self.col * (PLAYGROUND_LENGTH // GRID_SIZE)
            + (PLAYGROUND_LENGTH // GRID_SIZE // 2)
            - rect.width // 2
            + PLAYGROUND_OFFSET
        )
        rect.y = (
            self.row * (PLAYGROUND_LENGTH // GRID_SIZE)
            + (PLAYGROUND_LENGTH // GRID_SIZE // 2)
            - rect.height // 2
            + PLAYGROUND_OFFSET
        )
        self.rect = rect
