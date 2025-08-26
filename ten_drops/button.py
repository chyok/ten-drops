from pygame import Font
from pygame.sprite import Sprite

from ten_drops import FONT_PATH, PANEL_X

FONT = Font(FONT_PATH, size=65)
FONT.set_italic(True)


class Button(Sprite):
    def __init__(self, text, y, action, *groups):
        super().__init__(*groups)
        self.action = action
        self.normal = FONT.render(text, True, "white")
        self.hovered = FONT.render(text, True, "grey")
        self.image = self.normal
        self.rect = self.image.get_rect(topleft=(PANEL_X, y))

    def set_hover(self, hover: bool):
        self.image = self.hovered if hover else self.normal
