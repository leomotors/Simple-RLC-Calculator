import pygame as pg

import math

resistor = pg.image.load("assets/images/Resistor.png")
resistor = pg.transform.scale(resistor, (120, 90))
inductor = pg.image.load("assets/images/Inductor.png")
inductor = pg.transform.scale(inductor, (120, 60))
capacitor = pg.image.load("assets/images/Capacitor.png")
capacitor = pg.transform.scale(capacitor, (100, 100))


class Component:
    def __init__(self):
        self.pic = None
        self.y_offset = 0
        self.current = None
        self.voltage = None
        self.impedance = None
        self.v_phase = None
        self.i_phase = None

    def CalcPhase(self):
        if self.voltage.real == 0:
            self.v_phase = math.pi/2 if self.voltage.imag > 0 else -math.pi/2
        elif self.voltage.imag == 0:
            self.v_phase = 0
        else:
            self.v_phase = math.atan(self.voltage.imag / self.voltage.real)

        if self.current.real == 0:
            self.i_phase = math.pi/2 if self.current.imag > 0 else -math.pi/2
        elif self.current.imag == 0:
            self.i_phase = 0
        else:
            self.i_phase = math.atan(self.current.imag / self.current.real)

    def drawComponent(self, screen: pg.Surface, x_pos: float):
        screen.blit(self.pic, (x_pos, 200 + self.y_offset))

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

    def printf(self, printI: bool, printV: bool) -> str:
        return "• {} :{}{}{}".format(
            self.getName(), " I = {}".format(self.printAmp) if printI else "", "," if printI and printV else "", " V = {}".format(self.printVolt()) if printV else "")


class Resistor(Component):
    def __init__(self):
        Component.__init__(self)
        self.resistance = None
        self.impedance: complex = None
        self.pic: pg.Surface = resistor

    def CalcImpedance(self, _):
        self.impedance = self.resistance

    def getName(self) -> str:
        return "Resistor {} Ω".format(self.resistance)


class Inductor(Component):
    def __init__(self):
        Component.__init__(self)
        self.inductance = None
        self.impedance: complex = None
        self.pic: pg.Surface = inductor
        self.y_offset = 15

    def CalcImpedance(self, ω):
        self.impedance = (self.inductance * ω) * 1j

    def getName(self) -> str:
        return "Inductor {} H".format(self.inductance)


class Capacitor(Component):
    def __init__(self):
        Component.__init__(self)
        self.capacitance = None
        self.impedance: complex = None
        self.pic: pg.Surface = capacitor
        self.y_offset = -5

    def CalcImpedance(self, ω):
        try:
            self.impedance = (1 / (self.capacitance * ω)) * -1j
        except ZeroDivisionError:
            self.impedance = math.inf * -1j

    def getName(self) -> str:
        return "Capacitor {} F".format(self.capacitance)
