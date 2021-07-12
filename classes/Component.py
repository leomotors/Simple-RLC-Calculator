import pygame as pg

resistor = pg.image.load("assets/images/Resistor.png")
resistor = pg.transform.scale(resistor, (80, 80))
inductor = pg.image.load("assets/images/Inductor.png")
inductor = pg.transform.scale(inductor, (80, 80))
capacitor = pg.image.load("assets/images/Capacitor.png")
capacitor = pg.transform.scale(capacitor, (80, 80))


class Component:
    def __init__(self):
        self.pic = None
        pass

    def drawComponent(self, screen: pg.Surface):
        screen.blit(self.pic, (200, 200))


class Resistor(Component):
    def __init__(self):
        self.resistance = None
        self.impedance: complex = None
        self.pic: pg.Surface = resistor

    def CalcImpedance(self):
        self.impedance = self.resistance


class Inductor(Component):
    def __init__(self):
        self.inductance = None
        self.impedance: complex = None
        self.pic: pg.Surface = inductor

    def CalcImpedance(self, ω):
        self.impedance = (self.inductance * ω) * 1j


class Capacitor(Component):
    def __init__(self):
        self.capacitance = None
        self.impedance: complex = None
        self.pic: pg.Surface = capacitor

    def CalcImpedance(self, ω):
        self.impedance = (1 / (self.capacitance * ω)) * -1j
