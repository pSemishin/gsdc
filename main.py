from gsdc import Box, Mol, Pot
import time

if __name__ == "__main__":
    script = "(A)2"
    mol = Mol(script)
    box = Box(20.0, 20.0, 20.0)
    pot = Pot(box)
    # pot.add(mol)
    # pot.add_bead("B")
    t1 = time.time()
    for _ in range(24000):
        pot.add_bead('B')
    pot.brew()
    t2 = time.time()
    # print(pot.types)
    # print(pot.coords)
    # print(len(pot.coords))
    print(t2-t1)