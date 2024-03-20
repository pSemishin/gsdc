import pytest

from gsdc import check_script


@pytest.mark.parametrize(
    "script_with_error",
    [
        ("(X-x)1(G)99"),
        ("(Xx)1 (G)99"),
        ("(X))1(G)99"),
        ("(X)1[(G)99"),
        ("x(X)1(G)99"),
        ("(X)1(G)99x"),
        ("(X)1(G)(A)99"),
        ("()1(G)99"),
        ("(X)1(A)x(G)1"),
        ("(X)1(A)02(G)1"),
        ("(1X)1(A)2(G)1"),
        ("(X)1[A]2(G)1"),
        ("(X)1(a)1[(x)1)1A((b)2](G)1"),
        ("(X)1(a)1[(A)1a](a)2(G)1"),
        ("(X)1(a)1[(A)1a1](a)2(G)1"),
        ("(X)1(a)1[(A](a)2)1(G)1"),
    ],
)
def test_check_script_false(script_with_error: str) -> None:
    assert check_script(script_with_error) != "No errors"


@pytest.mark.parametrize(
    "script_without_error",
    [
        ("(H)1(O)1(H)1"),
        ("(A)2[(A)2[(A)2](A)2](A)2"),
        ("(Na)1(C0)1[(O)1]((C)1([(H)1])2)3(O)1(H)1"),
    ],
)
def test_check_script_true(script_without_error: str) -> None:
    assert check_script(script_without_error) == "No errors"
