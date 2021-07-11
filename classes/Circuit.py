import pygame as pg


class Circuit:
    def __init__(self):
        self.impedance = None
        self.voltage = None
        self.current = None
        self.v_phase = None
        self.i_phase = None


class SeriesCircuit(Circuit):
    def __init__(self):
        Circuit.__init__(self)
        self.components = []  # * Circuits or Components
        self.impedance = None

    def CalcImpedance(self):
        self.impedance = sum(k.impedance for k in self.components)

    def getImpedance(self) -> complex:
        return self.impedance


class ParallelCircuit(Circuit):
    def __init__(self):
        Circuit.__init__(self)
        self.components = []  # * Circuits or Components
        self.impendance = None

    def CalcImpedance(self):
        self.impedance = 1 / sum(1/k.impedance for k in self.components)

    def getImpedance(self) -> complex:
        return self.impedance
