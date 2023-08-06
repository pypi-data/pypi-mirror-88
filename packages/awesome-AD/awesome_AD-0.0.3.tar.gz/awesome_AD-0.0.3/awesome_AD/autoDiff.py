# CS 107 Final Project group 8
# Forward mode

import numpy as np


# Functionality:
# 1) Calculate derivatives of a scalar function of a scalar, overloading addition,
# subtraction, multiplication, divisoin, power, negation, exponential, and trig (sin, cos, tan)

# Class that performs elementary operations on functions


class AutoDiff():

    """ Stores single variables as values and multiple variable inputs in arrays
    ATTRIBUTES
    ==========
    required:
    val: the value of the object, can be a scalar or a vector
    der: the derivative of the object, can be a scalar, a vector or an array, default=1.0
    Optional:
    var_num: number of variables used in a multivariable function, required in multiple input value with scalar function or vector fuction.
    idx : index of this variable in the function, required in multiple input value with scalar function or vector fuction.

    OUTPUTS
    =========
    self.val: the final specific value of input function
    self.der: the final specific value of derivative of input function

    EXAMPLES
    ==========
    >>> x = AutoDiff(4)
    >>> x.val[0]
    4
    >>> x.der[0][0]
    1.0

    """
    def __init__(self, val, der=1.0, var_num=1, idx=0):
        ''' initial inputs
        To use:
        >>> AutoDiff(1).val[0]
        1
        '''

        if isinstance(val, (np.ndarray, np.generic)):
            self.val = val
            self.der = der
        elif isinstance(val, (list, int, float)):
            self.val = np.array([val]).transpose()
            self.der = np.ones((len(self.val), 1)) * der

        if var_num > 1:
            self.der = np.zeros((len(self.val), var_num))
            self.der[:, idx] = der

    def __add__(self, other):
        """ Adds AutoDiff objects and returns result for function evaluated at specified number
        and result for the derivative of the function
        >>> a = AutoDiff(7)
        >>> b = AutoDiff(1)
        >>> c = a+b
        >>> c.val[0]
        8
        >>> c.der[0][0]
        2.0
        """
        try:
            return AutoDiff(self.val + other.val, self.der + other.der)
        except AttributeError:
            # Derivative of a constant is zero
            return AutoDiff(self.val + other, self.der)

    def __radd__(self, other):
        """ Makes addition commutative and returns result for function evaluated at specified number
        and result for the derivative of the function
        >>> b = AutoDiff(1)
        >>> c = 1 + b
        >>> c.val[0]
        2
        >>> c.der[0][0]
        1.0

        """
        return self.__add__(other)

    def __mul__(self, other):
        """ Multiplies AutoDiff objects and returns result for function evaluated at specified number
        and result for the derivative of the function
        >>> a = AutoDiff(1)
        >>> c = a*5
        >>> c.val[0]
        5
        >>> c.der[0][0]
        5.0
        """
        try:
            return AutoDiff(self.val * other.val, self.der * other.val + self.val * other.der)
        except AttributeError:
            return AutoDiff(self.val * other, self.der * other)

    def __rmul__(self, other):
        """ Makes multiplication commutative and returns result for function evaluated at specified number
        and result for the derivative of the function
        >>> a = AutoDiff(6)
        >>> b = 2* a
        >>> b.val[0]
        12
        >>> b.der[0][0]
        2.0
        """
        return self.__mul__(other)

    def __sub__(self, other):
        """ Makes subtraction and returns a AutoDiff object with specified value and derivative.
        >>> a = AutoDiff(1)
        >>> c = a-2
        >>> c.val[0]
        -1
        >>> c.der[0][0]
        1.0
        """
        try:
            return AutoDiff(self.val - other.val, self.der - other.der)
        except AttributeError:
            # Derivative of a constant is zero
            return AutoDiff(self.val - other, self.der)

    def __rsub__(self, other):
        """ Makes subtraction commutative and returns result for function evaluated at specified number
        and result for the derivative of the function
        >>> a = AutoDiff(1.0)
        >>> c = 2-a
        >>> c.val[0]
        1.0
        >>> c.der[0][0]
        -1.0
        """
        try:
            return AutoDiff(other.val - self.val, other.der - self.der)
        except AttributeError:
            return AutoDiff(other - self.val, - self.der)


    def __truediv__(self, other):
        """ Divides AutoDiff objects and returns  result for function evaluated at specified number
        and result for the derivative of the function
        >>> a = AutoDiff(1)
        >>> c = a/2
        >>> c.val[0]
        0.5
        >>> c.der[0][0]
        0.5
        """
        try:
            # Use chain rule for f(x)/g(x): [f'(x)*g(x) - f(x)*g'(x)]/[g(x)]^2
            return AutoDiff(self.val / other.val, (self.der * other.val - self.val * other.der) / other.val ** 2)
        except AttributeError:
            return AutoDiff(self.val/other, self.der/other)
        #     raise ZeroDivisionError("Cannot divide by zero")
        # return AutoDiff(self.val / other.val, (self.der * other.val - self.val * other.der) / other.val ** 2)

    def __rtruediv__(self, other):
        """ Other divide self and returns a AutoDiffRev object with specified value and derivative.
        >>> a = AutoDiff(1)
        >>> c = 2/a
        >>> c.val[0]
        2.0
        >>> c.der[0][0]
        -2.0
        """
        try:
            return AutoDiff(other.val / self.val, (self.val * other.der - self.der * other.val) / (self.val ** 2))
        except AttributeError:
            return AutoDiff(other / self.val, -self.der * other / (self.val ** 2))

    def __pow__(self, other):
        """ Raises an AutoDiff object to a power and returns result for function evaluated at specified number
        and result for the derivative of the function
        >>> a = AutoDiff(7)
        >>> b = 2
        >>> c = a**2
        >>> c.val[0]
        49
        >>> abs(c.der[0][0] - 14.0) < 1e-12
        True
        """
        try:
            return AutoDiff(self.val ** other.val, other.val*(self.val**(other.val-1))*self.der+(self.val**other.val)*np.log(np.abs(self.val))*other.der)
        except AttributeError:
            return AutoDiff(self.val ** other, other * (self.val ** (other - 1)) * self.der)

    def __rpow__(self, other):
        """ Raises an  object to a AutoDiff power and returns result for function evaluated at specified number
        and result for the derivative of the function
        >>> a = AutoDiff(3)
        >>> c = 2**a
        >>> c.val[0]
        8
        >>> abs(c.der[0][0]-5.545177444479562) < 1e-12
        True
        """

        try:
            return AutoDiff(other.val ** self.val,
                            self.val * (other.val ** (self.val - 1)) * other.der + np.log(np.abs(other.val)) * (
                                        other.val ** self.val) * self.der)
        except AttributeError:
            return AutoDiff(other ** self.val, np.log(np.abs(other)) * (other ** self.val) * self.der)

    def __neg__(self):
        """ Negates AutoDiff object and returns result for function evaluated at specified number
        and result for the derivative of the function
        >>> a = AutoDiff(1)
        >>> c = -a
        >>> c.val[0]
        -1
        >>> c.der[0][0]
        -1.0
        """
        return AutoDiff(- self.val, - self.der)

    def __exp__(self):
        """ Takes exponential of an AutoDiff object and returns result for function evaluated at specified number
        and result for the derivative of the function
        >>> a = AutoDiff(1)
        >>> c = exp(a)
        >>> c.val[0]
        2.718281828459045
        >>> c.der[0][0]
        2.718281828459045
        """

        return AutoDiff(np.exp(self.val), np.exp(self.val) * self.der)

    def __sin__(self):
        """ Takes sine of an AutoDiff object and returns result for function evaluated at specified number
        and result for the derivative of the function
        >>> a = AutoDiff(2)
        >>> c = sin(a ** 2)
        >>> c.val[0]
        -0.7568024953079282
        >>> c.der[0][0]
        -2.6145744834544478
        """
        # Derivative of sin(f(x)) is f'(x)*cos(f(x))
        return AutoDiff(np.sin(self.val), self.der * np.cos(self.val))

    def __cos__(self):
        """ Takes cosine of an AutoDiff object and returns result for function evaluated at specified number
        and result for the derivative of the function
        >>> x0 = AutoDiff(2)
        >>> func = cos(x0 ** 2)
        >>> abs(func.val[0] + 0.6536436208636119) < 1e-12
        True
        >>> abs(func.der[0][0] - 3.027209981231713) < 1e-12
        True
        """
        # Derivative of cos(f(x)) is -f'(x)*sin(f(x))
        return AutoDiff(np.cos(self.val), - self.der * np.sin(self.val))

    def __tan__(self):
        """ Takes tangent of an AutoDiff object and returns result for function evaluated at specified number
        and result for the derivative of the function
        >>> x0 = AutoDiff(2)
        >>> func = tan(x0 ** 2)
        >>> abs(func.val[0] - 1.1578212823495775) < 1e-12
        True
        >>> abs(func.der[0][0] - 9.36220048744648) < 1e-12
        True

        """
        return AutoDiff(np.tan(self.val), self.der / np.cos(self.val) ** 2)
    
    def __arcsin__(self):
        """ Takes inverse sine of an AutoDiff object and returns result for function evaluated at specified number
        and result for the derivative of the function
        >>> x1 = AutoDiff(0.5)
        >>> func = arcsin(x1)
        >>> abs(func.val[0] - 0.5235987755982988) < 1e-12
        True
        >>> abs(func.der[0][0] - 1.1547005383792517) < 1e-12
        True
        """
        return AutoDiff(np.arcsin(self.val), self.der / np.sqrt(1 - self.val ** 2))
    
    def __arccos__(self):
        """ Takes inverse cosine of an AutoDiff object and returns result for function evaluated at specified number
        and result for the derivative of the function
        >>> x1 = AutoDiff(0.5)
        >>> func = arccos(x1)
        >>> abs(func.val[0] - 1.0471975511965976) < 1e-12
        True
        >>> abs(func.der[0][0] - (-1.1547005383792517)) < 1e-12
        True
        """
        return AutoDiff(np.arccos(self.val), - self.der / np.sqrt(1 - self.val ** 2))

    def __arctan__(self):
        """ Takes inverse tangent of an AutoDiff object and returns result for function evaluated at specified number
        and result for the derivative of the function
        >>> x1 = AutoDiff(0.8)
        >>> func = arctan(x1 ** 2)
        >>> abs(func.val[0] - 0.5693131911006619) < 1e-12
        True
        >>> abs(func.der[0][0] - 1.1350737797956867) < 1e-12
        True
        """
        return AutoDiff(np.arctan(self.val), self.der / (1 + self.val ** 2))

    def __sqrt__(self):
        """ Takes the square root of an AutoDiff object and returns result for function evaluated at specified number
        and result for the derivative of the function
        >>> x0 = AutoDiff(4)
        >>> func = sqrt(x0)
        >>> func.val[0]
        2.0
        >>> func.der[0][0]
        0.25
        """
        if self.val < 0:
            raise ValueError
        return AutoDiff(np.sqrt(self.val), self.der * 0.5 / np.sqrt(self.val))
     
    def __lt__(self, other):
        """ Comparison between self and other: less than
        the default der is 1
        >>> x1 = AutoDiff(7)
        >>> x2 = 8
        >>> f1 = 3* x1
        >>> f2 = 3* x2
        >>> (f1 < f2)[0]
        True
        """
        try:
            return np.less(self.val, other.val) and np.less(self.der, other.der)
        except AttributeError:
            return np.less(self.val, other)

    def __gt__(self, other):
        """ Comparison between self and other: great than
        the default der is 1

        >>> (AutoDiff(2)>AutoDiff(3))[0]
        False
        """
        try:
            return np.greater(self.val, other.val) and np.greater(self.der, other.der)
        except AttributeError:
            return np.greater(self.val, other)

    def __le__(self, other):
        """ Comparison between self and other: less or equal
        the default der is 1
        >>> x1 = AutoDiff(7)
        >>> x2 = 8
        >>> f1 = 3* x1
        >>> f2 = 3* x2
        >>> (f1 <= f2)[0]
        True
        """
        try:
            return np.less_equal(self.val, other.val) and np.less_equal(self.der, other.der)
        except AttributeError:
            return np.less_equal(self.val, other)

    def __ge__(self, other):
        """ Comparison between self and other: great or equal
        the default der is 1

        >>> (AutoDiff(2)>=AutoDiff(3))[0]
        False
        """
        try:
            return np.greater_equal(self.val, other.val) and np.greater_equal(self.der, other.der)
        except AttributeError:
            return np.greater_equal(self.val, other)

    def __eq__(self, other):
        """ Comparison between self and other: equal
        the default der is 1
        >>> (AutoDiff(2)==AutoDiff(2))
        True
        """
        try:
            return np.array_equal(self.val, other.val) and np.array_equal(self.der, other.der)
        except AttributeError:
            return np.array_equal(self.val, other)

    def __ne__(self, other):
        """ Comparison between self and other: not equal
        the default der is 1
        >>> (AutoDiff(2) != AutoDiff(3))
        True
        """
        try:
            return not np.array_equal(self.val, other.val) or not np.array_equal(self.der, other.der)
        except AttributeError:
            return not np.array_equal(self.val, other)


