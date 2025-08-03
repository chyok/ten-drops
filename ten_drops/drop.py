from pygame.sprite import Sprite

from ten_drops import DROP_IMAGES, GROW_SOUND, cell_center

HOVER = "hover"
GROW = "grow"
MAX_STATE = len(DROP_IMAGES) - 1


class Drop(Sprite):
    def __init__(self, row, col, state=0, *groups):
        super().__init__(*groups)
        self.row = row
        self.col = col
        self.state = state
        self.action = None
        self.frame = 0
        self.need_diffuse = False
        self._set_image(DROP_IMAGES[state].static)

    def _set_image(self, image):
        self.image = image
        self.rect = image.get_rect(center=cell_center(self.row, self.col))

    def click(self) -> bool:
        """Return False if the click was ignored."""
        if self.action == GROW:
            return False
        GROW_SOUND.play()
        self.hit()
        return True

    def hit(self):
        if self.state == MAX_STATE:
            self.kill()
            self.need_diffuse = True
        else:
            self.state += 1
            self.action = GROW

    def update(self):
        if self.action == GROW:
            frames = DROP_IMAGES[self.state - 1].grow
        elif self.action == HOVER:
            frames = DROP_IMAGES[self.state].hover
        else:
            self._set_image(DROP_IMAGES[self.state].static)
            return

        if self.frame < len(frames):
            self._set_image(frames[self.frame])
            self.frame += 1
        else:
            self.frame = 0
            self.action = HOVER if self.action == GROW else None

    def mouse_hover(self):
        if self.action != GROW:
            self.action = HOVER
