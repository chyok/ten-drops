from pygame import Font

from ten_drops import FONT_PATH, PANEL_X, PLAYGROUND_OFFSET, SCREEN

LARGE_FONT = Font(FONT_PATH, size=45)
SMALL_FONT = Font(FONT_PATH, size=40)


def draw_panel(level, score, hp):
    for text, font, row in (
        (f"level {level}", LARGE_FONT, 1),
        (f"score \n{score}", SMALL_FONT, 4),
        (f"drop \n{hp}", SMALL_FONT, 7),
    ):
        SCREEN.blit(
            font.render(text, True, "white"), (PANEL_X, PLAYGROUND_OFFSET * row)
        )
