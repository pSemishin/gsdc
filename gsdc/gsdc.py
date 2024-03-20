from typing import List

import numpy as np

from .molecule import Mol
from .periodic_box import Box


class Pot:
    def __init__(self, box: Box):
        self.box = box
        self.coords = np.array(list())
        self.types: List = list()
        self.bonds: List = list()
        self.N = 0

    def add(self, molecule: Mol):
        x, y, z = molecule.get_coords(self.box)
        coord = np.vstack([x, y, z]).T
        if len(self.coords) < 1:
            self.coords = coord
        else:
            self.coords = np.vstack([self.coords, coord])
        self.types += molecule.types
        self.bonds += [(b[0] + self.N, b[1] + self.N) for b in molecule.bonds]
        self.N += molecule.num_beads
