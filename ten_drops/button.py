from pygame import Font
from pygame.sprite import Sprite

from ten_drops import PLAYGROUND_OFFSET, PLAYGROUND_LENGTH, FONT_PATH, SCREEN

white = (255, 255, 255)
grey = (160, 160, 160)

NormalFont = Font(FONT_PATH, size=65)
NormalFont.set_italic(True)


class StartButton(Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self._update_color(white)

    def _update_color(self, color):
        self.image = NormalFont.render("start", True, color)
        self.rect = self.image.get_rect()
        self.rect.x = PLAYGROUND_LENGTH + PLAYGROUND_OFFSET * 2
        self.rect.y = PLAYGROUND_OFFSET * 13.5

    def mouse_hover(self):
        self._update_color(grey)

    def mouse_leave(self):
        self._update_color(white)


class AboutButton(Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self._update_color(white)

    def _update_color(self, color):
        self.image = NormalFont.render("about", True, color)
        self.rect = self.image.get_rect()
        self.rect.x = PLAYGROUND_LENGTH + PLAYGROUND_OFFSET * 2
        self.rect.y = PLAYGROUND_OFFSET * 15.5

    def mouse_hover(self):
        self._update_color(grey)

    def mouse_leave(self):
        self._update_color(white)


class ExitButton(Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self._update_color(white)

    def _update_color(self, color):
        self.image = NormalFont.render("exit", True, color)
        self.rect = self.image.get_rect()
        self.rect.x = PLAYGROUND_LENGTH + PLAYGROUND_OFFSET * 2
        self.rect.y = PLAYGROUND_OFFSET * 17.5

    def mouse_hover(self):
        self._update_color(grey)

    def mouse_leave(self):
        self._update_color(white)
