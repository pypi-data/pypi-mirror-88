# Test suite for AD2020 module

import sys
sys.path.append('./AD2020')

import pytest
import numpy as np

from AD2020 import AD2020

def test_AD2020_init():
    '''Test initiation'''

    def test_scalar_input():
        x = AD2020(2, 1)
        assert x.value == [2]
        assert x.derivative == [1]

        x = AD2020([2])
        assert x.value == [2]
        assert x.derivative == [1]

        x = AD2020([2], [3])
        assert x.value == [2]
        assert x.derivative == [3]

    def test_vector_input():
        x = AD2020([1],[1,0])
        y = AD2020([2],[0,1])
        f = AD2020([x, y])
        assert np.all(f.value == [1,2])
        assert np.all(f.derivative == [[1,0],[0,1]])

        x = AD2020([1],[1,0,0])
        y = AD2020([2],[0,1,0])
        z = AD2020([3],[0,0,1])
        f = AD2020([x, y, z])
        assert np.all(f.value == [1,2,3])
        assert np.all(f.derivative == [[1,0,0],[0,1,0],[0,0,1]])

    def test_repr():
        x = AD2020([2],[1])
        f = 2 * x + 1
        assert f.value == [5]
        assert f.derivative == [2]
        assert repr(f) == 'An AD2020 Object\nValues:\n{}\nJacobian:\n{}'.format(f.value, f.derivative)

    test_scalar_input()
    test_vector_input()
    test_repr()

def test_AD2020_comparisons():
    '''Test comparison methods'''

    def test_eq():
        x = AD2020([1])
        y = AD2020([2])
        z = AD2020([1])
        assert x == z
        assert not x == y

    def test_nq():
        x = AD2020([1])
        y = AD2020([2])
        z = AD2020([1])
        assert not x != z
        assert x != y

    def test_lt():
        x = AD2020([1])
        y = AD2020([2])
        assert x < 2
        assert 0 < x
        assert not x < 1
        assert not y < 2
        assert x < y

    def test_gt():
        x = AD2020([1])
        y = AD2020([2])
        assert x > 0
        assert 2 > x
        assert not x > 1
        assert not y > 2
        assert y > x

    def test_ge():
        x = AD2020([1])
        y = AD2020([2])
        assert x >= 0
        assert 1 >= x
        assert 2 >= x
        assert not x >= 2
        assert y >= x

    def test_le():
        x = AD2020([1])
        y = AD2020([2])
        assert x <= 1
        assert 0 <= x
        assert 1 <= x
        assert not x <= 0
        assert x <= y

    test_eq()
    test_nq()
    test_lt()
    test_gt()
    test_ge()
    test_le()

def test_AD2020_scalar():
    '''Test scalar functions'''

    def test_add():
        x = AD2020(2, 1)
        f1 = x + x
        f2 = x + 2
        f3 = x + 3.0 + x
        assert f1 == AD2020(4, 2)
        assert f2 == AD2020(4, 1)
        assert f3 == AD2020(7.0, 2)

    def test_radd():
        x = AD2020(5, 1)
        f1 = x + x
        f2 = 2 + x
        f3 = 2.0 + x + 1.0 + x
        assert f1 == AD2020(10, 2)
        assert f2 == AD2020(7, 1)
        assert f3 == AD2020(13.0, 2)

    def test_sub():
        x = AD2020(4, 1)
        f1 = x - x
        f2 = x - 4
        f3 = x - 2.0 - 1.0 - x + x
        assert f1 == AD2020(0, 0)
        assert f2 == AD2020(0, 1)
        assert f3 == AD2020(1.0, 1)

    def test_rsub():
        x = AD2020(4, 1)
        f1 = x - x - x
        f2 = 4 - x
        f3 = 4.0 - x + 1.0 - x + x
        assert f1 == AD2020(-4, -1)
        assert f2 == AD2020(0, -1)
        assert f3 == AD2020(1.0, -1)

    def test_mul():
        x = AD2020(3, 1)
        f1 = x * x
        f2 = x * 2
        f3 = x * x * 2.0
        assert f1 == AD2020(9, 6)
        assert f2 == AD2020(6, 2)
        assert f3 == AD2020(18.0, 12.0)

    def test_rmul():
        x = AD2020(6, 1)
        f1 = x * x * x
        f2 = 2 * x
        f3 = 2.0 * x
        assert f1 == AD2020(216, 108)
        assert f2 == AD2020(12, 2)
        assert f3 == AD2020(12.0, 2.0)

    def test_truediv():
        x = AD2020(2, 1)
        f1 = x / x
        f2 = x / 2
        f3 = x / 2.0 / 2.0 / x * x
        assert f1 == AD2020(1.0, 0.0)
        assert f2 == AD2020(1, 0.5)
        assert f3 == AD2020(0.5, 0.25)

        with pytest.raises(ZeroDivisionError):
            x0 = AD2020(2, 1)
            f0 = x0 / 0

    def test_rtruediv():
        x = AD2020(2, 1)
        f1 = x / x / x
        f2 = 1 / x
        f3 = 1.0 / x / 2.0 / x * x
        assert f1 == AD2020(0.5, -0.25)
        assert f2 == AD2020(0.5, -0.25)
        assert f3 == AD2020(0.25, -0.125)

        with pytest.raises(ZeroDivisionError):
            x0 = AD2020(0, 1)
            f0 = 2 / x0

    def test_pow():
        x = AD2020(2, 1)
        f1 = x ** (2 * x)
        f2 = x ** 3
        f3 = x ** (1/2)
        assert f1.value == 16
        assert np.round(f1.derivative, 2) == 54.18
        assert f2 == AD2020(8, 12)
        assert np.round(f3.value, 2) == 1.41
        assert np.round(f3.derivative, 2) == 0.35

        with pytest.raises(ValueError):
            x0 = AD2020(-2, 1)
            f0 = x0 ** (1/2)
        with pytest.raises(ZeroDivisionError):
            x0 = AD2020(0, 1)
            f0 = x0 ** (1/2)

    def test_rpow():
        x = AD2020(4, 1)
        f1 = 2 ** x
        f2 = 0 ** x
        assert f1.value == 16
        assert np.round(f1.derivative, 2) == 11.09
        assert f2 == AD2020(0, 0)

        with pytest.raises(ValueError):
            x0 = AD2020(2, 1)
            f0 = (-4) ** x
        with pytest.raises(ZeroDivisionError):
            x0 = AD2020(-2, 1)
            f0 = 0 ** x0

    def test_neg():
        x = AD2020(3, 1)
        f1 = x * x
        f2 = -f1
        assert f1 == AD2020(9, 6)
        assert f2 == AD2020(-9, -6)

    test_add()
    test_radd()
    test_sub()
    test_rsub()
    test_mul()
    test_rmul()
    test_truediv()
    test_rtruediv()
    test_pow()
    test_rpow()
    test_neg()

