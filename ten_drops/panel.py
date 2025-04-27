from pygame import Font
from pygame.sprite import Sprite
from pygame.color import Color

from ten_drops import PLAYGROUND_OFFSET, PLAYGROUND_LENGTH, FONT_PATH


class Level(Sprite):
    LevelFont = Font(FONT_PATH, size=45)

    def __init__(self, level, *groups):
        super().__init__(*groups)
        self.level = level
        self._update_image()

    def _update_image(self):
        self.image = self.LevelFont.render(f"level {self.level}", True, Color("white"))
        self.rect = self.image.get_rect()
        self.rect.x = PLAYGROUND_LENGTH + PLAYGROUND_OFFSET * 2
        self.rect.y = PLAYGROUND_OFFSET

    def update(self, game):
        self.level = game.level
        self._update_image()


class Score(Sprite):
    ScoreFont = Font(FONT_PATH, size=40)

    def __init__(self, score, *groups):
        super().__init__(*groups)
        self.score = score
        self._update_image()

    def _update_image(self):
        self.image = self.ScoreFont.render(
            f"score \n{self.score}", True, Color("white")
        )
        self.rect = self.image.get_rect()
        self.rect.x = PLAYGROUND_LENGTH + PLAYGROUND_OFFSET * 2
        self.rect.y = PLAYGROUND_OFFSET * 4

    def update(self, game):
        self.score = game.score
        self._update_image()


class HP(Sprite):
    HpFont = Font(FONT_PATH, size=40)

    def __init__(self, hp, *groups):
        super().__init__(*groups)
        self.hp = hp
        self._update_image()

    def _update_image(self):
        self.image = self.HpFont.render(f"drop \n{self.hp}", True, Color("white"))
        self.rect = self.image.get_rect()
        self.rect.x = PLAYGROUND_LENGTH + PLAYGROUND_OFFSET * 2
        self.rect.y = PLAYGROUND_OFFSET * 7

    def update(self, game):
        self.hp = game.hp
        self._update_image()

