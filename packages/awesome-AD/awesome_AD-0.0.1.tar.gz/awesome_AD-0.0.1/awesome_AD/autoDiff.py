# CS 107 Final Project
# Forward mode

import numpy as np


# Functionality:
# 1) Calculate derivatives of a scalar function of a scalar, overloading addition,
# subtraction, multiplication, divisoin, power, negation, exponential, and trig (sin, cos, tan)

# Class that performs elementary operations on functions


class AutoDiff():

    """ Stores single variables as values and multiple variable inputs in arrays"""
    def __init__(self, val, der=1.0, var_num=1, idx=0):

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
        """
        try:
            return AutoDiff(self.val + other.val, self.der + other.der)
        except AttributeError:
            # Derivative of a constant is zero
            return AutoDiff(self.val + other, self.der)

    def __radd__(self, other):
        """ Makes addition commutative and returns result for function evaluated at specified number
        and result for the derivative of the function
        """
        return self.__add__(other)

    def __mul__(self, other):
        """ Multiplies AutoDiff objects and returns result for function evaluated at specified number
        and result for the derivative of the function
        """
        try:
            return AutoDiff(self.val * other.val, self.der * other.val + self.val * other.der)
        except AttributeError:
            return AutoDiff(self.val * other, self.der * other)

    def __rmul__(self, other):
        """ Makes multiplication commutative and returns result for function evaluated at specified number
        and result for the derivative of the function
        """
        return self.__mul__(other)

    def __sub__(self, other):
        try:
            return AutoDiff(self.val - other.val, self.der - other.der)
        except AttributeError:
            # Derivative of a constant is zero
            return AutoDiff(self.val - other, self.der)

    def __rsub__(self, other):
        """ Makes subtraction commutative and returns result for function evaluated at specified number
        and result for the derivative of the function
        """
        try:
            return AutoDiff(other.val - self.val, other.der - self.der)
        except AttributeError:
            return AutoDiff(other - self.val, - self.der)
        # return self.__sub__(other)

    def __truediv__(self, other):
        """ Divides AutoDiff objects and returns  result for function evaluated at specified number
        and result for the derivative of the function
        """
        try:
            # Use chain rule for f(x)/g(x): [f'(x)*g(x) - f(x)*g'(x)]/[g(x)]^2
            return AutoDiff(self.val / other.val, (self.der * other.val - self.val * other.der) / other.val ** 2)
        except AttributeError:
            return AutoDiff(self.val/other, self.der/other)
        #     raise ZeroDivisionError("Cannot divide by zero")
        # return AutoDiff(self.val / other.val, (self.der * other.val - self.val * other.der) / other.val ** 2)

    def __rtruediv__(self, other):
        try:
            return AutoDiff(other.val / self.val, (self.val * other.der - self.der * other.val) / (self.val ** 2))
        except AttributeError:
            return AutoDiff(other / self.val, -self.der * other / (self.val ** 2))
        # try:
        #     (other.val/self.val, (self.val*other.der-other.val*self.der)/(self.val**2))
        # except:
        #     raise ZeroDivisionError("Cannot divide by zero")
        # return AutoDiff(other.val/self.val, der = (self.val*other.der-other.val*self.der)/(self.val**2))

    def __pow__(self, other):
        """ Raises an AutoDiff object to a power and returns result for function evaluated at specified number
        and result for the derivative of the function
        """
        try:
            return AutoDiff(self.val ** other.val, other.val*(self.val**(other.val-1))*self.der+(self.val**other.val)*np.log(np.abs(self.val))*other.der)
        except AttributeError:
            return AutoDiff(self.val ** other, other * (self.val ** (other - 1)) * self.der)

    def __rpow__(self, other):
        try:
            return AutoDiff(other.val ** self.val,
                            self.val * (other.val ** (self.val - 1)) * other.der + np.log(np.abs(other.val)) * (
                                        other.val ** self.val) * self.der)
        except AttributeError:
            return AutoDiff(other ** self.val, np.log(np.abs(other)) * (other ** self.val) * self.der)

    def __neg__(self):
        """ Negates AutoDiff object and returns result for function evaluated at specified number
        and result for the derivative of the function
        """
        return AutoDiff(- self.val, - self.der)

    def __exp__(self):
        """ Takes exponential of an AutoDiff object and returns result for function evaluated at specified number
        and result for the derivative of the function
        """
        return AutoDiff(np.exp(self.val), np.exp(self.val) * self.der)

    def __sin__(self):
        """ Takes sine of an AutoDiff object and returns result for function evaluated at specified number
        and result for the derivative of the function
        """
        # Derivative of sin(f(x)) is f'(x)*cos(f(x))
        return AutoDiff(np.sin(self.val), self.der * np.cos(self.val))

    def __cos__(self):
        """ Takes cosine of an AutoDiff object and returns result for function evaluated at specified number
        and result for the derivative of the function
        """
        # Derivative of cos(f(x)) is -f'(x)*sin(f(x))
        return AutoDiff(np.cos(self.val), - self.der * np.sin(self.val))

    def __tan__(self):
        """ Takes tangent of an AutoDiff object and returns result for function evaluated at specified number
        and result for the derivative of the function
        """
        #        try:
        # Derivative of tan(f(x)) is f'(x)*sec^2(f(x)), where sec(x) = 1/cos(x)
        #            (np.tan(self.val), self.der / np.cos(self.val)**2)
        #        except:
        #            raise ZeroDivisionError('cannot divide by zero')
        return AutoDiff(np.tan(self.val), self.der / np.cos(self.val) ** 2)
    
    def __arcsin__(self):
        """ Takes inverse sine of an AutoDiff object and returns result for function evaluated at specified number
        and result for the derivative of the function
        """
        return AutoDiff(np.arcsin(self.val), self.der / np.sqrt(1 - self.val ** 2))
    
    def __arccos__(self):
        """ Takes inverse cosine of an AutoDiff object and returns result for function evaluated at specified number
        and result for the derivative of the function
        """
        return AutoDiff(np.arccos(self.val), - self.der / np.sqrt(1 - self.val ** 2))

    def arctan(self):
        """ Takes inverse tangent of an AutoDiff object and returns result for function evaluated at specified number
        and result for the derivative of the function
        """
        return AutoDiff(np.arctan(self.val), self.der / (1 + self.val ** 2))

    def __sinh__(self):
        """ Takes hyperbolic sine of an AutoDiff object and returns result for function evaluated at specified number
        and result for the derivative of the function
        """
        return AutoDiff(np.sinh(self.val), self.der * np.cosh(self.val))

    def __cosh__(self):
        """ Takes hyperbolic cosh of an AutoDiff object and returns result for function evaluated at specified number
        and result for the derivative of the function
        """
        return AutoDiff(np.cosh(self.val), self.der * np.sinh(self.val))
    
    def __tanh__(self):
        """ Takes hyperbolic tangent of an AutoDiff object and returns result for function evaluated at specified number
        and result for the derivative of the function
        """
        return AutoDiff(np.tanh(self.val), self.der / np.cosh(self.val) ** 2)

    def __logistic__(self):
        """ Uses the standard logistic function with parameters k = 1, L = 1 on an AutoDiff object and returns result for function evaluated at specified number
        and result for the derivative of the function
        """
        return AutoDiff(logistic(self.val), self.der * logistic(self.val) * logistic(- self.val))

    def __sqrt__(self):
        """ Takes the square root of an AutoDiff object and returns result for function evaluated at specified number
        and result for the derivative of the function
        """
        if self.val < 0:
            raise ValueError
        return AutoDiff(np.sqrt(self.val), self.der * 0.5 / np.sqrt(self.val))
    
    # def __sqrt__(self):
    #     """ Takes the square root of an AutoDiff object and returns result for function evaluated at specified number
    #     and result for the derivative of the function
    #     """
    #     return AutoDiff(np.sqrt(self.val), self.der * 0.5 / np.sqrt(self.val))
    
    def __lt__(self, other):
        try:
            return np.less(self.val, other.val) and np.less(self.der, other.der)
        except AttributeError:
            return np.less(self.val, other)

    def __gt__(self, other):
        try:
            return np.greater(self.val, other.val) and np.greater(self.der, other.der)
        except AttributeError:
            return np.greater(self.val, other)

    def __le__(self, other):
        try:
            return np.less_equal(self.val, other.val) and np.less_equal(self.der, other.der)
        except AttributeError:
            return np.less_equal(self.val, other)

    def __ge__(self, other):
        try:
            return np.greater_equal(self.val, other.val) and np.greater_equal(self.der, other.der)
        except AttributeError:
            return np.greater_equal(self.val, other)

    def __eq__(self, other):
        try:
            return np.array_equal(self.val, other.val) and np.array_equal(self.der, other.der)
        except AttributeError:
            return np.array_equal(self.val, other)

    def __ne__(self, other):
        try:
            return not np.array_equal(self.val, other.val) or not np.array_equal(self.der, other.der)
        except AttributeError:
            return not np.array_equal(self.val, other)
        
