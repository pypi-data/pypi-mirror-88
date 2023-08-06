# CS 107 Final Project
# Reverse mode
import numpy as np


# Functionality:
# 1) Calculate derivatives of a scalar function of a scalar, overloading addition,
# subtraction, multiplication, divisoin, power, negation, exponential, and trig (sin, cos, tan)



class AutoDiffRev():

    """ Stores single variables as values and multiple variable inputs in arrays"""
    def __init__(self, val,parents=None):
        if isinstance(val, (np.ndarray, np.generic)):
            self.val = val
        elif isinstance(val, (list)):
            self.val = np.array(val)
        elif isinstance(val,(int, float)):
            self.val = np.array([val])
        self.grad = np.zeros((len(self.val)))
        self.parents = parents

    def __str__(self):   # for printing
        return 'AutoDiff with val:'+str(self.val)+'der:'+str(self.grad)
    
    def __len__(self):   # for use in printing 
        return len(self.val)

    def __add__(self, other):
        """ Adds AutoDiff objects and returns result for function evaluated at specified number
        and result for the derivative of the function
        >>> a = AutoDiffRev(1) 
        >>> b = AutoDiffRev(2)
        >>> c = a+b
        >>> c.val[0]
        3
        >>> c.parents
        [(a,1.0),(b,1.0)]
        """
        try:
            z = AutoDiffRev(self.val + other.val)
            z.parents = [(self, 1.0), (other, 1.0)]
            return z
        except AttributeError:
            # Derivative of a constant is zero
            other = AutoDiffRev(other*np.ones(np.shape(self.val)))
            return self+other

    def __radd__(self, other):
        """ Makes addition commutative and returns result for function evaluated at specified number
        and result for the derivative of the function
        """
        return self.__add__(other)

    def __mul__(self, other):
        try:
            z = AutoDiffRev(self.val*other.val)
            z.parents = [(self, other.val), (other, self.val)]
            return z
        except AttributeError:
            other = AutoDiffRev(other*np.ones(np.shape(self.val)))
            return self*other

    def __rmul__(self, other):
        """ Makes multiplication commutative and returns result for function evaluated at specified number
        and result for the derivative of the function
        """
        return self.__mul__(other)
    
    def __sub__(self, other):
        try:
            z = AutoDiffRev(self.val - other.val)
            z.parents = [(self, 1.0), (other, -1.0)]
            return z
        except AttributeError:
            other = AutoDiffRev(other*np.ones(np.shape(self.val)))
            return self-other

    def __rsub__(self, other):
        """ Makes subtraction commutative and returns result for function evaluated at specified number
        and result for the derivative of the function
        """
        try:
            return AutoDiffRev(other.val - self.val,parents=[(self, -1.0), (other, 1.0)])
            # print('warning!')
            # z.parents = [(self, -1.0), (other, 1.0)]
            # return z
        except AttributeError:
            other = AutoDiffRev(other*np.ones(np.shape(self.val)))
            return other-self

    def __truediv__(self, other):
        try:
            z = AutoDiffRev(self.val/other.val)
            z.parents = [(self, 1/other.val), (other, -self.val/(other.val)**2)]
            return z
        except AttributeError:
            other = AutoDiffRev(other*np.ones(np.shape(self.val)))
            return self/other
    
    def __rtruediv__(self, other):
        try:
            return  AutoDiffRev(other.val / self.val,parents=[(self,-1*other.val/(self.val**2)),(other,1/self.val)])
            # z = AutoDiffRev(other.val / self.val)
            # # z.parents = [(self,-1*other.val/(self.val**2)),(other,1/self.val)]
            # return z
        except AttributeError:
            other = AutoDiffRev(other*np.ones(np.shape(self.val)))
            return other/self
    
    def __pow__(self, other):
        """ Raises an AutoDiff object to a power and returns result for function evaluated at specified number
        and result for the derivative of the function
        """
        try:
            z = AutoDiffRev(self.val ** other.val)
            z.parents = [(self,other.val*self.val**(other.val-1)),(other,self.val**other.val*np.log(np.abs(self.val)))]
            return z
        except AttributeError:
            other = AutoDiffRev(other*np.ones(np.shape(self.val)))
            return self**other
    
    def __rpow__(self, other):
        try:
            return AutoDiffRev(other.val ** self.val,parents=[(other,self.val*other.val**(self.val-1)),(self,other.val**self.val*np.log(np.abs(other.val)))])
            # z = AutoDiffRev(other.val ** self.val)
            # z.parents = [(other,self.val*other.val**(self.val-1)),(self,other.val**self.val*np.log(np.abs(other.val)))]
            # return z
        except AttributeError:
            other = AutoDiffRev(other*np.ones(np.shape(self.val)))
            return other**self

    def __neg__(self):
        """ Negates AutoDiff object and returns result for function evaluated at specified number
        and result for the derivative of the function
        """
        return AutoDiffRev(- self.val,parents=[(self,-1)])

    def __exp__(self):
        """ Takes exponential of an AutoDiff object and returns result for function evaluated at specified number
        and result for the derivative of the function
        """
        return AutoDiffRev(np.exp(self.val),parents=[(self,np.exp(self.val))])

    def __sin__(self):
        """ Takes sine of an AutoDiff object and returns result for function evaluated at specified number
        and result for the derivative of the function
        """
        # Derivative of sin(f(x)) is f'(x)*cos(f(x))
        z = AutoDiffRev(np.sin(self.val))
        z.parents = [(self,np.cos(self.val))]
        return z

    def __cos__(self):
        """ Takes cosine of an AutoDiff object and returns result for function evaluated at specified number
        and result for the derivative of the function
        """
        # Derivative of cos(f(x)) is -f'(x)*sin(f(x))
        return AutoDiffRev(np.cos(self.val), parents=[(self,-np.sin(self.val))])

    def __tan__(self):
        """ Takes tangent of an AutoDiff object and returns result for function evaluated at specified number
        and result for the derivative of the function
        """
        return AutoDiffRev(np.tan(self.val), parents=[(self,(1/np.cos(self.val))**2)])

    def __lt__(self, other):
        try:
            return np.less(self.val, other.val) and np.less(self.grad, other.grad)
        except AttributeError:
            return np.less(self.val, other)

    def __gt__(self, other):
        try:
            return np.greater(self.val, other.val) and np.greater(self.grad, other.grad)
        except AttributeError:
            return np.greater(self.val, other)

    def __le__(self, other):
        try:
            return np.less_equal(self.val, other.val) and np.less_equal(self.grad, other.grad)
        except AttributeError:
            return np.less_equal(self.val, other)

    def __ge__(self, other):
        try:
            return np.greater_equal(self.val, other.val) and np.greater_equal(self.grad, other.grad)
        except AttributeError:
            return np.greater_equal(self.val, other)

    def __eq__(self, other):
        try:
            return np.array_equal(self.val, other.val) and np.array_equal(self.grad, other.grad)
        except AttributeError:
            return np.array_equal(self.val, other)
    
    def __hash__(self):
        return id(self)

    def __ne__(self, other):
        try:
            return not np.array_equal(self.val, other.val) or not np.array_equal(self.grad, other.grad)
        except AttributeError:
            return not np.array_equal(self.val, other)

    def __arcsin__(self):
        """ Takes inverse sine of an AutoDiff object and returns result for function evaluated at specified number
        and result for the derivative of the function
        """
        return AutoDiffRev(np.arcsin(self.val), parents=[(self,1/ np.sqrt(1 - self.val ** 2))])

    def __arccos__(self):
        """ Takes inverse cosine of an AutoDiff object and returns result for function evaluated at specified number
        and result for the derivative of the function
        """
        return AutoDiffRev(np.cossin(self.val), parents=[(self,1/ np.sqrt(1 - self.val ** 2))])    

    def arctan(self):
        """ Takes inverse tangent of an AutoDiff object and returns result for function evaluated at specified number
        and result for the derivative of the function
        """
        return AutoDiffRev(np.arctan(self.val), parents=[(self,1 / (1 + self.val ** 2))])

    def __sinh__(self):
        """ Takes hyperbolic sine of an AutoDiff object and returns result for function evaluated at specified number
        and result for the derivative of the function
        """
        return AutoDiffRev(np.sinh(self.val), parents=[(self,np.cosh(self.val))])

    def __cosh__(self):
        """ Takes hyperbolic cosh of an AutoDiff object and returns result for function evaluated at specified number
        and result for the derivative of the function
        """
        return AutoDiffRev(np.cosh(self.val), parents=[(self,np.sinh(self.val))])

    def __tanh__(self):
        """ Takes hyperbolic tangent of an AutoDiff object and returns result for function evaluated at specified number
        and result for the derivative of the function
        """
        return AutoDiffRev(np.tanh(self.val), parents=[(self,1 / (np.cosh(self.val) ** 2))])

    def __logistic__(self):
        """ Uses the standard logistic function with parameters k = 1, L = 1 on an AutoDiff object and returns result for function evaluated at specified number
        and result for the derivative of the function
        """
        return 1/(1+exp(-1*self))

    def __sqrt__(self):
        """ Takes the square root of an AutoDiff object and returns result for function evaluated at specified number
        and result for the derivative of the function
        """
        if self.val <0:
            raise ValueError
        return AutoDiffRev(np.sqrt(self.val), parents=[(self,0.5 / np.sqrt(self.val))])

    def backward(self, grad = 1.0):
        def _clear_grad(node):
            if node.parents is None: return
            for p,s in node.parents:
                p.grad =0
                _clear_grad(p)

        def _compute_grad_of_parents(node):
            if node.parents ==None:
                pass
            else:
                for parent,node2parent in node.parents:
                    # print(node.val,node.grad,node2parent)             
                    parent.grad += node.grad * node2parent
        _clear_grad(self)
        self.grad = np.ones(len(self.val))*grad
        # print(self.grad)
        for node in toposort(self):
            _compute_grad_of_parents(node)
    
    def clear_grad(self):
        def _clear_grad(node):
            if node.parents is None: return
            for p,s in node.parents:
                p.grad =np.zeros((len(p.val)))
                _clear_grad(p)
        self.grad = np.zeros((len(self.val)))
        _clear_grad(self)

    def get_grad(self,funcs):
        if isinstance(funcs,AutoDiffRev):
            funcs.backward()
            grad = self.grad
            funcs.clear_grad()
            return grad
        elif isinstance(funcs,list):
            try:
                all_grad = np.zeros((len(funcs),len(self.val)))
                for i in range(len(funcs)):
                    funcs[i].backward()
                    all_grad[i,:] = self.grad
                    funcs[i].clear_grad()
                return all_grad
            except AttributeError:
                raise Exception('you must input AutoDiffRev function or function list!')
            
