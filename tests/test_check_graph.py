import pytest

from gsdc import CheckGraph, NegativeValueError, bondset


class TestCheckGraph:
    @pytest.mark.parametrize(
        "bonds, expected_result",
        [
            (bondset.EMPTY, True),
            (bondset.LINEAR, True),
            (bondset.GAP_ENUM, False),
        ],
    )
    def test_is_not_gaps(self, bonds: bondset.Bondtype, expected_result: bool) -> None:
        assert CheckGraph.is_not_gaps(bonds) == expected_result

    @pytest.mark.parametrize(
        "bonds",
        [
            (bondset.NEGATIVE),
        ],
    )
    def test_is_not_gaps_raises(self, bonds: bondset.Bondtype) -> None:
        with pytest.raises(NegativeValueError) as err:
            CheckGraph.is_not_gaps(bonds)
        assert "Some node in grpah is negative" in str(err.value)

    @pytest.mark.parametrize(
        "bonds, expected_result",
        [
            (bondset.EMPTY, True),
            (bondset.LINEAR, True),
            (bondset.GAP_ENUM, True),
            (bondset.NEGATIVE, True),
            (bondset.DOUBLE_BOND, False),
            (bondset.CYCLIC_EDGE, False),
        ],
    )
    def test_is_simple(self, bonds: bondset.Bondtype, expected_result: bool) -> None:
        assert CheckGraph.is_simple(bonds) == expected_result

    @pytest.mark.parametrize(
        "bonds, expected_result",
        [
            (bondset.EMPTY, False),
            (bondset.LINEAR, True),
            (bondset.GAP_ENUM, True),
            (bondset.NEGATIVE, True),
            (bondset.DOUBLE_BOND, True),
            (bondset.CYCLIC_EDGE, False),
            (bondset.NOT_CONNECT, False),
        ],
    )
    def test_is_connected(self, bonds: bondset.Bondtype, expected_result: bool) -> None:
        assert CheckGraph.is_connected(bonds) == expected_result

    @pytest.mark.parametrize(
        "bonds, expected_result",
        [
            (bondset.EMPTY, False),
            (bondset.LINEAR, True),
            (bondset.GAP_ENUM, False),
            (bondset.NEGATIVE, True),
            (bondset.DOUBLE_BOND, True),
            (bondset.CYCLIC_EDGE, False),
            (bondset.NOT_CONNECT, False),
            (bondset.NOT_DIRECTED, False),
        ],
    )
    def test_is_directed(self, bonds: bondset.Bondtype, expected_result: bool) -> None:
        assert CheckGraph.is_directed(bonds) == expected_result
