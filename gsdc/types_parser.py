from typing import List

import sympy


def types_parser(script: str) -> List[str]:
    """_summary_

    Args:
        script (str): topological script defining the molecule,
        sample: "(Na)1(C0)1[(O)1]((C)1([(H)])2)3(O)1(H)1"

    Returns:
        List[str]: list of beads (atoms) types,
        sample: ['Na', 'C0', 'O', 'C', 'H', 'H', 'C', 'H', 'H', 'C', 'H', 'H', 'O', 'H']
    """

    indexes = list()
    index_br_close = 0
    index_br_open = 0
    for i, symbol in enumerate(script[::-1]):
        # print(len(script) - i -1, "  ", symbol)
        if symbol == ")":
            index_br_close = len(script) - i - 1

        if symbol == "(" and index_br_close != 0:
            index_br_open = len(script) - i - 1
            indexes.append(index_br_open)
            indexes.append(index_br_close)
            index_br_close = 0
    indexes_set = set(indexes)

    new_script = str()
    for i, symbol in enumerate(script):
        if i in indexes_set:
            new_script += "'"
        elif symbol in "[]":
            pass
        else:
            new_script += symbol

    formula = str()
    for i, symbol in enumerate(new_script):
        if symbol == ")":
            formula += f"{symbol}*"
        elif symbol == "(":
            formula += f"+{symbol}"
        elif (
            symbol == "'"
            and not new_script[i + 1].isdigit()
            and i != 0
            and new_script[i - 1] != "("
            and new_script[i + 1] != ")"
        ):
            formula += f"+{symbol}"

        elif symbol == "'" and new_script[i + 1].isdigit():
            formula += f"{symbol}*"
        else:
            formula += symbol

    exprssion = str()
    label = 1
    for s in formula:
        if s == "'":
            if label == 1:
                exprssion += "['"
                label = -label
            else:
                exprssion += "']"
                label = -label
        else:
            exprssion += s

    return sympy.sympify(exprssion)


if __name__ == "__main__":
    print(types_parser("(Na)1(C0)1[(O)1]((C)1([(H)])2)3(O)1(H)1"))
