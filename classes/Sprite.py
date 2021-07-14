import pygame as pg


class Sprite:
    def __init__(self, init_position: tuple[int], size: tuple[int], screen: pg.Surface, appearance: bool = False):
        self.position = init_position
        self.size = size
        self.screen = screen
        self.appearance = appearance
        self.text = None
        self.font = None

    def SetText(self, text: str):
        self.text = text

    def SetFont(self, font: pg.font.Font):
        self.font = font

    # * Check if pos is in Sprite's Boundary
    def checkCollide(self, pos: tuple[int]):
        if pos[0] > self.position[0] and pos[0] < self.position[0] + self.size[0] and pos[1] > self.position[1] and pos[1] < self.position[1] + self.size[1]:
            return True
        else:
            return False

    def show(self):
        pass


class Button(Sprite):
    def __init__(self, position: tuple[int], size: tuple[int], screen: pg.Surface, appearance: bool = False):
        Sprite.__init__(self, position, size, screen, appearance)

    def show(self):
        if not self.appearance:
            return

        pg.draw.rect(self.screen, (0, 0, 0), (self.position + self.size))
        if self.text is not None:
            self.renderText()

    def renderText(self):
        txtSprite = self.font.render(self.text, True, (255, 255, 255))
        self.screen.blit(
            txtSprite, (self.position[0] + 20, self.position[1] + 5))


class Text(Sprite):
    def __init__(self, position: tuple[int], screen: pg.Surface):
        Sprite.__init__(self, position, None, screen, True)

    def show(self):
        if not self.appearance:
            return

        txtSprite = self.font.render(self.text, True, (0, 0, 0))
        self.screen.blit(txtSprite, self.position)


class PopUpMessages():
    def __init__(self, screen: pg.Surface, font: pg.font.Font, dest: tuple[int]):
        self.screen: pg.Surface = screen
        self.font: pg.font.Font = font
        self.dest = dest
        self.txt_sprite = None
        self.txt_len = 0
        self.showTime = None

    def ShowText(self, txt: str, showTime: int = 75):
        self.txt_sprite = self.font.render(txt, True, (0, 0, 0))
        self.txt_len = len(txt)
        self.showTime = showTime

    def update(self):
        if self.txt_sprite is not None:
            self.screen.blit(
                self.txt_sprite, (self.dest[0] - self.txt_len * 3, self.dest[1]))
            self.showTime -= 1
            if self.showTime <= 0:
                self.txt_sprite = None
