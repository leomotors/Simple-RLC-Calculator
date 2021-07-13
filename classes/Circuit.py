import pygame as pg

import math

from .Component import Component


class Circuit(Component):
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
        self.impedance: complex = None

    def CalcImpedance(self):
        self.impedance = sum(k.impedance for k in self.components)

    def getImpedance(self) -> complex:
        return self.impedance

    def drawComponent(self, screen: pg.Surface):
        x_offset = 0
        x_start = 400 - 50 * len(self.components)
        for c in self.components:
            c.drawComponent(screen, x_start + x_offset)
            x_offset += 100

    def ApplyVoltage(self, voltage: complex):
        Component.ApplyVoltage(self, voltage)
        for c in self.components:
            c.ApplyCurrent(self.current)

    def printf(self) -> str:
        thicc_txt = "Series Circuit with current of {} and voltage across it is {}\n\n".format(
            self.printAmp(), self.printVolt())

        for c in self.components:
            thicc_txt += c.printf()
            thicc_txt += "\n\n"
        return thicc_txt


class ParallelCircuit(Circuit):
    def __init__(self):
        Circuit.__init__(self)
        self.components = []  # * Circuits or Components
        self.impendance: complex = None

    def CalcImpedance(self):
        self.impedance = 1 / sum(1/k.impedance for k in self.components)

    def getImpedance(self) -> complex:
        return self.impedance

    def ApplyCurrent(self, current: complex):
        Component.ApplyCurrent(self, current)
        for c in self.components:
            c.ApplyVoltage
