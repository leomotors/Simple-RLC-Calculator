import pygame as pg


class Resistor:
    def __init__(self):
        self.resistance = None
        self.impedance: complex = None

    def CalcImpedance(self):
        self.impedance = self.resistance


class Inductor:
    def __init__(self):
        self.inductance = None
        self.impedance: complex = None

    def CalcImpedance(self, ω):
        self.impedance = (self.inductance * ω) * 1j


class Capacitor:
    def __init__(self):
        self.capacitance = None
        self.impedance: complex = None

    def CalcImpedance(self, ω):
        self.impedance = (1 / (self.capacitance * ω)) * -1j
