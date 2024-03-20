from .bonds_parser import bonds_parser
from .check_script import check_script
from .constructor import MolGraph
from .types_parser import types_parser


class Mol(MolGraph):
    def __init__(self, script: str) -> None:
        if check_script(script) != "No errors":
            raise ValueError(f"{script}: is not correct")
        self.types = types_parser(script)
        self.bonds = bonds_parser(script)
        super().__init__(self.bonds)
