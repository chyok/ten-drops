from pygame import Font

from ten_drops import PLAYGROUND_OFFSET, PLAYGROUND_LENGTH, FONT_PATH, SCREEN

LevelFont = Font(FONT_PATH, size=45)
ScoreFont = Font(FONT_PATH, size=40)
DropFont = Font(FONT_PATH, size=40)
NormalFont = Font(FONT_PATH, size=65)
NormalFont.set_italic(True)

TitleFont = Font(FONT_PATH, size=120)

white = (255, 255, 255)
grey = (160, 160, 160)

START_TEXT = NormalFont.render("start", True, white)
ABOUT_TEXT = NormalFont.render("about", True, white)
EXIT_TEXT = NormalFont.render("exit", True, white)


class TextHelper:

    @staticmethod
    def draw_title():
        title = TitleFont.render("ten drops", True, (51, 255, 255))
        SCREEN.blit(title, ((SCREEN.get_width() - title.get_width()) / 2, 10))

    @staticmethod
    def draw_panel(level, score, hp, running, over_mouse=False):
        level_text = LevelFont.render(f"level {level}", True, white)
        score_text = ScoreFont.render(f"score \n{score}", True, white)
        drops_text = DropFont.render(f"drop \n{hp}", True, white)

        if over_mouse:
            start_text = NormalFont.render("start", True, grey)
            about_text = NormalFont.render("about", True, grey)
            exit_text = NormalFont.render("exit", True, grey)
        else:
            start_text = START_TEXT
            about_text = ABOUT_TEXT
            exit_text = EXIT_TEXT

        if running:
            SCREEN.blit(level_text, (PLAYGROUND_LENGTH + PLAYGROUND_OFFSET * 2, PLAYGROUND_OFFSET))
            SCREEN.blit(score_text, (PLAYGROUND_LENGTH + PLAYGROUND_OFFSET * 2, PLAYGROUND_OFFSET * 4))
            SCREEN.blit(drops_text, (PLAYGROUND_LENGTH + PLAYGROUND_OFFSET * 2, PLAYGROUND_OFFSET * 7))

        SCREEN.blit(start_text, (PLAYGROUND_LENGTH + PLAYGROUND_OFFSET * 2, PLAYGROUND_OFFSET * 12))
        SCREEN.blit(about_text, (PLAYGROUND_LENGTH + PLAYGROUND_OFFSET * 2, PLAYGROUND_OFFSET * 14))
        SCREEN.blit(exit_text, (PLAYGROUND_LENGTH + PLAYGROUND_OFFSET * 2, PLAYGROUND_OFFSET * 16))
