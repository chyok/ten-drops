import pygame
from pygame import Font, Surface

from ten_drops import FONT_PATH, SCREEN


def make_cover() -> Surface:
    width, height = SCREEN.get_size()
    cover = Surface((width, height), pygame.SRCALPHA)
    cover.fill((255, 255, 255, 30))

    title = Font(FONT_PATH, size=120).render("ten drops", True, (51, 255, 255))
    cover.blit(title, ((width - title.get_width()) / 2, height / 10))

    text = Font(FONT_PATH, size=42).render(
        "A ten drops game written in pygame.", True, (32, 32, 32)
    )
    cover.blit(text, ((width - text.get_width()) / 2, height / 3))
    return cover
