from typing import Dict, Final, Optional, Tuple

import numpy as np

from .bondset import Bondtype
from .check_graph import CheckGraph
from .exceptions import (EmptyGraphError, FixedDictError, FixedOutBoxError,
                         FixedRootError, GapsMolGraphError,
                         IterationLimitError, MolGraphConnectionError,
                         MolGraphSimplicityError)
from .periodic_box import Box

BOND_LENGTH: Final[float] = (1.0 / 3.0) ** (1.0 / 3.0)
ITERATION_LIMIT: Final[int] = 1000
EPS = 0.001


def rnd_vector(length: float = BOND_LENGTH) -> np.ndarray:
    """
    Generates a random 3D vector of a given length

    Args:
        length (float, optional): Defaults to LENGTH_BOND = (1/3)^(1/3) ~ 0.693..

    Returns:
        np.ndarray: random 3D vector of any given length
    """
    v = np.random.uniform(-1.0, 1.0, 3)
    v = v / np.sqrt(np.sum(v**2)) * length
    return v


def repulsive_force(bond_length: float, x: float) -> float:
    """_summary_

    Args:
        bond_length (float): lengths of bond
        x (float): coordinate

    Returns:
        float: linear repulsive force
    """
    return (bond_length / x - 1.0) * 0.5


class MolGraph:
    """
    Creation, building and processing of a molecular graph
        Graph must be simple and fully-connected

    Attributes:
        self.num_bonds (int): number of bonds (edges) <- input
        self.num_beads (int): number of beads (nodes)
        self.cyclical (bool): True if graph is cyclical, False otherwise
        self.directed (bool): True if graph is directed, False otherwise
    """

    def __init__(self, bonds: Bondtype, sort: bool = True) -> None:
        """
        Args:
            bonds (List[Tuple[int,int]]): list of bonded node ids
            sort (bool, optional): Should the graph be sorted? Defaults to True.

        Raises:
            GapsMolGraphError: Gaps in indexation
            MolGraphSimplicityError: Graph is not simple
            MolGraphConnectionError: Graph is not connected
        """
        # Sorting the list of bonds and id in bonds
        if sort:
            self.bonds = sorted([(min(bond), max(bond)) for bond in bonds])
        else:
            self.bonds = bonds
        # Check graph for critical exceptions
        if not self.bonds:
            raise EmptyGraphError
        if not CheckGraph.is_not_gaps(self.bonds):
            raise GapsMolGraphError
        if not CheckGraph.is_simple(self.bonds):
            raise MolGraphSimplicityError
        if not CheckGraph.is_connected(self.bonds):
            raise MolGraphConnectionError
        # Searchig for max index in the bond list
        self.num_beads: int = max([max(bond[0], bond[1]) for bond in bonds]) + 1
        self.num_bonds: int = len(self.bonds)
        # Basic properties for building a graph
        self.cyclical: bool = self.num_bonds >= self.num_beads
        self.directed: bool = CheckGraph.is_directed(self.bonds)

    def __str__(self):
        return f"""
            Num_beads = {self.num_beads} 
            Num_bonds = {self.num_bonds}
            Cyclical = {self.cyclical}
            Directed = {self.directed}            
            """

    def get_coords(
        self,
        box: Box,
        fixed_coords: Optional[Dict[int, Tuple[float, float, float]]] = None,
        bond_length: float = BOND_LENGTH,
        iteration_limit: int = ITERATION_LIMIT,
        periodic: bool = True,
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Gets coordinates of the molecular graph in 3D-box

        Args:
            fixed_coords (Optional[Dict[int, Tuple[float,float,float]]]): list of fixed beads
            box (Box): instance of box
            bond_length (float, optional): Defaults to BOND_LENGTH.
            iteration_limit (int, optional): Defaults to ITERATION_LIMIT.
            periodic (bool, optional): False if graph in impenetrable box. Defaults to True.

        Raises:
            FixedRootError: First id of fixed beads not equal 0
            FixedDictError: Fixed beads is out of range (0, num_beads)
            FixedOutBoxError: Coordinates of fixed beads out box

        Returns:
            Tuple[np.ndarray, np.ndarray, np.ndarray]: x, y, z coordinates
        """
        x = np.random.uniform(-box.x / 2, box.x / 2, self.num_beads)
        y = np.random.uniform(-box.y / 2, box.y / 2, self.num_beads)
        z = np.random.uniform(-box.z / 2, box.z / 2, self.num_beads)
        if fixed_coords:
            if 0 in fixed_coords:
                if len(fixed_coords) == 1:
                    only_id0_fixed = True
                else:
                    only_id0_fixed = False
            else:
                raise FixedRootError
            if any([(i < 0 and i >= self.num_beads) for i in fixed_coords]):
                raise FixedDictError
            for id in fixed_coords:
                x[id], y[id], z[id] = fixed_coords[id]
                if not box.check_in_box(x[id], y[id], z[id]):
                    raise FixedOutBoxError
        else:
            fixed_coords = {0: (x[0], y[0], z[0])}
            only_id0_fixed = True

        if only_id0_fixed and self.directed and (not self.cyclical):
            # sequential graph generation
            for bond in self.bonds:
                label_to_break = False
                num_iter = 0
                while not label_to_break:
                    num_iter += 1
                    if num_iter > iteration_limit:
                        raise IterationLimitError(iteration_limit)
                    v = rnd_vector(length=bond_length)
                    xt = x[bond[0]] + v[0]
                    yt = y[bond[0]] + v[1]
                    zt = z[bond[0]] + v[2]
                    if not box.check_in_box(xt, yt, zt):
                        if periodic:
                            xt, yt, zt = box.periodic_correct(xt, yt, zt)
                            label_to_break = True
                    else:
                        label_to_break = True
                    if label_to_break:
                        x[bond[1]] = xt
                        y[bond[1]] = yt
                        z[bond[1]] = zt
                        break
        else:
            ## random graph generation (only without periodic conditions)
            r_max: float = bond_length * 2
            r_min: float = 0.0
            fx = np.zeros(self.num_beads)
            fy = np.zeros(self.num_beads)
            fz = np.zeros(self.num_beads)
            num_iter = 0
            while r_max - r_min > bond_length * EPS:
                num_iter += 1
                if num_iter > iteration_limit:
                    raise IterationLimitError(iteration_limit)
                fx[:] = 0.0
                fy[:] = 0.0
                fz[:] = 0.0
                r_max = 0.0
                r_min = bond_length * 2
                for b in self.bonds:
                    dx = x[b[0]] - x[b[1]]
                    dy = y[b[0]] - y[b[1]]
                    dz = z[b[0]] - z[b[1]]
                    r = np.sqrt(dx**2 + dy**2 + dz**2)
                    if r > r_max:
                        r_max = r
                    if r < r_min:
                        r_min = r
                    f = repulsive_force(bond_length, r)
                    fx[b[0]] += f * dx
                    fx[b[1]] -= f * dx
                    fy[b[0]] += f * dy
                    fy[b[1]] -= f * dy
                    fz[b[0]] += f * dz
                    fz[b[1]] -= f * dz
                for i in range(self.num_beads):
                    if i not in fixed_coords:
                        xt = x[i] + fx[i]
                        yt = y[i] + fy[i]
                        zt = z[i] + fz[i]
                        if box.check_in_box(xt, yt, xt):
                            x[i], y[i], z[i] = xt, yt, zt
        return x, y, z
