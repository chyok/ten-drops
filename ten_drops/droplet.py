from pygame.sprite import Sprite
from pygame.transform import rotate

from ten_drops import BREAK_SOUND, DROPLET_IMAGE, GRID_SIZE, cell_center

# (row step, col step) -> rotation of the right-facing image
DIRECTIONS = {(1, 0): 270, (-1, 0): 90, (0, -1): 180, (0, 1): 0}
SPEED = 0.13


class Droplet(Sprite):
    def __init__(self, row, col, direction, *groups):
        super().__init__(*groups)
        self.row = row
        self.col = col
        self.direction = direction
        self.image = rotate(DROPLET_IMAGE, DIRECTIONS[direction])

    def update(self):
        self.row += self.direction[0] * SPEED
        self.col += self.direction[1] * SPEED
        # drops sit in the middle of their cell, so leave half a cell past the edge
        edge = GRID_SIZE - 0.5
        if not (-0.5 <= self.row <= edge and -0.5 <= self.col <= edge):
            self.kill()
            return
        self.rect = self.image.get_rect(center=cell_center(self.row, self.col))

    @classmethod
    def diffusion(cls, row, col, *groups):
        BREAK_SOUND.play()
        for direction in DIRECTIONS:
            cls(row, col, direction, *groups)
