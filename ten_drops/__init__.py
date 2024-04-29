import pygame

from os.path import join, dirname
from dataclasses import dataclass

from pygame import image, Surface
from pygame.transform import smoothscale

__all__ = [
    "SCREEN",
    "BACKGROUND",
    "PLAYGROUND",
    "DROP_IMAGES"
]

pygame.init()
pygame.display.set_caption("ten drops")

SCREEN = pygame.display.set_mode((800, 600))

PATH = dirname(__file__)
IMAGE_PATH = join(PATH, "asset", "img")

BACKGROUND = Surface((SCREEN.get_width(), SCREEN.get_height()))
BACKGROUND.fill((128, 128, 128))

PLAYGROUND = Surface((SCREEN.get_height(), SCREEN.get_height()))
PLAYGROUND.fill((0, 0, 0))
PLAYGROUND.set_alpha(100)


@dataclass
class Status:
    action: list[Surface]
    change_action: list[Surface]
    stable: Surface


def get_drop_images() -> list[Status]:
    drop_image_path = join(IMAGE_PATH, "drop")
    drop_image_paths = [join(drop_image_path, f"{i}.png") for i in range(139)]

    drop_images = [image.load(i).convert_alpha() for i in drop_image_paths]

    max_height = max(i.get_height() for i in drop_images[:134])
    max_width = max(i.get_width() for i in drop_images[:134])

    drop_images = [smoothscale(i, (i.get_width() * (PLAYGROUND.get_width() / 10 / max_width),
                                   i.get_height() * (PLAYGROUND.get_height() / 10 / max_height))) for i in drop_images]

    return [Status(action=drop_images[:31], change_action=drop_images[31:35], stable=drop_images[3]),
            Status(action=drop_images[35:71], change_action=drop_images[71:76], stable=drop_images[39]),
            Status(action=drop_images[76:110], change_action=drop_images[110:121], stable=drop_images[79]),
            Status(action=drop_images[121:134], change_action=drop_images[134:], stable=drop_images[125])]


DROP_IMAGES = get_drop_images()
