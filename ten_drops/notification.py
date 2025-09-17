from pygame import Font
from pygame.sprite import Sprite

from ten_drops import FONT_PATH, NOTIFICATION, TEXT_FONT_PATH


class NoticeType:
    about = "about"
    failed = "failed"
    success = "success"


_text_font = Font(TEXT_FONT_PATH, size=16)
_text_font.set_bold(True)
_title_font = Font(FONT_PATH, size=45)

FONTS = {
    NoticeType.about: _text_font,
    NoticeType.failed: _title_font,
    NoticeType.success: _title_font,
}


class Notice(Sprite):
    """A notice that slides down from the top of the screen."""

    def __init__(self, kind, text, *groups):
        super().__init__(*groups)
        self.image = NOTIFICATION.copy()
        self.rect = self.image.get_rect(bottom=0)
        width, height = self.image.get_size()
        text_image = FONTS[kind].render(text, True, "white")
        self.image.blit(text_image, (width // 9, height * 0.4))

    def update(self):
        self.rect.y = min(self.rect.y + 25, 0)
