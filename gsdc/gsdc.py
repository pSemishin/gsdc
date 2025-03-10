from typing import List

import gsd
import gsd.hoomd
import numpy as np

from .molecule import Mol
from .periodic_box import Box


class Pot:
    def __init__(self, box: Box):
        self.box = box
        self.coords = np.array(list())
        self.types: List = list()
        self.bonds: List = list()
        self.rho = 3
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

    def add_bead(self, bead_name: str):
        x = (0.5 - np.random.random()) * self.box.x
        y = (0.5 - np.random.random()) * self.box.y
        z = (0.5 - np.random.random()) * self.box.z
        coord = np.array([x, y, z])
        if len(self.coords) > 1:
            self.coords = np.vstack([self.coords, coord])
        else: 
            self.coords = coord
        self.types += [bead_name]
        self.N += 1
        
    def fuller(self, bead_name: str):
        num_solvent = int(self.box.volume * self.rho) - self.N
        if num_solvent < 1:
            raise ValueError('Pot: fuller: num_solvent < 1')
        x = (0.5 - np.random.random(num_solvent)) * self.box.x
        y = (0.5 - np.random.random(num_solvent)) * self.box.y
        z = (0.5 - np.random.random(num_solvent)) * self.box.z
        coord = np.vstack([x, y, z]).T
        if len(self.coords) > 1:
            self.coords = np.vstack([self.coords, coord])
        else: 
            self.coords = coord
        self.types += [bead_name] * num_solvent
        self.N += num_solvent
        
        
    def brew(self, name: str = "input.gsd"):
        bonds = np.array(self.bonds)
        coords = np.array(self.coords)

        snapshot = gsd.hoomd.Frame()
        snapshot.particles.N = self.N
        snapshot.configuration.box = [self.box.x, self.box.y, self.box.z, 0, 0, 0]
        snapshot.bonds.N = len(self.bonds)

        snapshot.particles.types = sorted(list(set(self.types)))
        b_types = set()
        for b in self.bonds:

            if self.types[b[0]] < self.types[b[1]]:
                b_types.add(self.types[b[0]] + self.types[b[1]])
            else:
                b_types.add(self.types[b[1]] + self.types[b[0]])

        snapshot.bonds.types = sorted(list(b_types))

        snapshot.particles.typeid = np.array(
            [snapshot.particles.types.index(t) for t in self.types]
        )
        snapshot.particles.position = coords
        snapshot.particles.mass = np.array([1.0] * self.N)
        snapshot.bonds.group = bonds
        tmp_type: str = ""
        b_type_id = list()
        for b in self.bonds:
            if self.types[b[0]] < self.types[b[1]]:
                tmp_type = self.types[b[0]] + self.types[b[1]]
            else:
                tmp_type = self.types[b[1]] + self.types[b[0]]
            b_type_id.append(snapshot.bonds.types.index(tmp_type))
        snapshot.bonds.typeid = np.array(b_type_id)

        with gsd.hoomd.open(name=name, mode="w") as f:
            f.append(snapshot)


    def dl_meso_config(self, name: str = 'CONFIG', solvent: str = "W"):
        coords = np.array(self.coords)
        N = self.N
        box = [self.box.x, self.box.y, self.box.z]
        types = self.types
        num = 1

        with open(file = name, mode = "w+") as f:
            f.write('DL_MESO molecule cyclic example\n')
            f.write(f'       0       1{N:10.0f}\n')
            f.write(f'{box[0]:16.10f}{0.0:16.10f}{0.0:16.10f}\n')
            f.write(f'{0.0:16.10f}{box[1]:16.10f}{0.0:16.10f}\n')
            f.write(f'{0.0:16.10f}{0.0:16.10f}{box[2]:16.10f} \n')
            for i, t in enumerate(types):
                if t == solvent:
                    f.write(f'{solvent}   {num :7.0f}\n')
                    num += 1
                    f.write(f'{coords[i][0] :16.10f}{coords[i][1] :16.10f}{coords[i][2] :16.10f}\n')
            for i, t in enumerate(types):
                if t != solvent:
                    f.write(f'{t}   {num :7.0f}\n')
                    num += 1
                    f.write(f'{coords[i][0] :16.10f}{coords[i][1] :16.10f}{coords[i][2] :16.10f}\n')