import time

from gsdc import Box, Mol, Pot

if __name__ == "__main__":
    script = "(A)1[(B)2](A)2"
    mol = Mol(script)
    box = Box(10.0, 10.0, 10.0)
    pot = Pot(box)
    pot.add(mol)
    pot.add(mol)
    solvent = "W"
    pot.fuller(solvent)
    pot.brew()
    pot.dl_meso_config()
    pot.dl_meso_field()