def exp(x):
    """
    If it is AutoDiff object, then
    takes the expontenial of an AutoDiff object and returns a AutoDiff object with specified value and derivative result.
    else just use numerical methods
    >>> a = 1
    >>> c = exp(a)
    >>> c
    2.718281828459045
    >>> a = AutoDiff(1)
    >>> c = exp(a)
    >>> c.val[0]
    2.718281828459045
    >>> c.der[0][0]
    2.718281828459045
    """
    try:
        return x.__exp__()
    except AttributeError:
        return np.exp(x)


def sin(x):
    """ If it is AutoDiff object, then
    takes the sine of an AutoDiff object and returns a AutoDiff object with specified value and derivative result.
    else just use numerical methods
    >>> a = AutoDiff(2)
    >>> c = sin(a ** 2)
    >>> c.val[0]
    -0.7568024953079282
    >>> c.der[0][0]
    -2.6145744834544478
    """
    try:
        return x.__sin__()
    except AttributeError:
        return np.sin(x)


def cos(x):
    """ If it is AutoDiff object, then
    takes the cosine of an AutoDiff object and returns a AutoDiff object with specified value and derivative result.
    else just use numerical methods
    >>> x0 = AutoDiff(2)
    >>> func = cos(x0 ** 2)
    >>> abs(func.val[0] + 0.6536436208636119) < 1e-12
    True
    >>> abs(func.der[0][0] - 3.027209981231713) < 1e-12
    True
    """
    try:
        return x.__cos__()
    except AttributeError:
        return np.cos(x)


