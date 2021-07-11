import pygame as pg
from classes.Sprite import *

pg.init()

SCREENRES = (800, 600)
TICK_RATE = 75

screen = pg.display.set_mode(SCREENRES)
pg.display.set_caption("Simple RLC Calculator 1.0 Snapshot")
setfps = pg.time.Clock()

box = Button((300, 300), (200, 50), screen, True)

while True:
    screen.fill((0, 0, 0))

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
        if event.type == pg.MOUSEBUTTONDOWN:
            pos = pg.mouse.get_pos()
            print(pos)
            if box.checkCollide(pos):
                print("COLLIDE")

    box.show()
    pg.display.flip()
    setfps.tick(TICK_RATE)