def exp(x):
    try:
        return x.__exp__()
    except AttributeError:
        return np.exp(x)
    
def sin(x):
    try:
        return x.__sin__()
    except AttributeError:
        return np.sin(x)

def cos(x):
    try:
        return x.__cos__()
    except AttributeError:
        return np.cos(x)


def tan(x):
    try:
        return x.__tan__()
    except AttributeError:
        return np.tan(x)

def arcsin(x):
    try:
        return x.__arcsin__()
    except AttributeError:
        return np.arcsin(x)

def arccos(x):
    try:
        return x.__arccos__()
    except AttributeError:
        return np.arccos(x)

def arctan(x):
    try:
        return x.__arctan__()
    except AttributeError:
        return np.arctan(x)

def sinh(x):
    try:
        return (x.__exp__() - (-x).__exp__()) / 2
    except AttributeError:
        return np.sinh(x)

def cosh(x):
    try:
        return (x.__exp__() + (-x).__exp__()) / 2
    except AttributeError:
        return np.cosh(x)

def tanh(x):
    try:
        return (x.__exp__() - (-x).__exp__()) / (x.__exp__() + (-x).__exp__())
    except AttributeError:
        return np.tanh(x)

def logistic(x):
    try:
        return 1 / (1 + (-x).__exp__())
    except AttributeError:
        return 1 / (1 + np.exp(-x))


