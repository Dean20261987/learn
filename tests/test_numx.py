import pytest

from mytools.numx import is_even


@pytest.mark.parametrize("n, expected", [
    (0, True),
    (6, True),
    (-4, True),
    (7, False),
    (-3, False),
])
def test_is_even(n, expected):
    assert is_even(n) is expected