def tan(x):
    """ If it is AutoDiff object, then
    takes the tangent of an AutoDiff object and returns a AutoDiff object with specified value and derivative result.
    else just use numerical methods
    >>> x0 = AutoDiff(2)
    >>> func = tan(x0 ** 2)
    >>> abs(func.val[0] - 1.1578212823495775) < 1e-12
    True
    >>> abs(func.der[0][0] - 9.36220048744648) < 1e-12
    True

        """
    try:
        return x.__tan__()
    except AttributeError:
        return np.tan(x)


def arcsin(x):
    """ If it is AutoDiff object, then
    takes the inverse sine of an AutoDiff object and returns a AutoDiff object with specified value and derivative result.
    else just use numerical methods
    >>> x1 = AutoDiff(0.5)
    >>> func = arcsin(x1)
    >>> abs(func.val[0] - 0.5235987755982988) < 1e-12
    True
    >>> abs(func.der[0][0] - 1.1547005383792517) < 1e-12
    True
    """
    try:
        return x.__arcsin__()
    except AttributeError:
        return np.arcsin(x)


def arccos(x):
    """ If it is AutoDiff object, then
    takes the inverse cosine of an AutoDiff object and returns a AutoDiff object with specified value and derivative result.
    else just use numerical methods
    >>> x1 = AutoDiff(0.5)
    >>> func = arccos(x1)
    >>> abs(func.val[0] - 1.0471975511965976) < 1e-12
    True
    >>> abs(func.der[0][0] - (-1.1547005383792517)) < 1e-12
    True
    """
    try:
        return x.__arccos__()
    except AttributeError:
        return np.arccos(x)


