from csg2csg.Vector import add, cross, subtract


def test_subtract():
    a = [1, 0, 0]
    b = [1, 0, 0]
    c = subtract(a, b)

    assert c[0] == 0.0
    assert c[1] == 0.0
    assert c[2] == 0.0


def test_add():
    a = [1, 0, 0]
    b = [0, 1, 0]
    c = add(a, b)

    assert c[0] == 1.0
    assert c[1] == 1.0
    assert c[2] == 0.0


def test_cross():
    a = [1, 0, 0]
    b = [0, 1, 0]
    c = cross(a, b)

    assert c[0] == 0.0
    assert c[1] == 0.0
    assert c[2] == 1.0
