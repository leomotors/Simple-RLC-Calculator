import pygame as pg


class Resistor:
    def __init__(self):
        self.resistance = None
        self.impedance = None

    def CalcImpedance(self):
        self.impedance = self.resistance


class Inductor:
    def __init__(self):
        self.inductance = None
        self.impedance = None

    def CalcImpedance(self, ω):
        self.impedance = self.inductance * ω


class Capacitor:
    def __init__(self):
        self.capacitance = None
        self.impedance = None

    def CalcImpedance(self, ω):
        self.impedance = 1 / (self.capacitance * ω)
    