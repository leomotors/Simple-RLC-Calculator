import pygame as pg

import math
import cmath

from .cclean import *

resistor = pg.image.load("assets/images/Resistor.png")
resistor = pg.transform.scale(resistor, (120, 90))
inductor = pg.image.load("assets/images/Inductor.png")
inductor = pg.transform.scale(inductor, (120, 60))
capacitor = pg.image.load("assets/images/Capacitor.png")
capacitor = pg.transform.scale(capacitor, (120, 100))


class Component:
    def __init__(self):
        self.pic = None
        self.y_offset = 0
        self.current = None
        self.voltage = None
        self.impedance = None
        self.v_phase = None
        self.i_phase = None
        self.txtSprite = None
        self.txtOffset = 0

    def CalcPhase(self):
        self.v_phase = cmath.phase(self.voltage)
        self.i_phase = cmath.phase(self.current)

    def drawComponent(self, screen: pg.Surface, font: pg.font.Font, x_pos: float, y_pos: float = 150):
        screen.blit(self.pic, (x_pos, y_pos + self.y_offset))
        if self.txtSprite is None:
            self.txtSprite = font.render(self.getShortName(), True, (0, 0, 0))
        screen.blit(self.txtSprite, (x_pos + 30, y_pos + 70 + self.txtOffset))

    def ApplyCurrent(self, current):
        self.current = current
        self.voltage = current * self.impedance
        self.CalcPhase()

    def ApplyVoltage(self, voltage):
        self.voltage = voltage
        try:
            self.current = voltage / self.impedance
        except ZeroDivisionError:
            self.current = math.inf * voltage
        self.CalcPhase()

    def printAmp(self) -> str:
        return "{:.4} ({:.4}) Amp {} by {:.4}π ({:.4}deg)".format(self.current, abs(self.current), "leads" if self.i_phase >= 0 else "lacks", abs(self.i_phase/math.pi), abs(180*self.i_phase/math.pi))

    def printVolt(self) -> str:
        return "{:.4} ({:.4}) Volt {} by {:.4}π ({:.4}deg)".format(self.voltage, abs(self.voltage), "leads" if self.v_phase >= 0 else "lacks", abs(self.v_phase/math.pi), abs(180*self.v_phase/math.pi))

    def printImp(self) -> str:
        return "{:.4} ({:.4}) Ω".format(self.impedance, abs(self.impedance))

    def printPower(self) -> str:
        return "{:.4} VA".format(RoundComplex(self.voltage * self.current.conjugate()))

    def printf(self, printI: bool, printV: bool, printP: bool, indent_level: int, index: int) -> str:
        indent = " " * (indent_level - 1) if indent_level >= 1 else ""
        overindent = indent + " "
        return "{}{}) {} :\n{}{}{}".format(
            indent, index, self.getName(), "{}I = {}\n".format(overindent, self.printAmp()) if printI else "", "{}V = {}\n".format(overindent, self.printVolt()) if printV else "", "{}P = {}\n".format(overindent, self.printPower()) if printP else "")


class Resistor(Component):
    def __init__(self):
        Component.__init__(self)
        self.resistance = None
        self.impedance: complex = None
        self.pic: pg.Surface = resistor
        self.txtOffset = -5

    def CalcImpedance(self, _):
        self.impedance = self.resistance

    def getName(self) -> str:
        return "Resistor {} Ω".format(self.resistance)

    def getShortName(self) -> str:
        return "{} Ω".format(self.resistance)


class Inductor(Component):
    def __init__(self):
        Component.__init__(self)
        self.inductance = None
        self.impedance: complex = None
        self.pic: pg.Surface = inductor
        self.y_offset = 15
        self.txtOffset = 5

    def CalcImpedance(self, ω):
        self.impedance = (self.inductance * ω) * 1j

    def getName(self) -> str:
        return "Inductor {:.4} H ({:.4} Ω)".format(self.inductance, abs(self.impedance))

    def getShortName(self) -> str:
        return "{:.4} H".format(self.inductance)


class Capacitor(Component):
    def __init__(self):
        Component.__init__(self)
        self.capacitance = None
        self.impedance: complex = None
        self.pic: pg.Surface = capacitor
        self.y_offset = -5
        self.txtOffset = 5

    def CalcImpedance(self, ω):
        try:
            self.impedance = (1 / (self.capacitance * ω)) * -1j
        except ZeroDivisionError:
            self.impedance = math.inf * -1j

    def getName(self) -> str:
        return "Capacitor {:.4} F ({:.4} Ω)".format(self.capacitance, abs(self.impedance))

    def getShortName(self) -> str:
        return "{:.4} C".format(self.capacitance)
