from pygame import Font
from pygame.sprite import Sprite

from ten_drops import PLAYGROUND_OFFSET, PLAYGROUND_LENGTH, FONT_PATH, SCREEN

white = (255, 255, 255)
grey = (160, 160, 160)


class Level(Sprite):
    LevelFont = Font(FONT_PATH, size=45)

    def __init__(self, level, *groups):
        super().__init__(*groups)
        self.image = self.LevelFont.render(f"level {level}", True, white)
        self.rect = self.image.get_rect()
        self.rect.x = PLAYGROUND_LENGTH + PLAYGROUND_OFFSET * 2
        self.rect.y = PLAYGROUND_OFFSET


class Score(Sprite):
    ScoreFont = Font(FONT_PATH, size=40)

    def __init__(self, score, *groups):
        super().__init__(*groups)
        self.image = self.ScoreFont.render(f"score \n{score}", True, white)
        self.rect = self.image.get_rect()
        self.rect.x = PLAYGROUND_LENGTH + PLAYGROUND_OFFSET * 2
        self.rect.y = PLAYGROUND_OFFSET * 4


class HP(Sprite):
    HpFont = Font(FONT_PATH, size=40)

    def __init__(self, hp, *groups):
        super().__init__(*groups)
        self.image = self.HpFont.render(f"drop \n{hp}", True, white)
        self.rect = self.image.get_rect()
        self.rect.x = PLAYGROUND_LENGTH + PLAYGROUND_OFFSET * 2
        self.rect.y = PLAYGROUND_OFFSET * 7


class Title(Sprite):
    TitleFont = Font(FONT_PATH, size=120)

    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = self.TitleFont.render("ten drops", True, (51, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = (SCREEN.get_width() - self.image.get_width()) / 2
        self.rect.y = SCREEN.get_height() / 10


class About(Sprite):
    AboutFont = Font(FONT_PATH, size=40)

    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = self.AboutFont.render("A ten drops game written in pygame.\n"
                                           "author: chyok\n"
                                           "email: chyok@hotmail.com", True, (32, 32, 32))
        self.rect = self.image.get_rect()
        self.rect.x = (SCREEN.get_width() - self.image.get_width()) / 2
        self.rect.y = SCREEN.get_height() / 3