def arctan(x):
    """
    If it is AutoDiff object, then
    takes the inverse tangent of an AutoDiff object and returns a AutoDiff object with specified value and derivative result.
    else just use numerical methods
    >>> x1 = AutoDiff(0.8)
    >>> func = arctan(x1 ** 2)
    >>> abs(func.val[0] - 0.5693131911006619) < 1e-12
    True
    >>> abs(func.der[0][0] - 1.1350737797956867) < 1e-12
    True
    """
    try:
        return x.__arctan__()
    except AttributeError:
        return np.arctan(x)

def sinh(x):
    """
    If it is AutoDiff object, then
    takes the sinh of an AutoDiff object and returns a AutoDiff object with specified value and derivative result.
    else just use numerical methods

    >>> func= sinh(AutoDiff(0))
    >>> abs(func.val[0] - 0) < 1e-12
    True
    """
    try:
        return (x.__exp__() - (-x).__exp__()) / 2
    except AttributeError:
        return np.sinh(x)


def cosh(x):
    """
    If it is AutoDiff object, then
    takes the cosh of an AutoDiff object and returns a AutoDiff object with specified value and derivative result.
    else just use numerical methods

    >>> func= cosh(AutoDiff(0))
    >>> abs(func.val[0] - 1) < 1e-12
    True
    """
    try:
        return (x.__exp__() + (-x).__exp__()) / 2
    except AttributeError:
        return np.cosh(x)


