import pygame

from typing import Dict
from collections import namedtuple

from pygame import Surface, Font
from pygame.color import Color
from pygame.sprite import Sprite

from ten_drops import NOTIFICATION, FONT_PATH, TEXT_FONT_PATH

_NType = namedtuple("_NType", "name font color")


class NoticeType:
    about = "about"
    failed = "failed"
    success = "success"


text_font = Font(TEXT_FONT_PATH, size=16)
text_font.set_bold(True)

TextDict: Dict[str, _NType] = {
    NoticeType.about: _NType("about", text_font, Color("white")),
    NoticeType.failed: _NType("failed", Font(FONT_PATH, size=45), Color("white")),
    NoticeType.success: _NType("failed", Font(FONT_PATH, size=45), Color("white")),
}


class Notice(Sprite):
    def __init__(self, _type, text, *groups):
        super().__init__(*groups)
        self._notification = TextDict[_type]

        self.text_area = Surface(
            (NOTIFICATION.get_width() * 0.8, NOTIFICATION.get_height() * 0.5),
            pygame.SRCALPHA,
        )
        self.image = NOTIFICATION.copy()
        self.rect = self.image.get_rect()
        self.rect.y = -self.rect.height

        text_surface = self._notification.font.render(
            text, True, self._notification.color
        )

        self.text_area.blit(text_surface, (0, 0))
        self.image.blit(
            self.text_area,
            (
                (self.image.get_width() - self.text_area.get_width()) / 1.8,
                NOTIFICATION.get_height() * 0.4,
            ),
        )

    def update(self):
        if self.rect.y < 0:
            self.rect.y += 25
