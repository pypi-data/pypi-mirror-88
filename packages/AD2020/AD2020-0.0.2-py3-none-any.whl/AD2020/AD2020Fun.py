# Module for performing special elementary functions on AD2020 objects

import numpy as np
#from AD2020 import AD2020
from AD2020.AD2020 import AD2020

class AD2020Fun:
    '''
    Class to perform special elementary functions on an AD2020 object.
    '''
    def exp(x, base=np.e):
        '''
        Exponential of an AD2020 object (any base)

        Input
        ======
        x: An AD2020 object

        Returns
        =======
        Exponential of x (An AD2020 object)
        '''
        if base == np.e:
            return AD2020(np.exp(x.value), x.derivative*np.exp(x.value))
        else:
            new_x = AD2020(x.value, x.derivative)
            return new_x.__rpow__(base)

    def log(x, base=np.e):
        '''
        Logarithm of an AD2020 object (any base)

        Input
        ======
        x: An AD2020 object

        Returns
        =======
        Logarithm of x (An AD2020 object)
        '''
        if base == 0 or not (isinstance(base, int) or isinstance(base,float)):
            raise ZeroDivisionError("The base must be a constant integer or a float not equal to 0")

        if not np.all(x.value > 0):
            raise ValueError('Unable to caluclate the logarithm of a non-positive number')

        value = np.array([np.math.log(v, base) for v in x.value])
        derivative = np.multiply(1 / np.multiply(np.log(base), x.value), x.derivative)
        return AD2020(value, derivative)

    def sin(x):
        '''
        Sine of an AD2020 object

        Input
        ======
        x: An AD2020 object

        Returns
        =======
        Sine of x (An AD2020 object)
        '''
        return AD2020(np.sin(x.value), np.cos(x.value)*x.derivative)

    def cos(x):
        '''
        Cosine of an AD2020 object

        Input
        ======
        x: An AD2020 object

        Returns
        =======
        Cosine of x (An AD2020 object)
        '''
        return AD2020(np.cos(x.value), -np.sin(x.value)*x.derivative)

    def tan(x):
        '''
        Tangent of an AD2020 object

        Input
        ======
        x: An AD2020 object

        Returns
        =======
        Tangent of x (An AD2020 object)
        '''
        if np.any((x.value/np.pi - 0.5) % 1 == 0.0):
            raise ValueError('Unable to calculate tan(x) for x = pi/2 or -pi/2')
        return AD2020(np.tan(x.value), ((1/np.cos(x.value))**2)*x.derivative)

    def arcsin(x):
        '''
        Arcsine of an AD2020 object

        Input
        ======
        x: An AD2020 object

        Returns
        =======
        Arcsine of x (An AD2020 object)
        '''
        if not np.all(x.value < 1 and x.value > -1):
            raise ValueError('Unable to caluclate the arcsine of a number outside (-1, 1)]')

        return AD2020(np.arcsin(x.value), (1/np.sqrt(1-x.value**2))*x.derivative)

    def arccos(x):
        '''
        Arccosine of an AD2020 object

        Input
        ======
        x: An AD2020 object

        Returns
        =======
        Arccosine of x (An AD2020 object)
        '''
        values = map(lambda i: -1 < i < 1, x.value)
        if not np.all(x.value < 1 and x.value > -1):
            raise ValueError('Unable to caluclate the arcsine of a number outside (-1, 1)')
        return AD2020(np.arccos(x.value), (-1/np.sqrt(1 - x.value**2))*x.derivative)

    def arctan(x):
        '''
        Arctangent of an AD2020 object

        Input
        ======
        x: An AD2020 object

        Returns
        =======
        Arctangent of x (An AD2020 object)
        '''
        return AD2020(np.arctan(x.value), (1 / (1 + x.value**2))*x.derivative)

    def sinh(x):
        '''
        Sinh of an AD2020 object

        Input
        ======
        x: An AD2020 object

        Returns
        =======
        Sinh of x (An AD2020 object)
        '''
        return AD2020(np.sinh(x.value), np.cosh(x.value)*x.derivative)

    def cosh(x):
        '''
        Cosh of an AD2020 object

        Input
        ======
        x: An AD2020 object

        Returns
        =======
        Cosh of x (An AD2020 object)
        '''
        return AD2020(np.cosh(x.value), np.sinh(x.value)*x.derivative)

    def tanh(x):
        '''
        Tanh of an AD2020 object

        Input
        ======
        x: An AD2020 object

        Returns
        =======
        Tanh of x (An AD2020 object)
        '''
        return AD2020(np.tanh(x.value), (1/(np.cosh(x.value)**2))*x.derivative)

    def logistic(x):
        '''
        Logistic of an AD2020 object

        Input
        ======
        x: An AD2020 object

        Returns
        =======
        Logistic of x (An AD2020 object)
        '''
        return AD2020(1 / (1 + np.exp(-x.value)), (np.exp(x.value) / ((1 + np.exp(x.value)) ** 2))*x.derivative)

    def sqrt(x):
        '''
        Square root of an AD2020 object

        Input
        ======
        x: An AD2020 object

        Returns
        =======
        Square root of x (An AD2020 object)
        '''
        new_x = AD2020(x.value, x.derivative)
        return new_x.__pow__(0.5)
