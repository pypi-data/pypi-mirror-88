# Test suite for AD2020Fun module

import sys
sys.path.append('./AD2020')

import pytest
import numpy as np

from AD2020 import AD2020
from AD2020Fun import AD2020Fun

def test_AD2020Fun_scalar():

    def test_exp():
        x = AD2020(2, 1)
        f1 = 2 * AD2020Fun.exp(x) + 1
        f2 = 2 * AD2020Fun.exp(x,3) + 1
        assert np.round(f1.value, 2) == 15.78
        assert np.round(f1.derivative, 2) == 14.78
        assert np.round(f2.value, 2) == 19
        assert np.round(f2.derivative, 2) == 19.78

        with pytest.raises(ValueError):
            f0 = AD2020Fun.exp(x,-4)
        with pytest.raises(ZeroDivisionError):
            x0 = AD2020(-2, 1)
            f0 = AD2020Fun.exp(x0,0)

    def test_log():
        x = AD2020(2, 1)
        f1 = 2 * AD2020Fun.log(x) + 1
        f2 = 2 * AD2020Fun.log(x,10) + 1
        assert np.round(f1.value, 2) == 2.39
        assert np.round(f1.derivative, 2) == 1
        assert np.round(f2.value, 2) == 1.60
        assert np.round(f2.derivative, 2) == 0.43

        with pytest.raises(ValueError):
            x0 = AD2020(0, 1)
            f0 = 2 * AD2020Fun.log(x0) + 1
        with pytest.raises(ValueError):
            x0 = AD2020(-2, 1)
            f0 = 2 * AD2020Fun.log(x0) + 1

    def test_sin():
        x = AD2020(2, 1)
        f = 2 * AD2020Fun.sin(x) + 1
        assert np.round(f.value, 2) == 2.82
        assert np.round(f.derivative, 2) == -0.83

    def test_cos():
        x = AD2020(2, 1)
        f = 2 * AD2020Fun.cos(x) + 1
        assert np.round(f.value, 2) == 0.17
        assert np.round(f.derivative, 2) == -1.82

    def test_tan():
        x = AD2020(2, 1)
        f = 2 * AD2020Fun.tan(x) + 1
        assert np.round(f.value, 2) == -3.37
        assert np.round(f.derivative, 2) == 11.55

        with pytest.raises(ValueError):
            x0 = AD2020(np.pi/2, 1)
            f0 = 2 * AD2020Fun.tan(x0) + 1

    def test_arcsin():
        x = AD2020(0, 1)
        f = 2 * AD2020Fun.arcsin(x) + 1
        assert f.value == 1
        assert f.derivative == 2

        with pytest.raises(ValueError):
            x0 = AD2020(-2, 1)
            f0 = 2 * AD2020Fun.arcsin(x0) + 1

    def test_arccos():
        x = AD2020(0, 1)
        f = 2 * AD2020Fun.arccos(x) + 1
        assert f.value == 1 + np.pi
        assert f.derivative == -2

        with pytest.raises(ValueError):
            x0 = AD2020(-2, 1)
            f0 = 2 * AD2020Fun.arccos(x0) + 1

    def test_arctan():
        x = AD2020(2, 1)
        f = 2 * AD2020Fun.arctan(x) + 1
        assert np.round(f.value, 2) == 3.21
        assert np.round(f.derivative, 2) == 0.4

    def test_sinh():
        x = AD2020(2, 1)
        f = 2 * AD2020Fun.sinh(x) + 1
        assert np.round(f.value, 2) == 8.25
        assert np.round(f.derivative, 2) == 7.52

    def test_cosh():
        x = AD2020(2, 1)
        f = 2 * AD2020Fun.cosh(x) + 1
        assert np.round(f.value, 2) == 8.52
        assert np.round(f.derivative, 2) == 7.25

    def test_tanh():
        x = AD2020(2, 1)
        f = 2 * AD2020Fun.tanh(x) + 1
        assert np.round(f.value, 2) == 2.93
        assert np.round(f.derivative, 2) == 0.14

    def test_logistic():
        x = AD2020(2, 1)
        f = 2 * AD2020Fun.logistic(x) + 1
        assert np.round(f.value, 2) == 2.76
        assert np.round(f.derivative, 2) == 0.21

    def test_sqrt():
        x = AD2020(2, 1)
        f = 2 * AD2020Fun.sqrt(x) + 1
        assert np.round(f.value, 2) == 3.83
        assert np.round(f.derivative, 2) == 0.71

        with pytest.raises(ValueError):
            x0 = AD2020(-2, 1)
            f0 = AD2020Fun.sqrt(x0)

        with pytest.raises(ZeroDivisionError):
            x0 = AD2020(0, 1)
            f0 = AD2020Fun.sqrt(x0)

    test_exp()
    test_log()
    test_sin()
    test_cos()
    test_tan()
    test_arcsin()
    test_arccos()
    test_arctan()
    test_sinh()
    test_cosh()
    test_tanh()
    test_logistic()
    test_sqrt()

