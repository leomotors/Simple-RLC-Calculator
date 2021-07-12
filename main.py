import pygame as pg
from classes.Sprite import *
from classes.Toggle import Toggle
from classes.Circuit import *
from classes.Component import *

import pyautogui

import math
import sys

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

MainCircuit = SeriesCircuit()

try:
    Circuit_Voltage: float = float(pyautogui.prompt(
        text="Enter Voltage (rms): ", title="Circuit Setup", default=""))

    Circuit_f_Input = pyautogui.prompt(
        text="Enter Circuit Frequency or ω (Put 'Hz' if it is frequency, no prefix allowed)", title="Circuit Setup", default="")

    if Circuit_Voltage is None or Circuit_f_Input is None:
        raise TypeError

    Circuit_ω = 0
    if "Hz" in Circuit_f_Input:
        Circuit_ω = 2 * math.pi * float(Circuit_f_Input[:-2].split(" ")[0])
    else:
        Circuit_ω = Circuit_f_Input
        if type(Circuit_ω) is not int and type(Circuit_ω) is not float:
            raise TypeError

except:
    sys.stdout.write("\a")
    sys.stdout.flush()
    pyautogui.alert(
        text="Exception Raised, please make sure the input is correct", title="Error")
    pg.quit()
    sys.exit()


while True:
    screen.fill((255, 255, 255))

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

        if event.type == pg.MOUSEBUTTONDOWN:
            pos = pg.mouse.get_pos()
            for button in buttons:
                if button.checkCollide(pos):
                    if button.text == "Add R":
                        temp = Resistor()
                        temp.resistance = float(pyautogui.prompt(
                            text="Enter Resistance: ", title="Add Resistor", default=""))
                        if temp.resistance is None:
                            pass
                        temp.CalcImpedance()
                        print(temp.impedance)
                        MainCircuit.components.append(temp)

                    if button.text == "Add L":
                        temp = Inductor()
                        temp.inductance = float(pyautogui.prompt(
                            text="Enter Inductance: ", title="Add Inductor", default=""))
                        temp.CalcImpedance(Circuit_ω)
                        print(temp.impedance)
                        MainCircuit.components.append(temp)

                    if button.text == "Add C":
                        temp = Capacitor()
                        temp.capacitance = float(pyautogui.prompt(
                            text="Enter Capacitance: ", title="Add Capacitor", default=""))
                        temp.CalcImpedance(Circuit_ω)
                        print(temp.impedance)
                        MainCircuit.components.append(temp)

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                isParallel.toggleAndShow(screen, font)
            if event.key == pg.K_RETURN:
                MainCircuit.CalcImpedance()
                print(MainCircuit.impedance)

    for button in buttons:
        button.show()

    MainCircuit.drawComponent(screen)
    isParallel.update(screen)
    pg.display.flip()
    setfps.tick(TICK_RATE)
