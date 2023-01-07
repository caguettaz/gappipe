from gappipe import *


def test_factored_array_basic():
    a = FactoredArray()
    assert (len(a) == 0)

    b = FactoredArray(None, 1)
    assert (len(b) == 1)
    assert (len(a + b) == 1)

    c = FactoredArray("hihi", 2)
    assert (len(c) == 2)
    assert (len(b + c) == 3)

    d = FactoredArray("hihi", 3)
    assert (len(c + d) == 5)

    e = FactoredArray("one", 1) + FactoredArray("two", 2) + FactoredArray("three", 3)
    assert (len(e) == 6)
    assert (e[0] == "one")
    assert (e[1] == "two")
    assert (e[2] == "two")
    assert (e[3] == "three")
    assert (e[-1] == "three")
    assert (e[-4] == "two")
    assert (e[-6] == "one")
