from mypkg.mathx import add, average


def test_add():
    assert add(2, 3) == 5


def test_average_normal():
    assert average([1, 2, 3]) == 2.0


def test_average_empty():
    assert average([]) == 0