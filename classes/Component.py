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
        else:
            self.v_phase = math.atan(self.voltage.imag / self.voltage.real)

        if self.current.real == 0:
            self.i_phase = math.pi/2 if self.current.imag > 0 else -math.pi/2
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
        self.current = voltage / self.impedance
        self.CalcPhase()

    def printf(self) -> str:
        return "{} : I = {:.4} ({:.4}) A lacks by {:.4}π, V = {:.4} ({:.4}) V lacks by {:.4}π".format(
            self.getName(), self.current, abs(self.current), self.i_phase/math.pi, self.voltage, abs(self.voltage), self.v_phase/math.pi)


class Resistor(Component):
    def __init__(self):
        Component.__init__(self)
        self.resistance = None
        self.impedance: complex = None
        self.pic: pg.Surface = resistor

    def CalcImpedance(self):
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
        self.impedance = (1 / (self.capacitance * ω)) * -1j

    def getName(self) -> str:
        return "Capacitor {} F".format(self.capacitance)
