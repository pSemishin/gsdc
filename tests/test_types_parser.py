from typing import List

import pytest

from gsdc import types_parser


@pytest.mark.parametrize(
    "script, expected_result",
    [
        ("(H)1(O)1(H)1", ["H", "O", "H"]),
        ("(A)2[(A)2[(A)2](A)2](A)2", ["A"] * 10),
        (
            "(Na)1(C0)1[(O)1]((C)1([(H)1])2)3(O)1(H)1",
            ["Na", "C0", "O", "C", "H", "H", "C", "H", "H", "C", "H", "H", "O", "H"],
        ),
    ],
)
def test_types_parser(script: str, expected_result: List[str]) -> None:
    assert types_parser(script) == expected_result
