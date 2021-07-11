import pygame as pg


class Toggle:
    def __init__(self, init_data: bool, name: str, txtdest: tuple[int]):
        self.internal_data = init_data
        self.name = name
        self.txtdest = txtdest
        self.toShow = None
        self.showTime = 0

    def toggleAndShow(self, screen: pg.Surface = None, font: pg.font.Font = None):
        self.internal_data = not self.internal_data
        if screen is not None:
            self.toShow = font.render("{} : {}".format(
                self.name, self.internal_data), True, (0, 0, 0))
            self.showTime = 75

    def update(self, screen: pg.Surface):
        if self.toShow is not None:
            screen.blit(self.toShow, self.txtdest)
            self.showTime -= 1
            if self.showTime <= 0:
                self.toShow = None

    def data(self) -> bool:
        return self.internal_data
