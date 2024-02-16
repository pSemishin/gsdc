from typing import Final, List, Tuple

Bondtype = List[Tuple[int, int]]

EMPTY: Final[Bondtype] = []
LINEAR: Final[Bondtype] = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5)]
GAP_ENUM: Final[Bondtype] = [(0, 1), (3, 0), (1, 3)]
NEGATIVE: Final[Bondtype] = [(-1, 0), (0, 1), (1, 2)]
DOUBLE_BOND: Final[Bondtype] = [(1, 2), (2, 1)]
CYCLIC_EDGE: Final[Bondtype] = [(0, 0), (1, 1), (2, 2)]
NOT_CONNECT: Final[Bondtype] = [(1, 2), (2, 1), (0, 3), (3, 4)]
NOT_DIRECTED: Final[Bondtype] = [(0, 1), (2, 1), (2, 3)]
DENDRON: Final[Bondtype] = [
    (0, 1),
    (1, 2),
    (2, 3),
    (3, 4),
    (2, 5),
    (5, 6),
    (4, 7),
    (7, 8),
    (4, 9),
    (9, 10),
    (6, 11),
    (11, 12),
    (6, 13),
    (13, 14),
]
