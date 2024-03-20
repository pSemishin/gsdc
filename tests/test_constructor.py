from typing import Final

import pytest

from gsdc import Box, MolGraph
from gsdc.bondset import LINEAR

box = Box(2.0, 2.0, 2.0)
graph = MolGraph(bonds=LINEAR, sort=True)
bond_length: float = 1.0
EPS: Final[float] = 1e-8


@pytest.mark.parametrize("graph, box, bond_length", [(graph, box, bond_length)])
def test_get_coords(graph: MolGraph, box: Box, bond_length) -> None:
    (x, y, z) = graph.get_coords(box=box, periodic=False, bond_length=bond_length)
    for xb, yb, zb in zip(x, y, z):
        assert box.check_in_box(xb, yb, zb)
    for bond in graph.bonds:
        dx = x[bond[0]] - x[bond[1]]
        dy = y[bond[0]] - y[bond[1]]
        dz = z[bond[0]] - z[bond[1]]
        r = dx**2 + dy**2 + dz**2
        assert abs(r - bond_length**2) < EPS
