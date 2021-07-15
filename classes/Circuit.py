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

    def drawComponent(self, screen: pg.Surface, font: pg.font.Font):
        x_offset = 0
        x_start = 400 - 60 * len(self.components)
        for c in self.components:
            c.drawComponent(screen, font, x_start + x_offset)
            x_offset += 120

    def ApplyVoltage(self, voltage: complex):
        Component.ApplyVoltage(self, voltage)
        for c in self.components:
            c.ApplyCurrent(self.current)

    def printf(self, _=None, __=None, ___=None, indent_level: int = 0, _ind: int = 0) -> str:
        thicc_txt = "Series Circuit with these properties:\n  Current = {}\n  Total Voltage = {}\n  Total Impedance = {}\n  Total Power = {}\n  and it's components are\n\n".format(
            self.printAmp(), self.printVolt(), self.printImp(), self.printPower())

        for ind, c in enumerate(self.components):
            thicc_txt += c.printf(False, True, True, indent_level + 1, ind+1)
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

    def drawComponent(self, screen: pg.Surface, font: pg.font.Font, x_pos: float):
        y_offset = 0
        y_start = 185 - 35 * len(self.components) + 20

        for c in self.components:
            c.drawComponent(screen, font,  x_pos, y_start + y_offset)
            y_offset += 85
        pg.draw.rect(screen, (0, 0, 0),
                     ((x_pos, y_start + 45) + (5, y_offset - 85)))
        pg.draw.rect(screen, (0, 0, 0),
                     ((x_pos + 120, y_start + 45) + (5, y_offset - 85)))

    def ApplyCurrent(self, current: complex):
        Component.ApplyCurrent(self, current)
        for c in self.components:
            c.ApplyVoltage(self.voltage)

    def printf(self, _, __, ___, indent_level: int, index: int) -> str:
        indent = " " * (indent_level-1)
        overindent = indent + " "
        thicc_txt = "{}{}) Parallel Circuit with these properties:\n{}Total Current = {}\n{}Voltage = {}\n{}Total impedance = {}\n{}Total Power = {}\n{}and it's components are\n\n".format(
            indent, index, overindent, self.printAmp(), overindent, self.printVolt(), overindent, self.printImp(), overindent, self.printPower(), overindent)

        for ind, c in enumerate(self.components):
            thicc_txt += c.printf(True, False, True, indent_level + 1, ind + 1)
            thicc_txt += "\n"
        return thicc_txt
