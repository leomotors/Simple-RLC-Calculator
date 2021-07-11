import pygame as pg


class Sprite:
    def __init__(self, init_position: tuple[int], size: tuple[int], screen: pg.Surface, appearance: bool = False):
        self.position = init_position
        self.size = size
        self.screen = screen
        self.appearance = appearance

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
        self.text = None

    def SetText(self, text):
        self.text = text

    def SetFont(self, font):
        self.font = font
    
    def show(self):
        pg.draw.rect(self.screen, (255, 255, 255), (self.position + self.size))