def test_AD2020_vector():
    '''Test vector functions'''

    def test_add():
        x = AD2020([1],[1,0,0])
        y = AD2020([2],[0,1,0])
        z = AD2020([3],[0,0,1])
        f1 = x + y + z
        f2 = AD2020([x+y, y+3, z])
        f3 = AD2020([x+1, y, y+z])
        assert f1 == AD2020(6, [1,1,1])
        assert np.all(f2.value == [3,5,3])
        assert np.all(f2.derivative == [[1,1,0],[0,1,0],[0,0,1]])
        assert np.all(f3.value == [2,2,5])
        assert np.all(f3.derivative == [[1,0,0],[0,1,0],[0,1,1]])

    def test_radd():
        x = AD2020([1],[1,0,0])
        y = AD2020([2],[0,1,0])
        z = AD2020([3],[0,0,1])
        f1 = x + y + z
        f2 = AD2020([x+y, 1+y, z])
        f3 = AD2020([5+x, y, y+z])
        assert f1 == AD2020(6, [1,1,1])
        assert np.all(f2.value == [3,3,3])
        assert np.all(f2.derivative == [[1,1,0],[0,1,0],[0,0,1]])
        assert np.all(f3.value == [6,2,5])
        assert np.all(f3.derivative == [[1,0,0],[0,1,0],[0,1,1]])

    def test_sub():
        x = AD2020([1],[1,0,0])
        y = AD2020([2],[0,1,0])
        z = AD2020([3],[0,0,1])
        f1 = x - y + z
        f2 = AD2020([x-y, y-2, z])
        f3 = AD2020([x-1, y, y-z])
        assert f1 == AD2020(2, [1,-1,1])
        assert np.all(f2.value == [-1,0,3])
        assert np.all(f2.derivative == [[1,-1,0],[0,1,0],[0,0,1]])
        assert np.all(f3.value == [0,2,-1])
        assert np.all(f3.derivative == [[1,0,0],[0,1,0],[0,1,-1]])

    def test_rsub():
        x = AD2020([1],[1,0,0])
        y = AD2020([2],[0,1,0])
        z = AD2020([3],[0,0,1])
        f1 = y - x + z
        f2 = AD2020([y-x, 2-y, z])
        f3 = AD2020([1-x, y, z-y])
        assert f1 == AD2020(4, [-1,1,1])
        assert np.all(f2.value == [1,0,3])
        assert np.all(f2.derivative == [[-1,1,0],[0,-1,0],[0,0,1]])
        assert np.all(f3.value == [0,2,1])
        assert np.all(f3.derivative == [[-1,0,0],[0,1,0],[0,-1,1]])

    def test_mul():
        x = AD2020([1],[1,0,0])
        y = AD2020([2],[0,1,0])
        z = AD2020([3],[0,0,1])
        f1 = x * y + z
        f2 = AD2020([x*y, y*2, z])
        f3 = AD2020([x, y, y*z])
        assert f1 == AD2020(5, [2,1,1])
        assert np.all(f2.value == [2,4,3])
        assert np.all(f2.derivative == [[2,1,0],[0,2,0],[0,0,1]])
        assert np.all(f3.value == [1,2,6])
        assert np.all(f3.derivative == [[1,0,0],[0,1,0],[0,3,2]])

    def test_rmul():
        x = AD2020([1],[1,0,0])
        y = AD2020([2],[0,1,0])
        z = AD2020([3],[0,0,1])
        f1 = 2 * x * y * z
        f2 = AD2020([y*x, 3*y, z])
        f3 = AD2020([z*x, y, z*y])
        assert f1 == AD2020(12, [12,6,4])
        assert np.all(f2.value == [2,6,3])
        assert np.all(f2.derivative == [[2,1,0],[0,3,0],[0,0,1]])
        assert np.all(f3.value == [3,2,6])
        assert np.all(f3.derivative == [[3,0,1],[0,1,0],[0,3,2]])

    def test_truediv():
        x = AD2020([1],[1,0,0])
        y = AD2020([2],[0,1,0])
        z = AD2020([3],[0,0,1])
        f1 = x * z / y
        f2 = AD2020([x/y, y*z, z/y])
        f3 = AD2020([x/2, y/x, z/3])
        assert f1 == AD2020(1.5, [1.5,-0.75,0.5])
        assert np.all(f2.value == [0.5,6,1.5])
        assert np.all(f2.derivative == [[0.5,-0.25,0],[0,3,2],[0,-0.75,0.5]])
        assert np.all(f3.value == [0.5,2,1])
        assert np.all(f3.derivative == [[0.5,0,0],[-2,1,0],[0,0,1/3]])

        with pytest.raises(ZeroDivisionError):
            f0 = x / 0

    def test_rtruediv():
        x = AD2020([1],[1,0,0])
        y = AD2020([2],[0,1,0])
        z = AD2020([3],[0,0,1])
        f1 = y / x * z
        f2 = AD2020([x/y, y*z/x, z/y])
        f3 = AD2020([2/x, x/y, 3/z])
        assert f1 == AD2020(6, [-6,3,2])
        assert np.all(f2.value == [0.5,6,1.5])
        assert np.all(f2.derivative == [[0.5,-0.25,0],[-6,3,2],[0,-0.75,0.5]])
        assert np.all(f3.value == [2,0.5,1])
        assert np.all(f3.derivative == [[-2,0,0],[0.5,-0.25,0],[0,0,-1/3]])

        with pytest.raises(ZeroDivisionError):
            x0 = AD2020([0],[1,0,0])
            f0 = 2 / x0

    def test_pow():
        x = AD2020([1],[1,0,0])
        y = AD2020([2],[0,1,0])
        z = AD2020([3],[0,0,1])
        f1 = x**3 + y + z
        f2 = AD2020([x**2, y*z/x, z/y])
        f3 = AD2020([x, x/y, z**2])
        assert f1 == AD2020(6, [3,1,1])
        assert np.all(f2.value == [1,6,1.5])
        assert np.all(f2.derivative == [[2,0,0],[-6,3,2],[0,-0.75,0.5]])
        assert np.all(f3.value == [1,0.5,9])
        assert np.all(f3.derivative == [[1,0,0],[0.5,-0.25,0],[0,0,6]])

        with pytest.raises(ValueError):
            x0 = AD2020([-2],[1,0,0])
            f0 = x0 ** (1/2)
        with pytest.raises(ZeroDivisionError):
            x0 = AD2020([0],[1,0,0])
            f0 = x0 ** (1/2)

    def test_rpow():
        x = AD2020([1],[1,0,0])
        y = AD2020([2],[0,1,0])
        z = AD2020([3],[0,0,1])
        f1 = 2**x + y + z
        f2 = AD2020([2**(2*x), 2**(y-1), 2**(z**2)])
        assert f1.value == [7]
        assert np.all(np.round(f1.derivative, 2) == [1.39,1,1])
        assert np.all(f2.value == [4,2,512])
        assert np.all(np.round(f2.derivative, 2) == [[5.55,0,0],[0,1.39,0],[0,0,2129.35]])

        with pytest.raises(ValueError):
            f0 = (-4) ** x
        with pytest.raises(ZeroDivisionError):
            x0 = AD2020([-2],[1,0,0])
            f0 = 0 ** x0

    def test_neg():
        x = AD2020([1],[1,0,0])
        y = AD2020([2],[0,1,0])
        z = AD2020([3],[0,0,1])
        f1 = 2**x + y + z
        f2 = -f1
        assert f1.value == [7]
        assert np.all(np.round(f1.derivative, 2) == [1.39,1,1])
        assert f2.value == [-7]
        assert np.all(np.round(f2.derivative, 2) == [-1.39,-1,-1])

    test_add()
    test_radd()
    test_sub()
    test_rsub()
    test_mul()
    test_rmul()
    test_truediv()
    test_rtruediv()
    test_pow()
    test_rpow()
    test_neg()

test_AD2020_init()
test_AD2020_comparisons()
test_AD2020_scalar()
test_AD2020_vector()

print('Passed All Tests!')
