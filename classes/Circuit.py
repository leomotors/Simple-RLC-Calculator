import pygame as pg

import math

from .Component import Component


class Circuit(Component):
    def __init__(self):
        self.components: list[Component] = []  # * Circuits or Components
        self.impedance = None
        self.voltage = None
        self.current = None
        self.v_phase = None
        self.i_phase = None


class SeriesCircuit(Circuit):
    def __init__(self):
        Circuit.__init__(self)
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

    def printf(self, _=None, __=None, indent_level: int = 0) -> str:
        thicc_txt = "Series Circuit with current of {}, total voltage is {}, impedance is {}, and it's components are\n\n".format(
            self.printAmp(), self.printVolt(), self.printImp())

        for c in self.components:
            thicc_txt += c.printf(False, True, indent_level + 1)
            thicc_txt += "\n\n"
        return thicc_txt


class ParallelCircuit(Circuit):
    def __init__(self):
        Circuit.__init__(self)
        self.impendance: complex = None

    def CalcImpedance(self):
        sumimpinv = None
        try:
            sumimpinv = sum(1 / k.impedance for k in self.components)
        except ZeroDivisionError:
            sumimpinv = math.inf

        try:
            self.impedance = 1 / sumimpinv
        except ZeroDivisionError:
            self.impedance = math.inf

    def getImpedance(self) -> complex:
        return self.impedance

    def drawComponent(self, screen: pg.Surface, x_pos: float):
        y_offset = 0
        y_start = 200 - 35 * len(self.components)
        for c in self.components:
            c.drawComponent(screen, x_pos, y_start + y_offset)
            y_offset += 70

    def ApplyCurrent(self, current: complex):
        Component.ApplyCurrent(self, current)
        for c in self.components:
            c.ApplyVoltage(self.voltage)

    def printf(self, _, __, indent_level: int = 1) -> str:
        thicc_txt = "{}• Parallel Circuit with total current of {}, voltage across it is {}, impedance is {}, and it's components are\n\n".format(
            "  " * (indent_level - 1), self.printAmp(), self.printVolt(), self.printImp())

        for c in self.components:
            thicc_txt += c.printf(True, False, indent_level + 1)
            thicc_txt += "\n"
        return thicc_txt
