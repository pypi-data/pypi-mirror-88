# Test suite for AD2020Root module

import sys
sys.path.append('./AD2020')

import pytest
import numpy as np

from AD2020 import AD2020
from AD2020Fun import AD2020Fun
from AD2020Root import Find

def test_AD2020Root_univ():
    '''Test for 1 to 1'''

    def test_1():
        def f(x):
            return (x - 1) ** 2

        x0 = AD2020(2)
        root = Find(f, x0)
        assert np.isclose(root, 1)

    def test_2():
        def f(x):
            return - ((x + 1) ** 2) + 1

        x0 = AD2020(4)
        root = Find(f, x0)
        assert np.isclose(root, 0)

        x0 = AD2020(-4)
        root = Find(f, x0)
        assert np.isclose(root, -2)

    def test_3():
        def f(x):
            return (x - 1) ** 3 + 4

        x0 = AD2020(0)
        root = Find(f, x0)
        assert np.isclose(root, np.cbrt(-4) + 1)

    def test_4():
        def f(x):
            return (x + 1) ** 4 - 2

        x0 = AD2020(0)
        root = Find(f, x0)
        assert np.isclose(root, np.power(2, 1/4) - 1)

        x0 = AD2020(-2)
        root = Find(f, x0)
        assert np.isclose(root, - np.power(2, 1/4) - 1)

    def test_5():
        def f(x):
            return x + AD2020Fun.sin(AD2020Fun.exp(x)) - 1

        x0 = AD2020(0)
        root = Find(f, x0)
        assert np.isclose(root, 0.10432071)

        x0 = AD2020(1)
        root = Find(f, x0)
        assert np.isclose(root, 1.20986396)

        x0 = AD2020(2)
        root = Find(f, x0)
        assert np.isclose(root, 1.70490978)

    test_1()
    test_2()
    test_3()
    test_4()
    test_5()

def test_AD2020Root_multv():
    '''Test for m to 1'''

    def test_1():
        def f(var):
            x, y = var
            return x + y

        x0 = AD2020(2, [1,0])
        y0 = AD2020(5, [0,1])
        vars = [x0, y0]
        root = Find(f, vars)
        assert root[0] == - root[1]

    def test_2():
        def f(var):
            x, y = var
            return x ** 2 - y ** 2

        x0 = AD2020(-2, [1,0])
        y0 = AD2020(5, [0,1])
        vars = [x0, y0]
        root = Find(f, vars)
        assert abs(root[0]) == abs(root[1])

    def test_3():
        def f(var):
            x, y = var
            return (x ** 2 + y ** 2) - 1

        x0 = AD2020(-2, [1,0])
        y0 = AD2020(1, [0,1])
        vars = [x0, y0]
        root = Find(f, vars)
        assert np.isclose(root[0] ** 2 + root[1] ** 2, 1)

    def test_4():
        def f(var):
            x, y, z = var
            return (x - 1) ** 2 + (y + 2) ** 2 + (z * 2) ** 2

        x0 = AD2020(-2, [1,0,0])
        y0 = AD2020(1, [0,1,0])
        z0 = AD2020(1, [0,0,1])
        vars = [x0, y0, z0]
        root = Find(f, vars)
        assert np.all(np.round(root,2) == [[1.],[-2.],[0.]])

    def test_5():
        def f(var):
            x, y, z = var
            return (x - y) ** 2 - z

        x0 = AD2020(-2, [1,0,0])
        y0 = AD2020(1, [0,1,0])
        z0 = AD2020(1, [0,0,1])
        vars = [x0, y0, z0]
        root = Find(f, vars)
        assert np.isclose(abs(root[0] - root[1]), np.sqrt(root[2]))

    test_1()
    test_2()
    test_3()
    test_4()
    test_5()

def test_AD2020Root_excep():
    '''Test for exception'''

    with pytest.raises(Exception):
        def f(x):
            return (x - 1) ** 2

        x0 = 2
        root = Find(f, x0)

test_AD2020Root_univ()
test_AD2020Root_multv()
test_AD2020Root_excep()

print('Passed All Tests!')