def tanh(x):
    """
    If it is AutoDiff object, then
    takes the tanh of an AutoDiff object and returns a AutoDiff object with specified value and derivative result.
    else just use numerical methods

    >>> func= tanh(AutoDiff(0))
    >>> abs(func.val[0] - 0) < 1e-12
    True
    """
    try:
        return (x.__exp__() - (-x).__exp__()) / (x.__exp__() + (-x).__exp__())
    except AttributeError:
        return np.tanh(x)


def logistic(x):
    """
    If it is AutoDiff object, then
    takes the logistic of an AutoDiff object and returns a AutoDiff object with specified value and derivative result.
    else just use numerical methods

    >>> func= logistic(AutoDiff(0))
    >>> abs(func.val[0] - 0.5) < 1e-6
    True
    """

    try:
        return 1 / (1 + (-x).__exp__())
    except AttributeError:
        return 1 / (1 + np.exp(-x))


def sqrt(x):
    """ If it is AutoDiff object, then
    takes the square root of an AutoDiff object and returns a AutoDiff object with specified value and derivative result.
    else just use numerical methods
    >>> x0 = AutoDiff(4)
    >>> func = sqrt(x0)
    >>> func.val[0]
    2.0
    >>> func.der[0][0]
    0.25
    """
    try:
        return x.__sqrt__()
    except AttributeError:
        if x < 0:
            raise ValueError("Square root not defined for negative values")
        return np.sqrt(x)
    except ValueError:
        raise ValueError("Square root not defined for negative values")


def log(x, base=np.exp(1)):
    """
    If it is AutoDiff object, then
    takes the log of an AutoDiff object and returns a AutoDiff object with specified value and derivative.
    else just use numerical methods
    >>> func = log(2,2)
    >>> abs(func -1) < 1e-12
    True
    """
    if base == 1 or base < 0:
        raise ValueError('log base cannot <0 or ==1')
    try:
        return AutoDiff(np.log(x.val)/np.log(base), (x.der/(x.val*np.log(base))))
    except:
        return np.log(x)/np.log(base)


# if __name__ =='__main__':
#     import doctest
#     doctest.testmod(verbose=True)


