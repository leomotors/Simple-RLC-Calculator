import pygame as pg

import math


class Circuit:
    def __init__(self):
        self.impedance = None
        self.voltage = None
        self.current = None
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

    def ApplyVoltage(self, voltage):
        self.voltage = voltage
        self.current = self.voltage / self.impedance
        self.CalcPhase()
        for c in self.components:
            c.ApplyCurrent(self.current)

    def printf(self) -> str:
        thicc_txt = ""
        for c in self.components:
            thicc_txt += c.printf()
            thicc_txt += "\n\n"
        thicc_txt += "Circuit Current is {:.4} ({:.4}) A leads by {:.4}π\n\n".format(
            self.current, abs(self.current), self.i_phase/math.pi)
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
        self.current = current
        self.voltage = self.current * self.impedance
        self.CalcPhase()
        for c in self.components:
            c.ApplyVoltage
