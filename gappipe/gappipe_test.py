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

    f = e[1:-1]
    assert (len(f) == 4)
    assert (f[0] == "two")
    assert (f[-1] == "three")

    assert (f[-1:][0] == "three")
    assert (f[-1:42][0] == "three")
    assert (f[:1][0] == "two")
    assert (len(f[:]) == len(f))

    assert (len(e[1:1]) == 0)
    assert (len(e[42:0]) == 0)

    try:
        e[len(e)]
        assert (False)
    except IndexError:
        pass

    try:
        e[-len(e) - 1]
        assert (False)
    except IndexError:
        pass


def test_factored_array_iter():
    size = 42

    a = FactoredArray()
    for i in range(1, size):
        a += FactoredArray(i, i)

    assert (len(a) == size * (size - 1) // 2)

    it = iter(a)

    for i in range(1, size):
        for _ in range(i):
            assert (next(it) == i)

    try:
        next(it)
        assert (False)
    except StopIteration:
        pass

    for i, (val, sz) in enumerate(a.chunks()):
        assert (i + 1 == val)
        assert (i + 1 == sz)


def test_factored_array_misc():
    a = FactoredArray()
    a += FactoredArray()
    assert (len(a) == 0)


def test_factored_array_str():
    a = FactoredArray()
    assert (str(a) == 'FactoredArray()')

    a = FactoredArray(1, 2)
    assert (str(a) == 'FactoredArray((1, 2))')