def toposort(end_node):
    child_counts = {}
    stack = [end_node]
    while stack:
        node = stack.pop()
        if node in child_counts:
            child_counts[node] += 1
        else:
            child_counts[node] = 1
            if node.parents ==None:
                pass
            else:
                for p,s in node.parents:
                    stack.append(p)

    childless_nodes = [end_node]
    while childless_nodes:
        node = childless_nodes.pop()
        yield node
        if node.parents ==None:
            pass
        else:
            for parent,s in node.parents:
                if child_counts[parent] == 1:
                    childless_nodes.append(parent)
                else:
                    child_counts[parent] -= 1

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
        if x<0:
            raise ValueError("Square root not defined for negative values")  
        return np.sqrt(x)
    except ValueError:
        raise ValueError("Square root not defined for negative values")  


# if __name__ =='__main__':
    # print(np.array(2))
    # import doctest
    # doctest.testmod(verbose=True)
    # x = AutoDiffRev([1,1,1])
    # f = 2*sin(x)
    # f2 = x**3

    # print(x.get_grad([f,f2]))
    # f.backward()

    # print(x.grad)

    # f.backward()

    # print(x.grad)
    # x1 = AutoDiffRev(val=1.0)
    # x2 = AutoDiffRev(val=2.0)

    # a1 = x1*x2 #6
    # a2 = x1/x2 #1.5

    # b1 = a1/a2 #4
    # b2 = a1*a2 #9

    # y = b1-b2 #-5
    
    # # for i in toposort(y):
    # #     print(i)
    # # print(x1.grad, x2.grad,a1.grad,a2.grad,b1.grad,b2.grad)
    # y.backward()
    # # y2.backward(1)
    # # # -2.0 4.0
    # print(x1.grad, x2.grad)

    # y.backward()

    # -2.0 4.0
    # print(x1.grad, x2.grad)