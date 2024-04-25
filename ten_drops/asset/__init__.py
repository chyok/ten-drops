import os
from os.path import join
from pygame import image, Surface
from pygame.transform import smoothscale

from ten_drops import Screen

PATH = os.path.dirname(__file__)
IMAGE_PATH = join(PATH, "img")

DROP_IMAGE_PATH = join(IMAGE_PATH, "drop")
DROP_IMAGE_PATHS = [join(DROP_IMAGE_PATH, f"{i}.png") for i in range(139)]
DROP_IMAGES = [image.load(i).convert_alpha() for i in DROP_IMAGE_PATHS]

max_height = max(i.get_height() for i in DROP_IMAGES[:134])
max_width = max(i.get_width() for i in DROP_IMAGES[:134])

TO_SIZE = (Screen.get_height() / 10, Screen.get_width() / 10)
ratio = (TO_SIZE[0] / max_height, TO_SIZE[1] / max_width)

DROP_IMAGES = [smoothscale(i, (i.get_height() * ratio[0], i.get_width() * ratio[1])) for i in DROP_IMAGES]


class Status:
    def __init__(self, action, change_action, stable):
        self.action: list[Surface] = action
        self.change_action: list[Surface] = change_action
        self.stable: Surface = stable


DropImage = [Status(action=DROP_IMAGES[:31], change_action=DROP_IMAGES[31:35], stable=DROP_IMAGES[3]),
             Status(action=DROP_IMAGES[35:71], change_action=DROP_IMAGES[71:76], stable=DROP_IMAGES[39]),
             Status(action=DROP_IMAGES[76:110], change_action=DROP_IMAGES[110:121], stable=DROP_IMAGES[79]),
             Status(action=DROP_IMAGES[121:134], change_action=DROP_IMAGES[134:], stable=DROP_IMAGES[125])]