def test_AD2020Fun_vector():

    def test_exp():
        x = AD2020([1],[1,0,0])
        y = AD2020([2],[0,1,0])
        z = AD2020([3],[0,0,1])
        f1 = AD2020Fun.exp(x) + 2*y + z
        f2 = AD2020([AD2020Fun.exp(x), AD2020Fun.exp(x+y), AD2020Fun.exp(x+z)])
        f3 = AD2020([AD2020Fun.exp(x,3), x+y, z*2])
        assert f1 == AD2020(np.e+7, [np.e,2,1])
        assert np.all(np.round(f2.value,2) == np.round([np.e**1,np.e**3,np.e**4],2))
        assert np.all(np.round(f2.derivative,2) == np.round([[np.e**1,0,0],[np.e**3,np.e**3,0],[np.e**4,0,np.e**4]],2))
        assert np.all(f3.value == [3,3,6])
        assert np.all((np.round(f3.derivative,2) == [[3.30,0,0],[1,1,0],[0,0,2]]))

        with pytest.raises(ValueError):
            f0 = AD2020Fun.exp(x,-4)
        with pytest.raises(ZeroDivisionError):
            x0 = AD2020(-2, [1,0,0])
            f0 = AD2020Fun.exp(x0,0)

    def test_log():
        x = AD2020([1],[1,0,0])
        y = AD2020([2],[0,1,0])
        z = AD2020([3],[0,0,1])
        f1 = AD2020Fun.log(x) + 2*y + z
        f2 = AD2020([AD2020Fun.log(x), AD2020Fun.log(x+y), AD2020Fun.log(x+z)])
        f3 = AD2020([AD2020Fun.log(x,10), AD2020Fun.log(x+y,10), z*2])
        assert f1 == AD2020(7, [1,2,1])
        assert np.all(np.round(f2.value,2) == np.round([0,np.log(3),np.log(4)],2))
        assert np.all(np.round(f2.derivative,2) == np.round([[1,0,0],[1/3,1/3,0],[0.25,0,0.25]],2))
        assert np.all(np.round(f3.value,2) == [0,0.48,6])
        assert np.all((np.round(f3.derivative,2) == [[0.43,0,0],[0.14,0.14,0],[0,0,2]]))

        with pytest.raises(ValueError):
            x0 = AD2020([-1],[1,0,0])
            f0 = AD2020Fun.log(x0)
        with pytest.raises(ZeroDivisionError):
            f0 = AD2020Fun.log(x,0)

    def test_sin():
        x = AD2020([np.pi/2],[1,0,0])
        y = AD2020([2],[0,1,0])
        z = AD2020([3],[0,0,1])
        f1 = AD2020Fun.sin(x) + 2*y + z
        f2 = AD2020([2*AD2020Fun.sin(x), AD2020Fun.sin(x+y), AD2020Fun.sin(x+z)])
        assert f1.value == 8
        assert np.all(np.round(f1.derivative,2) == [0,2,1])
        assert np.all(np.round(f2.value,2) == [2,-0.42,-0.99])
        assert np.all(np.round(f2.derivative,2) == [[0,0,0],[-0.91,-0.91,0],[-0.14,0,-0.14]])

    def test_cos():
        x = AD2020([np.pi/2],[1,0,0])
        y = AD2020([2],[0,1,0])
        z = AD2020([3],[0,0,1])
        f1 = AD2020Fun.cos(x) + 2*y + z
        f2 = AD2020([2*AD2020Fun.cos(x), AD2020Fun.cos(x+y), AD2020Fun.cos(x+z)])
        assert f1 == AD2020(7, [-1,2,1])
        assert np.all(np.round(f2.value,2) == [0,-0.91,-0.14])
        assert np.all(np.round(f2.derivative,2) == [[-2,0,0],[0.42,0.42,0],[0.99,0,0.99]])

    def test_tan():
        x = AD2020([np.pi/3],[1,0,0])
        y = AD2020([2],[0,1,0])
        z = AD2020([3],[0,0,1])
        f1 = AD2020Fun.tan(x) + 2*y + z
        f2 = AD2020([2*AD2020Fun.tan(x), AD2020Fun.tan(x+y), AD2020Fun.tan(2*x+z)])
        assert np.round(f1.value,2) == 8.73
        assert np.all(np.round(f1.derivative,2) == [4,2,1])
        assert np.all(np.round(f2.value,2) == [3.46,-0.09,-2.49])
        assert np.all(np.round(f2.derivative,2) == [[8,0,0],[1.01,1.01,0],[14.39,0,7.20]])

        with pytest.raises(ValueError):
            x0 = AD2020(np.pi/2, [1,0,0])
            f0 = 2 * AD2020Fun.tan(x0) + 1

    def test_arcsin():
        x = AD2020([0],[1,0,0])
        y = AD2020([-0.5],[0,1,0])
        z = AD2020([0.5],[0,0,1])
        f1 = AD2020Fun.arcsin(x) + 2*y + z
        f2 = AD2020([2*AD2020Fun.arcsin(x), AD2020Fun.arcsin(x+y), AD2020Fun.arcsin(2*x+z)])
        assert np.round(f1.value,2) == -0.5
        assert np.all(np.round(f1.derivative,2) == [1,2,1])
        assert np.all(np.round(f2.value,2) == [0,-0.52,0.52])
        assert np.all(np.round(f2.derivative,2) == [[2,0,0],[1.15,1.15,0],[2.31,0,1.15]])

        with pytest.raises(ValueError):
            x0 = AD2020(-2, [1,0,0])
            f0 = 2 * AD2020Fun.arcsin(x0) + 1

    def test_arccos():
        x = AD2020([0],[1,0,0])
        y = AD2020([-0.5],[0,1,0])
        z = AD2020([0.5],[0,0,1])
        f1 = AD2020Fun.arccos(x) + 2*y + z
        f2 = AD2020([2*AD2020Fun.arccos(x), AD2020Fun.arccos(x+y), AD2020Fun.arccos(2*x+z)])
        assert np.round(f1.value,2) == 1.07
        assert np.all(np.round(f1.derivative,2) == [-1,2,1])
        assert np.all(np.round(f2.value,2) == [3.14,2.09,1.05])
        assert np.all(np.round(f2.derivative,2) == [[-2,0,0],[-1.15,-1.15,0],[-2.31,0,-1.15]])

        with pytest.raises(ValueError):
            x0 = AD2020(-2, [1,0,0])
            f0 = 2 * AD2020Fun.arccos(x0) + 1

    def test_arctan():
        x = AD2020([1],[1,0,0])
        y = AD2020([2],[0,1,0])
        z = AD2020([3],[0,0,1])
        f1 = AD2020Fun.arctan(x) + 2*y + z
        f2 = AD2020([2*AD2020Fun.arctan(x), AD2020Fun.arctan(x+y), AD2020Fun.arctan(2*x+z)])
        assert np.round(f1.value,2) == 7.79
        assert np.all(np.round(f1.derivative,2) == [0.5,2,1])
        assert np.all(np.round(f2.value,2) == [1.57,1.25,1.37])
        assert np.all(np.round(f2.derivative,2) == [[1,0,0],[0.1,0.1,0],[0.08,0,0.04]])

    def test_sinh():
        x = AD2020([1],[1,0,0])
        y = AD2020([2],[0,1,0])
        z = AD2020([3],[0,0,1])
        f1 = AD2020Fun.sinh(x) + 2*y + z
        f2 = AD2020([2*AD2020Fun.sinh(x), AD2020Fun.sinh(x+y), AD2020Fun.sinh(2*x+z)])
        assert np.round(f1.value,2) == 8.18
        assert np.all(np.round(f1.derivative,2) == [1.54,2,1])
        assert np.all(np.round(f2.value,2) == [2.35,10.02,74.20])
        assert np.all(np.round(f2.derivative,2) == [[3.09,0,0],[10.07,10.07,0],[148.42,0,74.21]])

    def test_cosh():
        x = AD2020([1],[1,0,0])
        y = AD2020([2],[0,1,0])
        z = AD2020([3],[0,0,1])
        f1 = AD2020Fun.cosh(x) + 2*y + z
        f2 = AD2020([2*AD2020Fun.cosh(x), AD2020Fun.cosh(x+y), AD2020Fun.cosh(2*x+z)])
        assert np.round(f1.value,2) == 8.54
        assert np.all(np.round(f1.derivative,2) == [1.18,2,1])
        assert np.all(np.round(f2.value,2) == [3.09,10.07,74.21])
        assert np.all(np.round(f2.derivative,2) == [[2.35,0,0],[10.02,10.02,0],[148.41,0,74.20]])

    def test_tanh():
        x = AD2020([1],[1,0,0])
        y = AD2020([2],[0,1,0])
        z = AD2020([3],[0,0,1])
        f1 = AD2020Fun.tanh(x) + 2*y + z
        f2 = AD2020([2*AD2020Fun.tanh(x), AD2020Fun.tanh(x+y), AD2020Fun.tanh(2*x+z)])
        assert np.round(f1.value,2) == 7.76
        assert np.all(np.round(f1.derivative,2) == [0.42,2,1])
        assert np.all(np.round(f2.value,2) == [1.52,1.00,1.00])
        assert np.all(np.round(f2.derivative,5) == [[0.83995,0,0],[0.00987,0.00987,0],[0.00036,0,0.00018]])

    def test_logistic():
        x = AD2020([1],[1,0,0])
        y = AD2020([2],[0,1,0])
        z = AD2020([3],[0,0,1])
        f1 = AD2020Fun.logistic(x) + 2*y + z
        f2 = AD2020([2*AD2020Fun.logistic(x), AD2020Fun.logistic(x+y), AD2020Fun.logistic(2*x+z)])
        assert np.round(f1.value,2) == 7.73
        assert np.all(np.round(f1.derivative,2) == [0.20,2,1])
        assert np.all(np.round(f2.value,2) == [1.46,0.95,0.99])
        assert np.all(np.round(f2.derivative,3) == [[0.393,0,0],[0.045,0.045,0],[0.013,0,0.007]])

    def test_sqrt():
        x = AD2020([1],[1,0,0])
        y = AD2020([2],[0,1,0])
        z = AD2020([3],[0,0,1])
        f1 = AD2020Fun.sqrt(x) + 2*y + z
        f2 = AD2020([2*AD2020Fun.sqrt(x), AD2020Fun.sqrt(x+y), AD2020Fun.sqrt(2*x+z)])
        assert np.round(f1.value,2) == 8
        assert np.all(np.round(f1.derivative,2) == [0.5,2,1])
        assert np.all(np.round(f2.value,2) == [2,1.73,2.24])
        assert np.all(np.round(f2.derivative,2) == [[1,0,0],[0.29,0.29,0],[0.45,0,0.22]])

        with pytest.raises(ValueError):
            x0 = AD2020([-1],[1,0,0])
            f0 = AD2020Fun.sqrt(x0)

        with pytest.raises(ZeroDivisionError):
            x0 = AD2020([0],[1,0,0])
            f0 = AD2020Fun.sqrt(x0)

    test_exp()
    test_log()
    test_sin()
    test_cos()
    test_tan()
    test_arcsin()
    test_arccos()
    test_arctan()
    test_sinh()
    test_cosh()
    test_tanh()
    test_logistic()
    test_sqrt()

test_AD2020Fun_scalar()
test_AD2020Fun_vector()

print('Passed All Tests!')
