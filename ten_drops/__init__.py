import pygame

from typing import List, Union
from os.path import join, dirname
from dataclasses import dataclass

from pygame import image, Surface
from pygame.transform import smoothscale, gaussian_blur

__all__ = [
    "SCREEN",
    "GRID_SIZE",
    "BACKGROUND",
    "PLAYGROUND",
    "PLAYGROUND_LENGTH",
    "PLAYGROUND_OFFSET",
    "NOTIFICATION",
    "DROP_IMAGES",
    "DROPLET_IMAGES",
    "FONT_PATH",
    "TEXT_FONT_PATH",
    "BREAK_SOUND",
    "GROW_SOUND",
    "HP_SOUND",
]

pygame.init()

# To solve the error that occurs on some computers without audio output devices
_OPEN_SOUND = True
try:
    pygame.mixer.init()
except Exception as e:  # noqa
    _OPEN_SOUND = False

pygame.display.set_caption("ten drops")

Path = dirname(__file__)
ImageFolderPath = join(Path, "asset", "img")
AudioFolderPath = join(Path, "asset", "audio")

pygame.display.set_icon(pygame.image.load(join(ImageFolderPath, "game.ico")))

cursor = pygame.image.load(join(ImageFolderPath, "cursor.png"))

cursor = pygame.cursors.Cursor((10, 0), cursor)

pygame.mouse.set_cursor(cursor)


@dataclass
class Status:
    action: List[Surface]
    change_action: List[Surface]
    static: Union[Surface, None] = None


class Sound:
    def __init__(self, sound_file: str):
        if _OPEN_SOUND:
            self.sound = pygame.mixer.Sound(join(AudioFolderPath, sound_file))

    def play(self):
        if _OPEN_SOUND:
            self.sound.play()


def get_drop_images() -> List[Status]:
    drop_image_path = join(ImageFolderPath, "drop")
    drop_image_paths = [join(drop_image_path, f"{i}.png") for i in range(134)]

    drop_images = [image.load(i).convert_alpha() for i in drop_image_paths]
    _ = [
        i.fill(pygame.Color("blue"), special_flags=pygame.BLEND_ADD)
        for i in drop_images
    ]

    max_length = max(max(i.get_size()) for i in drop_images[:130])
    radio = PLAYGROUND_LENGTH / GRID_SIZE / max_length

    drop_images = [
        smoothscale(i, (i.get_width() * radio, i.get_height() * radio))
        for i in drop_images
    ]

    return [
        Status(
            action=drop_images[0:20],
            change_action=drop_images[25:31],
            static=drop_images[19],
        ),
        Status(
            action=drop_images[48:66],
            change_action=drop_images[69:76],
            static=drop_images[60],
        ),
        Status(
            action=drop_images[76:90],
            change_action=drop_images[108:115],
            static=drop_images[85],
        ),
        Status(
            action=drop_images[115:130],
            change_action=drop_images[130:134],
            static=drop_images[126],
        ),
    ]


def get_droplet_images() -> List[Status]:
    droplet_image_path = join(ImageFolderPath, "droplet")
    droplet_image_paths = [join(droplet_image_path, f"{i}.png") for i in range(7)]

    droplet_images = [image.load(i).convert_alpha() for i in droplet_image_paths]
    _ = [
        i.fill(pygame.Color("blue"), special_flags=pygame.BLEND_ADD)
        for i in droplet_images
    ]

    max_length = max(max(i.get_size()) for i in droplet_images[:3])

    radio = (
        PLAYGROUND_LENGTH / GRID_SIZE / max_length / 3
    )  # droplet is 3 times smaller than a drop

    droplet_images = [
        smoothscale(i, (i.get_width() * radio, i.get_height() * radio))
        for i in droplet_images
    ]

    return [
        Status(
            action=droplet_images[:3],
            change_action=droplet_images[3:],
            static=droplet_images[1],
        )
    ]


SCREEN = pygame.display.set_mode((800, 600))
GRID_SIZE = 6

FONT_PATH = join(Path, "asset", "font", "kust.ttf")
TEXT_FONT_PATH = join(Path, "asset", "font", "FiraCode-Regular.ttf")

BACKGROUND = smoothscale(
    image.load(join(ImageFolderPath, "background.png")),
    (SCREEN.get_width(), SCREEN.get_height()),
)

NOTIFICATION = smoothscale(
    image.load(join(ImageFolderPath, "notification.png")),
    (SCREEN.get_width() / 1.5, SCREEN.get_height() / 1.5),
)

PLAYGROUND = BACKGROUND.copy()

PLAYGROUND_LENGTH = SCREEN.get_height() * (9 / 10)

PLAYGROUND_OFFSET = (SCREEN.get_height() - PLAYGROUND_LENGTH) / 2

PLAYGROUND = gaussian_blur(PLAYGROUND, 5)

DROP_IMAGES = get_drop_images()

DROPLET_IMAGES = get_droplet_images()

BREAK_SOUND = Sound("break.mp3")
GROW_SOUND = Sound("grow.mp3")
HP_SOUND = Sound("hp.mp3")
