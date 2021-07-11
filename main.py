import pygame as pg
from classes.Sprite import *
from classes.Toggle import Toggle
import pyautogui

pg.init()

SCREENRES = (800, 600)
TICK_RATE = 75
FONT_SIZE = 18

screen = pg.display.set_mode(SCREENRES)
pg.display.set_caption("Simple RLC Calculator 1.0 Snapshot")
setfps = pg.time.Clock()

font = pg.font.Font("assets/fonts/Prompt-Regular.ttf", FONT_SIZE)

addR = Button((150, 510), (100, 40), screen, True)
addR.SetText("Add R")
addL = Button((350, 510), (100, 40), screen, True)
addL.SetText("Add L")
addC = Button((550, 510), (100, 40), screen, True)
addC.SetText("Add C")

buttons = [addR, addL, addC]
for button in buttons:
    button.SetFont(font)

isParallel = Toggle(False, "Parallel Mode", (313, 560))

while True:
    screen.fill((0, 0, 0))

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()

        if event.type == pg.MOUSEBUTTONDOWN:
            pos = pg.mouse.get_pos()
            for button in buttons:
                if button.checkCollide(pos):
                    print("Collide with", button.text)

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                isParallel.toggleAndShow(screen, font)

    for button in buttons:
        button.show()

    isParallel.update(screen)
    pg.display.flip()
    setfps.tick(TICK_RATE)
