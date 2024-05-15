import pygame
from pygame import Surface, Font
from pygame.color import THECOLORS
from pygame.sprite import Sprite

from ten_drops import DROP_IMAGES, GRID_SIZE, PLAYGROUND_OFFSET, PLAYGROUND_LENGTH, NOTIFICATION, FONT_PATH, SCREEN


class NotificationType:
    about = "about"
    failed = "failed"
    success = "success"


AboutFont = Font(FONT_PATH, size=45)
FailedFont = Font(FONT_PATH, size=45)
SuccessFont = Font(FONT_PATH, size=45)

TextDict = {
    NotificationType.about: "this is about",
    NotificationType.failed: "You Failed",
    NotificationType.success: "drops +1"
}


class Notification(Sprite):
    def __init__(self, _type, *groups):
        super().__init__(*groups)
        self.text = TextDict[_type]
        self.text_area = Surface((NOTIFICATION.get_width() * 0.8, NOTIFICATION.get_height() * 0.5),
                                 pygame.SRCALPHA)
        self.image = NOTIFICATION.copy()
        self.rect = self.image.get_rect()

    # @staticmethod
    # def _init_about():
    #     text = "this is text"
    #     return AboutFont.render(text, True, THECOLORS["white"])
    #
    # def _init(self, text):
    #     self.text_area.blit(text, (0, 0))
    #     self.image.blit(self.text_area,
    #                     ((self.image.get_width() - self.text_area.get_width()) / 1.8,
    #                      NOTIFICATION.get_height() * 0.4))
    #
    # def update(self):
    #     if self.type == NotificationType.about:
    #         text = self._init_about()
    #
    #     self.text_area.blit(text, (0, 0))
