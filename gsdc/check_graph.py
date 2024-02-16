from typing import Dict, Set

from .bondset import Bondtype
from .exceptions import NegativeValueError


class CheckGraph:
    """Pre-check of any molecular graph"""

    @staticmethod
    def is_not_gaps(bonds: Bondtype) -> bool:
        """
        Detects gaps or invalid value in node enum,

        bonds-list can be empty, but node ids must

        i) be enumerated from 0 to max id without gaps,

        ii) contain only non-negative integers

        Args:
            bonds (List[Tuple[int,int]]): list of bonded node ids

        Raises:
            NegativeValueError: if a negative id is found
        Returns:
            bool: True if there are no gaps, False otherwise
        """
        nodes = set([bond[0] for bond in bonds] + [bond[1] for bond in bonds])
        if any([i < 0 for i in nodes]):
            raise NegativeValueError
        num_nodes = len(nodes)
        return num_nodes * (num_nodes - 1) / 2 == sum(nodes)

    @staticmethod
    def is_simple(bonds: Bondtype) -> bool:
        """
        Checks for the absence of multiple and cyclic edges

        Likes that: (1, 2) and (2, 1) or (0, 0), (1, 1) etc.

        Args:
            bonds (List[Tuple[int,int]]): list of bonded node ids

        Returns:
            bool: True if the graph is simple or empty, False otherwise
        """
        new_bonds: Bondtype = bonds + [(bond[1], bond[0]) for bond in bonds]
        return len(new_bonds) == len(set(new_bonds))

    @staticmethod
    def is_connected(bonds: Bondtype) -> bool:
        """
        Full graph traversal to detect that it's connected

        (i.e. there is a path from any node to any node)

        Args:
            bonds (List[Tuple[int,int]]): list of bonded node ids

        Returns:
            bool: True if graph is connected,
                    False if it is disconnected or empty
        """
        label: Dict = dict()
        for bond in bonds:
            if bond[0] not in label:
                label[bond[0]] = 0
            if bond[1] not in label:
                label[bond[1]] = 0
        counter: int = 0
        cluster: Dict = dict()
        minimum: int
        maximum: int
        for bond in bonds:
            if label[bond[0]] == label[bond[1]]:
                if label[bond[0]] == 0:
                    counter += 1
                    label[bond[0]] = counter
                    label[bond[1]] = counter
                    cluster[counter] = [bond[0], bond[1]]
            else:
                if label[bond[0]] == 0 and label[bond[1]] != 0:
                    label[bond[0]] = label[bond[1]]
                    cluster[label[bond[0]]].append(bond[0])
                elif label[bond[1]] == 0 and label[bond[0]] != 0:
                    label[bond[1]] = label[bond[0]]
                    cluster[label[bond[1]]].append(bond[1])
                else:
                    minimum = min(label[bond[1]], label[bond[0]])
                    maximum = max(label[bond[1]], label[bond[0]])
                    cluster[minimum] = cluster[minimum] + cluster[maximum]
                    for clust in cluster[maximum]:
                        label[clust] = minimum
                    cluster.pop(maximum)
        return len(cluster) == 1

    @staticmethod
    def is_directed(bonds: Bondtype) -> bool:
        """
        Checks the possibility of constructing a <<directed>> graph

        (the first id must be listed before the second in the bonds list)
            Directed:     [(0, 1), (1, 2), (2, 3)]
            Not directed: [(0, 1), (2, 1), (2, 3)]

        Args:
            bonds (List[Tuple[int,int]]): list of bonded node ids

        Returns:
            bool: True if graph is connected,
                    False if it is disconnected or empty
        """
        if bonds:
            painted: Set = set()
            painted.add(bonds[0][0])
            for bond in bonds:
                if bond[0] in painted:
                    painted.add(bond[1])
                else:
                    return False
            return True
        return False
