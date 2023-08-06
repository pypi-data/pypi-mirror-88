# Module for automatic differentiation

import numpy as np

class AD2020:
    '''
    Class to create an AD2020 object, perform basic operations on the object, and perform automatic differentiation on the object.

    Attributes
    ==========
    value: numpy.array; the value of the function (AD2020 object) evaluated at the user specified values of variables.
    derivative: numpy.array; the derivative of the function (AD2020 object) with respective to variables.

    Inputs
    ======
    value: int, float, list, or np.array
    derivative: int, float, list, or np.array

    Examples
    ========
    # Scalar input
    >>> x = AD2020(value=2.0, derivative=1.0)
    >>> f = 2 * x + 1
    >>> print(f.value)
    [5.0]
    >>> print(f.derivative)
    [2.0]

    # Vector Input
    >>> x1 = AD2020(2.0, [1.0, 0])
    >>> x2 = AD2020(2.0, [0, 1.0])
    >>> f = AD2020([x1, x2])
    >>> print(f.value)
    [2.0 2.0]
    >>> print(f.derivative)
    [[1.0 0.0]
    [0.0 1.0]]
    '''
    def __init__(self, value, derivative=[1]):
        if isinstance(value, int) or isinstance(value, float):
            value = [float(value)]
        if isinstance(derivative, int) or isinstance(derivative, float):
            derivative = [float(derivative)]
        if len(value) == 1:
            self.value = np.array(value)
            self.derivative = np.array(derivative)
        else:
            self.value = np.hstack(([x.value for x in value]))
            self.derivative = np.vstack(([x.derivative for x in value]))

    def __repr__(self):
        return 'An AD2020 Object\nValues:\n{}\nJacobian:\n{}'.format(self.value, self.derivative)

    def __eq__(self, other):
        '''
        Check if an AD2020 object is equal to another AD2020 object, int, float, list, or np.array

        Inputs
        ======
        self: AD2020 object
        other: AD2020 object, int, float, list, or np.array

        Return
        =======
        True if self.value == other (or other.value) else False
        '''
        try:
            return np.array_equal(self.value, other.value) and np.array_equal(self.derivative, other.derivative)
        except:
            return self.value == other

    def __ne__(self, other):
        '''
        Check if an AD2020 object is not equal to another AD2020 object, int, float, list, or np.array

        Inputs
        ======
        self: AD2020 object
        other: AD2020 object, int, float, list, or np.array

        Return
        =======
        True if self.value != other (or other.value) else False
        '''
        return not self.__eq__(other)

    def __lt__(self, other):
        '''
        Check if the value of an AD2020 object is less than the value of another AD2020 object, int, float, list, or np.array

        Inputs
        ======
        self: AD2020 object
        other: AD2020 object, int, float, list, or np.array

        Return
        =======
        True if self.value < other (or other.value) else False
        '''
        try:
            return self.value < other.value
        except:
            return self.value < other

    def __gt__(self, other):
        '''
        Check if the value of an AD2020 object is greater than the value of another AD2020 object, int, float, list, or np.array

        Inputs
        ======
        self: AD2020 object
        other: AD2020 object, int, float, list, or np.array

        Return
        =======
        True if self.value > other (or other.value) else False
        '''
        try:
            return self.value > other.value
        except:
            return self.value > other

    def __le__(self, other):
        '''
        Check if the value of an AD2020 object is less than or equal to the value of another AD2020 object, int, float, list, or np.array

        Inputs
        ======
        self: AD2020 object
        other: AD2020 object, int, float, list, or np.array

        Return
        =======
        True if self.value <= other (or other.value) else False
        '''
        return self.__lt__(other) or self.__eq__(other)

    def __ge__(self, other):
        '''
        Check if the value of an AD2020 object is greater than or equal to the value of another AD2020 object, int, float, list, or np.array

        Inputs
        ======
        self: AD2020 object, int, float, list, or np.array
        other: AD2020 object

        Return
        =======
        True if self.value >= other (or other.value) else False
        '''
        return self.__gt__(other) or self.__eq__(other)

    def __add__(self, other):
        '''
        The addition of an AD2020 object and another AD2020 object, int, or float

        Inputs
        ======
        self: AD2020 object
        other: AD2020 object, int, or float

        Return
        =======
        An AD2020 object which is the addition of self and other
        '''
        try:
            value = self.value + other.value
            derivative = self.derivative + other.derivative
        except AttributeError:
            value = self.value + other
            derivative = self.derivative

        return AD2020(value, derivative)

    def __radd__(self, other):
        '''
        Overload the right side addition dunder method
        '''
        return self.__add__(other)

    def __sub__(self, other):
        '''
        The substraction of an AD2020 object, int, or float from another AD2020 object

        Inputs
        ======
        self: AD2020 object
        other: AD2020 object, int, or float

        Return
        =======
        An AD2020 object which is the substraction of other from self
        '''
        return self.__add__(-other)

    def __rsub__(self, other):
        '''
        Overload the right substraction dunder method
        '''
        return (-self).__add__(other)

    def __mul__(self, other):
        '''
        The multiplication of an AD2020 object and another AD2020 object, int, or float

        Inputs
        ======
        self: AD2020 object
        other: AD2020 object, int, or float

        Returns
        =======
        An AD2020 object which is the multiplication of self and other
        '''
        try:
            value = self.value * other.value
            derivative = self.derivative * other.value + self.value * other.derivative
        except AttributeError:
            value = self.value * other
            derivative = self.derivative * other

        return AD2020(value, derivative)

    def __rmul__(self, other):
        '''
        Overload the right side multiplication dunder method
        '''
        return self.__mul__(other)

    def __truediv__(self, other):
        '''
        The division of an AD2020 object by another AD2020 object, int, or float

        Inputs
        ======
        self: AD2020 object
        other: AD2020 object, int, or float

        Return
        =======
        An AD2020 object which is the division of self by other
        '''
        ndiv = other if isinstance(other, int) or isinstance(other, float) else other.value
        if ndiv == 0:
            raise ZeroDivisionError('Unable to calculate the division of x by 0')

        try:
            value = np.divide(self.value, other.value)
            der_num = np.multiply(other.value, self.derivative) - np.multiply(self.value, other.derivative)
            der_den = other.value ** 2
            derivative = np.divide(der_num, der_den)
        except AttributeError:
            value = np.divide(self.value, other)
            derivative = np.divide(self.derivative, other)

        return AD2020(value, derivative)

    def __rtruediv__(self, other):
        '''
        The division of an AD2020 object, int, or float by another AD2020 object

        Inputs
        ======
        self: AD2020 object
        other: AD2020 object, int, or float

        Return
        =======
        An AD2020 object which is the division of other by self
        '''
        if self.value == 0:
            raise ZeroDivisionError('Unable to calculate the division of a number by 0')

        try:
            value = np.divide(other.value, self.value)
            der_num = np.multiply(other.derivative, self.value) - np.multiply(self.derivative, other.value)
            der_den = self.value ** 2
            derivative = np.divide(der_num, der_den)
        except AttributeError:
            value = np.divide(other, self.value)
            derivative = (-np.multiply(other, self.derivative)) / (self.value ** 2)

        return AD2020(value, derivative)

    def __pow__(self, other):
        '''
        The power of an AD2020 object

        Inputs
        ======
        self: AD2020 object
        other: AD2020 object, int, or float

        Return
        =======
        An AD2020 object which is self raised to power other
        '''
        npow = other if isinstance(other, int) or isinstance(other, float) else other.value
        if self.value == 0 and npow < 1:
            raise ZeroDivisionError('Unable to calculate derivative of 0**x for x < 1')
        elif self.value < 0 and npow % 1 != 0:
            raise ValueError('Unable to calculate derivative of x**y for x < 0, y is a fraction')

        try:
            value = np.power(self.value, other.value)
            derivative = value * (np.multiply(np.divide(other.value, self.value), self.derivative) + np.log(self.value) * other.derivative)
        except:
            value = np.power(self.value, other)
            derivative = other * np.multiply((self.value ** (other - 1)), self.derivative)

        return AD2020(value, derivative)

    def __rpow__(self, other):
        '''
        The power of an AD2020 object

        Inputs
        ======
        self: AD2020 object
        other: AD2020 object, int, or float

        Return
        =======
        An AD2020 object which is other raised to power self
        '''
        if other == 0:
            if self.value == 0:
                value, derivative = [1, 0]
            elif self.value > 0:
                value, derivative = [0, 0]
            elif self.value < 0:
                raise ZeroDivisionError('Unable to raise 0 to a negative power')
        elif other < 0:
            raise ValueError()
        else:
            try:
                value = np.power(other.value, self.value)
                derivative = value * (np.multiply(np.divide(self.value, other.value), other.derivative) + np.log(other.value) * self.derivative)
            except AttributeError:
                value = other ** self.value
                derivative = other ** self.value * self.derivative * np.log(other)

        return AD2020(value, derivative)

    def __neg__(self):
        '''
        The negation of an AD2020 object

        Inputs
        ======
        self: AD2020 object

        Return
        =======
        An AD2020 object which is the negation of self
        '''
        value = self.value * -1
        derivative = self.derivative * -1
        return AD2020(value, derivative)
