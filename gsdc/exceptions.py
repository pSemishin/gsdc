from typing import Optional


class NegativeValueError(Exception):
    def __str__(self):
        return "Some node in grpah is negative"


class GapsMolGraphError(Exception):
    def __str__(self):
        return "Gaps in indexation were detected"


class MolGraphSimplicityError(Exception):
    def __str__(self):
        return "Graph is not simple"


class MolGraphConnectionError(Exception):
    def __str__(self):
        return "Graph is not connected"


class OutBoxError(Exception):
    def __str__(self):
        return "Some bead occure out of box > 1.5 box"


class FixedRootError(Exception):
    def __str__(self):
        return "First id in dictonary of fixed beads most be equal 0"


class FixedDictError(Exception):
    def __str__(self):
        return "Dictonary of fixed beads is out of range (0, num_beads)"


class FixedOutBoxError(Exception):
    def __str__(self):
        return "Fixed bead occure out of box > 0.5 box"


class EmptyGraphError(Exception):
    def __str__(self):
        return "Graph is empty"


class IterationLimitError(Exception):
    def __init__(self, iteration_limit: Optional[int] = None):
        if iteration_limit:
            self.message: str = "< " + str(iteration_limit)
        else:
            self.message = str("see MolGraph.get_coords info")

    def __str__(self):
        return f"Iteration limit is over ({self.message})"
