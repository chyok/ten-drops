from typing import Literal

from pygame.sprite import Sprite, Group

from ten_drops import DROP_IMAGES, GRID_SIZE, PLAYGROUND_OFFSET, PLAYGROUND_LENGTH
from ten_drops.droplet import Droplet


class ActionType:
    hover = "hover"
    change = "change"
    static = "static"


class Drop(Sprite):
    def __init__(self, row, col, state: Literal[0, 1, 2, 3] = 0, *groups):
        super().__init__(*groups)
        self.row = row
        self.col = col
        self.state = state
        self.radius = 10
        self.action_type = ActionType.static
        self.action_count = 0
        self._update_image(DROP_IMAGES[self.state].static)

    def _update_image(self, image):
        self.image = image
        rect = self.image.get_rect()
        rect.x = self.col * (PLAYGROUND_LENGTH // GRID_SIZE) + (
                PLAYGROUND_LENGTH // GRID_SIZE // 2) - rect.width // 2 + PLAYGROUND_OFFSET
        rect.y = self.row * (PLAYGROUND_LENGTH // GRID_SIZE) + (
                PLAYGROUND_LENGTH // GRID_SIZE // 2) - rect.height // 2 + PLAYGROUND_OFFSET
        self.rect = rect

    def click(self):
        if self.action_type == ActionType.change:
            # ignore click when changing
            return

        self.state = self.state + 1

        self.radius = (PLAYGROUND_LENGTH // GRID_SIZE // 2 // 2) + self.state * 5
        self.action_type = ActionType.change

    def hit(self) -> bool:
        if self.state + 1 > len(DROP_IMAGES):
            # if two droplets hit same drop and will break, return false to keep the droplet
            return False

        self.state = self.state + 1

        self.radius = (PLAYGROUND_LENGTH // GRID_SIZE // 2 // 2) + self.state * 5
        self.action_type = ActionType.change
        return True

    def update(self, drops: Group, droplets: Group):
        if self.state >= len(DROP_IMAGES):
            drops.remove(self)
            droplets.add(Droplet.diffusion(self.row, self.col))
            return

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
                self._update_image(DROP_IMAGES[self.state - 1].change_action[self.action_count])
                self.action_count += 1
            else:
                self.action_count = 0
                self.action_type = ActionType.hover
        else:
            self._update_image(DROP_IMAGES[self.state].static)

    def mouse_hover(self):
        if self.action_type != ActionType.change:
            self.action_type = ActionType.hover
