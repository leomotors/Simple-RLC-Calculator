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
        self.v_phase = math.atan(self.voltage.imag / self.voltage.real)
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
        return "{} : I = {} A, V = {} V".format(
            self.getName(), self.current, self.voltage)


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
