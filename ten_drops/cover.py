import pygame
from pygame import Font, Surface

from ten_drops import FONT_PATH, SCREEN


class Cover:
    TitleFont = Font(FONT_PATH, size=120)
    TextFont = Font(FONT_PATH, size=42)

    def __init__(self):
        self._update_image()

    def _update_image(self):
        width = SCREEN.get_width()
        height = SCREEN.get_height()
        cover_surface = Surface((width, height), pygame.SRCALPHA)
        cover_surface.fill((255, 255, 255, 30))

        title_image = self.TitleFont.render("ten drops", True, (51, 255, 255))
        cover_surface.blit(
            title_image, ((width - title_image.get_width()) / 2, height / 10)
        )

        text_image = self.TextFont.render(
            "A ten drops game written in pygame.", True, (32, 32, 32)
        )

        cover_surface.blit(
            text_image, ((width - text_image.get_width()) / 2, height / 3)
        )

        self.image = cover_surface
        self.rect = self.image.get_rect()

    def draw(self):
        SCREEN.blit(self.image, self.rect)
