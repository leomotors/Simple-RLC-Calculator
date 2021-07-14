import pygame as pg
from classes.Sprite import *
from classes.Toggle import Toggle
from classes.Circuit import *
from classes.Component import *

import pyautogui

import math
import sys

# * Initialization

pg.init()

SCREENRES = (800, 600)
TICK_RATE = 75
FONT_SIZE = 18

programIcon = pg.image.load("assets/images/Diode.png")
programIcon = pg.transform.scale(programIcon, (256, 256))

pg.display.set_icon(programIcon)
pg.display.set_caption("Simple RLC Calculator 1.0 Pre-Release")

screen = pg.display.set_mode(SCREENRES)

setfps = pg.time.Clock()

font = pg.font.Font("assets/fonts/Prompt-Regular.ttf", FONT_SIZE)


PopUp = PopUpMessages(screen, font, (300, 10))

addR = Button((150, 510), (100, 40), screen, True)
addR.SetText("Add R")
addL = Button((350, 510), (100, 40), screen, True)
addL.SetText("Add L")
addC = Button((550, 510), (100, 40), screen, True)
addC.SetText("Add C")

buttons = [addR, addL, addC]
for button in buttons:
    button.SetFont(font)

isParallel = Toggle(False, "Parallel Mode", (280, 560))

MainCircuit = SeriesCircuit()

# * Initialize Circuit Voltage and Angular Speed
try:
    temp_cv_input = pyautogui.prompt(
        text="Enter Voltage (Default: rms, add 'M' to mark as max): ", title="Circuit Setup", default="")
    if 'M' in temp_cv_input:
        Circuit_Voltage: float = float(temp_cv_input[:-1]) / math.sqrt(2)
    else:
        Circuit_Voltage: float = float(temp_cv_input)

    Circuit_f_Input = pyautogui.prompt(
        text="Enter Circuit Frequency or ω (Put 'Hz' if it is frequency, no prefix allowed)", title="Circuit Setup", default="")

    if Circuit_Voltage is None or Circuit_f_Input is None:
        raise TypeError

    Circuit_ω = 0
    if "Hz" in Circuit_f_Input:
        Circuit_ω = 2 * math.pi * float(Circuit_f_Input[:-2].split(" ")[0])
    else:
        Circuit_ω = float(Circuit_f_Input)

except:
    sys.stdout.write("\a")
    sys.stdout.flush()
    pyautogui.alert(
        text="Exception Raised, please make sure the input is correct", title="Error")
    pg.quit()
    sys.exit()

# * The boi who take care of displaying circuit voltage info on screen 24/7
Circuit_Input_Information = Text((105, 470), screen)
Circuit_Input_Information.SetFont(font)
Circuit_Input_Information.SetText(
    "Circuit Voltage : {:.4} V rms ({:.4} V Peak) @ {:.4} Hz ({:.4} rad/s)".format(Circuit_Voltage, Circuit_Voltage * math.sqrt(2), Circuit_ω/2/math.pi, Circuit_ω))

newParallel = False


def CollapseLastParallelIfItIs():
    if len(MainCircuit.components) >= 1 and type(MainCircuit.components[-1]) is ParallelCircuit and len(MainCircuit.components[-1].components) == 1:
        MainCircuit.components.append(
            MainCircuit.components[-1].components[0])
        del MainCircuit.components[-2]


def addComponent(ComponentType: type):
    global newParallel
    temp = ComponentType()
    try:
        if ComponentType is Resistor:
            temp.resistance = float(pyautogui.prompt(
                text="Enter Resistance: ", title="Add Resistor", default=""))
        elif ComponentType is Inductor:
            input_method = pyautogui.confirm(
                title="Add Inductor", text="Please Select Input Method", buttons=["Inductance", "Reactance"])
            if input_method == "Inductance":
                temp.inductance = float(pyautogui.prompt(
                    text="Enter Inductance: ", title="Add Inductor", default=""))
            elif input_method == "Reactance":
                temp.inductance = float(pyautogui.prompt(
                    text="Enter Reactance: ", title="Add Inductor", default="")) / Circuit_ω
            else:
                raise KeyboardInterrupt
        elif ComponentType is Capacitor:
            input_method = pyautogui.confirm(
                title="Add Capacitor", text="Please Select Input Method", buttons=["Capacitance", "Reactance"])
            if input_method == "Capacitance":
                temp.capacitance = float(pyautogui.prompt(
                    text="Enter Capacitance: ", title="Add Capacitor", default=""))
            elif input_method == "Reactance":
                temp.capacitance = 1 / float(pyautogui.prompt(
                    text="Enter Reactance: ", title="Add Capacitor", default="")) / Circuit_ω
            else:
                raise KeyboardInterrupt
    except:
        PopUp.ShowText(
            "Adding Component aborted because exception is raised", 150)
    else:
        temp.CalcImpedance(Circuit_ω)
        if isParallel.data():
            if len(MainCircuit.components) == 0 or type(MainCircuit.components[-1]) is not ParallelCircuit or newParallel:
                CollapseLastParallelIfItIs()
                MainCircuit.components.append(ParallelCircuit())
            MainCircuit.components[-1].components.append(temp)
            MainCircuit.components[-1].CalcImpedance()
            newParallel = False
        else:
            CollapseLastParallelIfItIs()
            MainCircuit.components.append(temp)


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
                        addComponent(Resistor)
                    if button.text == "Add L":
                        addComponent(Inductor)
                    if button.text == "Add C":
                        addComponent(Capacitor)

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_r:
                addComponent(Resistor)
            elif event.key == pg.K_l:
                addComponent(Inductor)
            elif event.key == pg.K_c:
                addComponent(Capacitor)
            elif event.key == pg.K_SPACE:
                isParallel.toggleAndShow(screen, font)
                newParallel = True
            elif event.key == pg.K_RETURN:
                try:
                    if len(MainCircuit.components) == 0:
                        raise AttributeError
                    MainCircuit.CalcImpedance()
                    MainCircuit.ApplyVoltage(Circuit_Voltage)
                    pyautogui.alert(text=MainCircuit.printf() + "*Phase is referenced from input voltage",
                                    title="Circuit Calculation Result")
                except:
                    pyautogui.alert(text="Exception raised during calculation, Circuit might not be valid",
                                    title="Error")

    for button in buttons:
        button.show()

    MainCircuit.drawComponent(screen, font)
    Circuit_Input_Information.show()
    isParallel.update(screen)
    PopUp.update()

    pg.display.flip()
    setfps.tick(TICK_RATE)