def sqrt(x):
    try:
        return x.__sqrt__()
    except AttributeError:
        if x < 0:
            raise ValueError("Square root not defined for negative values")
        return np.sqrt(x)
    except ValueError:
        raise ValueError("Square root not defined for negative values")

# def sqrt(x):
#     try:
#         return x.__sqrt__()
#     except AttributeError:
#         return np.sqrt(x)
#     except ValueError:
#         raise ValueError("Square root not defined for negative values")
        
# def sqrt(x):
#     try:
#         if x.val < 0:
#             raise ValueError('Sqrt is not defined for negative values')
#         else:
#             return AutoDiff(np.sqrt(x.val), (1/2)*x.der/(np.sqrt(x.val)))
#     except AttributeError:
#         if x < 0:
#             raise ValueError('Sqrt is not defined for negative values')
#         else:
#             return np.sqrt(x)


class log(AutoDiff):
    def __init__(self, inputs, base=np.exp(1)):

        try:
            self.val = np.log(inputs.val)/np.log(base)
            self.der = inputs.der / inputs.val

        except AttributeError:
            self.val = np.log(inputs) / np.log(base)
            self.der = 0.0




# ## Inverse Trignometric Function
# class arcsin(AutoDiff):
#     def __init__(self, inputs):

#         try:
#             self.val = np.arcsin(inputs.val)
#             self.der = inputs.der * (1/np.sqrt(1-inputs.val**2))

#         except AttributeError:
#             self.val = np.arcsin(inputs)
#             self.der = 0.0


# class arccos(AutoDiff):
#     def __init__(self, inputs):

#         try:
#             self.val = np.arccos(inputs.val)
#             self.der = -inputs.der * (1/np.sqrt(1-inputs.val**2))

#         except AttributeError:
#             self.val = np.arccos(inputs)
#             self.der = 0.0


# class arctan(AutoDiff):
#     def __init__(self, inputs):

#         try:
#             self.val = np.arctan(inputs.val)
#             self.der = inputs.der * (1/(1+inputs.val**2))

#         except AttributeError:
#             self.val = np.arctan(inputs)
#             self.der = 0.0


## Hyperbolic Trigometric Funtion


# class sinh(AutoDiff):
#     def __init__(self, inputs):

#         try:
#             self.val = np.sinh(inputs.val)
#             self.der = np.cosh(inputs.val)

#         except AttributeError:
#             self.val = np.sinh(inputs)
#             self.der = 0.0


# class cosh(AutoDiff):
#     def __init__(self, inputs):

#         try:
#             self.val = np.cosh(inputs.val)
#             self.der = np.sinh(inputs.val)

#         except AttributeError:
#             self.val = np.cosh(inputs)
#             self.der = 0.0


# class tanh(AutoDiff):
#     def __init__(self, inputs):
#
#         try:
#             self.val = np.tanh(inputs.val)
#             self.der = inputs.der * (1 - np.tanh(inputs.val)**2)
#
#         except AttributeError:
#             self.val = np.tanh(inputs)
#             self.der = 0.0


# class logistic(AutoDiff):
#     def __init__(self, inputs):

#         try:
#             self.val = 1/(1 + exp(- inputs.val))
#             self.der = exp(- inputs.val)/((1 + exp(- inputs.val))**2)

#         except AttributeError:
#             self.val = 1/(1 + exp(- inputs))
#             self.der = 0.0        
#



