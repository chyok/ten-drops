from os.path import dirname, join
from typing import List, NamedTuple

import pygame
from pygame import Surface
from pygame.transform import gaussian_blur, smoothscale

ASSET_PATH = join(dirname(__file__), "asset")
IMG_PATH = join(ASSET_PATH, "img")
FONT_PATH = join(ASSET_PATH, "font", "kust.ttf")
TEXT_FONT_PATH = join(ASSET_PATH, "font", "FiraCode-Regular.ttf")

# the mixer stays uninitialised on machines without an audio device
pygame.init()
pygame.display.set_caption("ten drops")
pygame.display.set_icon(pygame.image.load(join(IMG_PATH, "game.ico")))
pygame.mouse.set_cursor(
    pygame.cursors.Cursor((10, 0), pygame.image.load(join(IMG_PATH, "cursor.png")))
)

SCREEN = pygame.display.set_mode((800, 600))
GRID_SIZE = 6
PLAYGROUND_LENGTH = SCREEN.get_height() * 0.9
PLAYGROUND_OFFSET = (SCREEN.get_height() - PLAYGROUND_LENGTH) / 2
PLAYGROUND_RECT = pygame.Rect(
    PLAYGROUND_OFFSET, PLAYGROUND_OFFSET, PLAYGROUND_LENGTH, PLAYGROUND_LENGTH
)
CELL = PLAYGROUND_LENGTH // GRID_SIZE
PANEL_X = PLAYGROUND_LENGTH + PLAYGROUND_OFFSET * 2


def cell_center(row: float, col: float):
    return (
        PLAYGROUND_OFFSET + col * CELL + CELL // 2,
        PLAYGROUND_OFFSET + row * CELL + CELL // 2,
    )


class Frames(NamedTuple):
    hover: List[Surface]
    grow: List[Surface]
    static: Surface


class Sound:
    def __init__(self, name: str):
        path = join(ASSET_PATH, "audio", name)
        self.sound = pygame.mixer.Sound(path) if pygame.mixer.get_init() else None

    def play(self):
        if self.sound:
            self.sound.play()


def _load(folder: str, index: int) -> Surface:
    image = pygame.image.load(join(IMG_PATH, folder, f"{index}.png")).convert_alpha()
    image.fill("blue", special_flags=pygame.BLEND_ADD)
    return image


def _scale(image: Surface, ratio: float) -> Surface:
    return smoothscale(image, (image.get_width() * ratio, image.get_height() * ratio))


# frame numbers in asset/img/drop: hover animation, grow animation, static frame
_DROP_FRAMES = [
    (range(0, 20), range(25, 31), 19),
    (range(48, 66), range(69, 76), 60),
    (range(76, 90), range(108, 115), 85),
    (range(115, 130), (), 126),  # the largest drop bursts instead of growing
]


def _drop_images() -> List[Frames]:
    used = {i for hover, grow, _ in _DROP_FRAMES for i in (*hover, *grow)}
    images = {i: _load("drop", i) for i in used}
    # the largest frame fills a whole cell
    ratio = CELL / max(max(image.get_size()) for image in images.values())
    images = {i: _scale(image, ratio) for i, image in images.items()}
    return [
        Frames([images[i] for i in hover], [images[i] for i in grow], images[static])
        for hover, grow, static in _DROP_FRAMES
    ]


def _droplet_image() -> Surface:
    images = [_load("droplet", i) for i in range(3)]
    # a droplet is a third of a drop
    ratio = CELL / max(max(image.get_size()) for image in images) / 3
    return _scale(images[1], ratio)


BACKGROUND = smoothscale(
    pygame.image.load(join(IMG_PATH, "background.png")), SCREEN.get_size()
)
PLAYGROUND = gaussian_blur(BACKGROUND, 5).subsurface(PLAYGROUND_RECT)
NOTIFICATION = smoothscale(
    pygame.image.load(join(IMG_PATH, "notification.png")),
    (SCREEN.get_width() / 1.5, SCREEN.get_height() / 1.5),
)

DROP_IMAGES = _drop_images()
DROPLET_IMAGE = _droplet_image()

BREAK_SOUND = Sound("break.mp3")
GROW_SOUND = Sound("grow.mp3")
HP_SOUND = Sound("hp.mp3")
