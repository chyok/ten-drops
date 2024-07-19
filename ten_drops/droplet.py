from typing import List

from pygame.sprite import Sprite
from pygame.transform import rotate

from ten_drops import DROPLET_IMAGES, BREAK_SOUND
from ten_drops import GRID_SIZE, PLAYGROUND_OFFSET, PLAYGROUND_LENGTH


class Direction:
    Down = (1, 0)
    Up = (-1, 0)
    Left = (0, -1)
    Right = (0, 1)


class Droplet(Sprite):
    def __init__(self, row, col, direction, *groups):
        super().__init__(*groups)
        self.row = row
        self.col = col
        self.direction = direction
        self.speed = 0.13

    def _update_image(self, image):
        if self.direction == Direction.Up:
            image = rotate(image, 90)
        elif self.direction == Direction.Left:
            image = rotate(image, 90 * 2)
        elif self.direction == Direction.Down:
            image = rotate(image, 90 * 3)

        self.image = image

        rect = image.get_rect()

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

    def update(self):
        self.row += self.direction[0] * self.speed
        self.col += self.direction[1] * self.speed
        if any(
            [
                self.row < -0.5,
                self.col < -0.5,
                self.row > GRID_SIZE - 0.5,
                self.col > GRID_SIZE - 0.5,
            ]
        ):
            # The actual animation is offset by half a grid cell
            self.kill()
            return

        self._update_image(DROPLET_IMAGES[0].static)

    @classmethod
    def diffusion(cls, row, col, *group) -> List["Droplet"]:
        BREAK_SOUND.play()
        droplets = []
        for direction in [
            Direction.Down,
            Direction.Up,
            Direction.Left,
            Direction.Right,
        ]:
            droplets.append(Droplet(row, col, direction, *group))
        return droplets
