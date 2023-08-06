# Module for applying the AD2020 library to find roots of functions using Newton's algorithm

import numpy as np
from AD2020Fun import AD2020Fun
from AD2020 import AD2020

def Find(f, x, max_iter=1000, tol=1e-7):
    '''
    Find the root of a (multivariate) function using Newton's algorithm

    Inputs
    ======
    f: a function
       The function to find the root for using Newton's algorithm.

    x0: an AD2020 object or a list of AD2020 objects
        The initial guess of the root for function f

    max_iter: int (default=1000)
              The maximum iterations for the root-finding algorithm.

    tol: float (default=1e-7)
         The tolerance for the root-finding algorithm.

    Returns
    ========
    The root value(s): an numpy array
    '''
    if isinstance(x, AD2020):

        fx = f(x)

        for k in range(max_iter):

            if fx.value == 0:
                root = x.value
                print('Root = {}'.format(root))
                break

            delta = - fx.value / fx.derivative

            if abs(delta) < tol:
                root = (x + delta).value
                print('Root = {}'.format(root))
                break

            print('Iteration {}, Delta x = {}'.format(k+1, delta))
            x = x + delta
            fx = f(x)

        return np.array(root)

    elif isinstance(x, list):

        fx = f(x)

        for k in range(max_iter):

            if fx.value == 0:
                root = np.array([v.value for v in x])
                print('Root = {}'.format(root))
                break

            delta = - np.linalg.pinv(np.expand_dims(fx.derivative, 0)) * fx.value

            if abs(np.linalg.norm(delta)) < tol:
                root = np.array([v.value for v in x]) + delta
                print('Root = {}'.format(root))
                break

            print('Iteration {}, Delta x = {}'.format(k+1, delta))
            x = [x[i] + delta[i] for i in range(len(x))]
            fx = f(x)

        return root

    else:

        raise Exception('Please provide the initial guess as an AD2020 object or a list of AD2020 objects')
