from typing import List, Optional, Tuple


def bonds_parser(script: str) -> List[Tuple[int, int]]:
    """_summary_

    Args:
        script (str): topological script defining the molecule,
        sample: "(Na)1(C0)1[(O)1]((C)1([(H)1])2)3(O)1(H)1"

    Returns:
        List[Tuple[int, int]]: list of connected pairs of beads,
        sample: [(0,1), (1,2), (1,3), (3,4), (3,5), (3,6), (6,7), (6,8), (6,9), (9,10), (9,11), (9,12), (12,13)]
    """

    # (1) erasing the atom symbols along with the brackets around them
    index_br_open: Optional[int] = None
    list_script = list(script)

    for i, symbol in enumerate(script):
        if symbol == "(":
            index_br_open = i

        if symbol == ")" and index_br_open is not None:
            for j in range(index_br_open, i + 1):
                list_script[j] = " "
            index_br_open = None

    # (2) combining consecutive digits into numbers if it's necessary
    script = "".join(list_script)
    list_script = []
    label = False
    for el in script:
        if el == " ":
            label = False
            continue
        elif el in "()[]":
            label = False
            list_script.append(el)
        elif el.isdigit():
            if label:
                list_script[-1] += el
            else:
                list_script.append(el)
            label = True

    # (3) "openning" the brackets ( and )
    index_br_open = None
    while ")" in list_script:
        for i, symbol in enumerate(list_script):
            if symbol == "(":
                index_br_open = i

            if symbol == ")" and index_br_open is not None:
                if len(list_script) >= i + 2:
                    list_script = (
                        list_script[0:index_br_open]
                        + list_script[index_br_open + 1 : i] * int(list_script[i + 1])
                        + list_script[i + 2 :]
                    )
                else:
                    list_script = list_script[0:index_br_open] + list_script[
                        index_br_open + 1 : i
                    ] * int(list_script[i + 1])
                index_br_open = None

    # (4) adding consecutive numbers not separated by brackets
    tmp_list = [""]
    for s in list_script:
        if tmp_list[-1].isdigit() and s.isdigit():
            tmp_list[-1] = str(int(tmp_list[-1]) + int(s))
        else:
            tmp_list.append(s)
    script = "".join(tmp_list)
    list_script = (
        script.replace("[", "*[*").replace("]", "*]*").replace("**", "*").split("*")
    )

    # (5) building a blob connection graph using script with square brackets
    blob_bonds = []
    numbers = set()
    numbers.add(0)
    brackets_counter = 0
    for i, s in enumerate(list_script[1:]):
        if s.isdigit():
            brackets_counter = 0
            for j in range(i, -1, -1):
                if list_script[j] == "]":
                    brackets_counter += 1
                if list_script[j] == "[":
                    brackets_counter -= 1
                if (
                    list_script[j].isdigit()
                    and brackets_counter <= 0
                    and list_script[j + 1] == "["
                ):
                    blob_bonds.append((j, i + 1))
                    numbers.add(j)
                    numbers.add(i + 1)
                    break

    # (6) collecting the list of bonds
    n = -1
    bonds = []
    blob = dict()
    for i in sorted(list(numbers)):
        p = int(list_script[i])
        for j in range(n + 1, n + p):
            bonds.append((j, j + 1))
        blob[i] = (n + 1, n + p)
        n += p

    for b in blob_bonds:
        bonds.append((blob[b[0]][1], blob[b[1]][0]))

    return sorted(bonds)


if __name__ == "__main__":
    print(bonds_parser("(Na)1(C0)1[(O)1]((C)1([(H)1])2)3(O)1(H)1"))
    print(bonds_parser("(H)1(O)1(H)1"))
