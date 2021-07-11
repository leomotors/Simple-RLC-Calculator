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
        pass


class ParallelCircuit(Circuit):
    def __init__(self):
        Circuit.__init__(self)
        pass
