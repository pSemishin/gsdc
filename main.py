from gsdc import Box, Mol, Pot

if __name__ == "__main__":
    script = "(A)2"
    mol = Mol(script)
    box = Box(20.0, 20.0, 20.0)
    pot = Pot(box)
    pot.add(mol)
    pot.add_bead("B")
    pot.brew()
    print(pot.types)
    print(pot.coords)
    print(len(pot.coords))
