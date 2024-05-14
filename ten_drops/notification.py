from pygame import Surface
from pygame.sprite import Sprite

from ten_drops import DROP_IMAGES, GRID_SIZE, PLAYGROUND_OFFSET, PLAYGROUND_LENGTH


class NotificationType:
    about = "about"
    failed = "failed"
    success = "success"


class Notification(Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.type = NotificationType.about
        self.base_surface = Surface()

    def _update_image(self):
        pass

    def update(self):
        pass
