# CS 107 Final Project
# Reverse mode
import numpy as np


# Functionality:
# 1) Calculate derivatives of a scalar function of a scalar, overloading addition,
# subtraction, multiplication, divisoin, power, negation, exponential, and trig (sin, cos, tan)



class AutoDiffRev():
    """ Stores single variables as values and multiple variable inputs in arrays"""
    def __init__(self, val,grad = 0,parents=None):
        """AutoDiffRev object initialize      
        INPUTS
        =====
        val: float, value at which function is evaluated at
        grad: float, optional, d_output/d_self,default value is 0,will be updated in backward
        parents: self's parents and the corresponding d self/d parent.[(parent1,Δself/Δparent1),(parent2,Δself/Δparent2)]
        
        EXAMPLE
        =====
        >>> a = AutoDiffRev(1)
        >>> a.val[0]
        1
        """
        if isinstance(val, (np.ndarray, np.generic)):
            self.val = val
        elif isinstance(val, (list)):
            self.val = np.array(val)
        elif isinstance(val,(int, float)):
            self.val = np.array([val])
        self.grad = np.ones((len(self.val)))*grad
        self.parents = parents

    def __str__(self):   
        '''for printing
        To use:
        >>> print(AutoDiffRev(1))
        AutoDiff with val:[1]der:[0.]
        '''
        return 'AutoDiff with val:'+str(self.val)+'der:'+str(self.grad)
    
    def __len__(self):
        '''get val length
        To use:
        >>> print(len(AutoDiffRev(1)))
        1
        '''
        return len(self.val)

    def __add__(self, other):
        """ Adds AutoDiffRev objects and returns a AutoDiffRev object with specified value and parents.
        >>> a = AutoDiffRev(1) 
        >>> b = AutoDiffRev(2)
        >>> c = a+b
        >>> c.val[0]
        3
        >>> c.parents==[(a, 1.0), (b, 1.0)]
        True
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
        """ Makes addition commutative and returns a AutoDiffRev object with specified value and parents.
        >>> a = AutoDiffRev(1) 
        >>> b = AutoDiffRev(2)
        >>> c = a+b
        >>> c.val[0]
        3
        >>> c.parents==[(a, 1.0), (b, 1.0)]
        True
        """
        return self.__add__(other)

    def __mul__(self, other):
        """ Multiply AutoDiffRev objects and returns a AutoDiffRev object with specified value and parents.
        >>> a = AutoDiffRev(1) 
        >>> b = AutoDiffRev(2)
        >>> c = a*b
        >>> c.val[0]
        2
        >>> c.parents==[(a, 2), (b, 1)]
        True
        """
        try:
            z = AutoDiffRev(self.val*other.val)
            z.parents = [(self, other.val), (other, self.val)]
            return z
        except AttributeError:
            other = AutoDiffRev(other*np.ones(np.shape(self.val)))
            return self*other

    def __rmul__(self, other):
        """ Makes multiplication commutative and returns a AutoDiffRev object with specified value and parents.
        >>> a = AutoDiffRev(1) 
        >>> b = AutoDiffRev(2)
        >>> c = a*b
        >>> c.val[0]
        2
        >>> c.parents==[(a, 2), (b, 1)]
        True
        """
        return self.__mul__(other)
    
    def __sub__(self, other):
        """ Makes subtraction and returns a AutoDiffRev object with specified value and parents.
        >>> a = AutoDiffRev(1) 
        >>> b = AutoDiffRev(2)
        >>> c = a-b
        >>> c.val[0]
        -1
        >>> c.parents==[(a, 1), (b, -1)]
        True
        """
        try:
            z = AutoDiffRev(self.val - other.val)
            z.parents = [(self, 1.0), (other, -1.0)]
            return z
        except AttributeError:
            other = AutoDiffRev(other*np.ones(np.shape(self.val)))
            return self-other

    def __rsub__(self, other):
        """ Makes subtraction commutative and returns a AutoDiffRev object with specified value and parents.
        >>> a = AutoDiffRev(1) 
        >>> b = AutoDiffRev(2)
        >>> c = a-b
        >>> c.val[0]
        -1
        >>> c.parents==[(a, 1), (b, -1)]
        True
        """
        
        try:
            return AutoDiffRev(other.val - self.val,parents=[(self, -1.0), (other, 1.0)])
        except AttributeError:
            other = AutoDiffRev(other*np.ones(np.shape(self.val)))
            return other-self

    def __truediv__(self, other):
        ''' Self divide other returns a AutoDiffRev object with specified value and parents.
        >>> a = AutoDiffRev(1) 
        >>> b = AutoDiffRev(2)
        >>> c = a/b
        >>> c.val[0]
        0.5
        >>> c.parents==[(a, 1/2), (b, -1/4)]
        True
        '''
        try:
            z = AutoDiffRev(self.val/other.val)
            z.parents = [(self, 1/other.val), (other, -self.val/(other.val)**2)]
            return z
        except AttributeError:
            other = AutoDiffRev(other*np.ones(np.shape(self.val)))
            return self/other
    
    def __rtruediv__(self, other):
        ''' Other divide self and returns a AutoDiffRev object with specified value and parents.
        >>> a = AutoDiffRev(1) 
        >>> b = AutoDiffRev(2)
        >>> c = a/b
        >>> c.val[0]
        0.5
        >>> c.parents==[(a, 1/2), (b, -1/4)]
        True
        '''
        try:
            return  AutoDiffRev(other.val / self.val,parents=[(self,-1*other.val/(self.val**2)),(other,1/self.val)])
        except AttributeError:
            other = AutoDiffRev(other*np.ones(np.shape(self.val)))
            return other/self
    
    def __pow__(self, other):
        """ Raises an AutoDiffRev object to a power and returns a AutoDiffRev object with specified value and parents.
        >>> a = AutoDiffRev(1) 
        >>> b = AutoDiffRev(2)
        >>> c = a**b
        >>> c.val[0]
        1
        >>> c.parents==[(a, 2), (b, 0)]
        True
        """
        try:
            z = AutoDiffRev(self.val ** other.val)
            z.parents = [(self,other.val*self.val**(other.val-1)),(other,self.val**other.val*np.log(np.abs(self.val)))]
            return z
        except AttributeError:
            other = AutoDiffRev(other*np.ones(np.shape(self.val)))
            return self**other
    
    def __rpow__(self, other):
        """ Raises an  object to a AutoDiffRev power and returns a AutoDiffRev object with specified value and parents.
        >>> a = AutoDiffRev(1) 
        >>> b = AutoDiffRev(2)
        >>> c = a**b
        >>> c.val[0]
        1
        >>> c.parents==[(a, 2), (b, 0)]
        True
        """
        try:
            return AutoDiffRev(other.val ** self.val,parents=[(other,self.val*other.val**(self.val-1)),(self,other.val**self.val*np.log(np.abs(other.val)))])
        except AttributeError:
            other = AutoDiffRev(other*np.ones(np.shape(self.val)))
            return other**self

    def __neg__(self):
        """ Negates AutoDiffRev object and returns a AutoDiffRev object with specified value and parents.
        >>> a = AutoDiffRev(1) 
        >>> c = -a
        >>> c.val[0]
        -1
        >>> c.parents==[(a, -1)]
        True
        """
        return AutoDiffRev(- self.val,parents=[(self,-1)])

    def __exp__(self):
        """ Takes exponential of an AutoDiffRev object and returns a AutoDiffRev object with specified value and parents.
        >>> a = AutoDiffRev(1) 
        >>> c = exp(a)
        >>> c.val[0]
        2.718281828459045
        """
        return AutoDiffRev(np.exp(self.val),parents=[(self,np.exp(self.val))])

    def __sin__(self):
        """ Takes sine of an AutoDiff object and returns a AutoDiffRev object with specified value and parents.
        >>> a = AutoDiffRev(1) 
        >>> c = sin(a)
        >>> c.val[0]
        0.8414709848078965
        """
        # Derivative of sin(f(x)) is f'(x)*cos(f(x))
        z = AutoDiffRev(np.sin(self.val))
        z.parents = [(self,np.cos(self.val))]
        return z

    def __cos__(self):
        """ Takes cosine of an AutoDiff object and returns a AutoDiffRev object with specified value and parents.
        >>> c = cos(AutoDiffRev(2)**2)
        >>> abs(c.val[0]+0.6536436208636119)<1e-6 
        True
        >>> c.grad[0]==0
        True
        """
        # Derivative of cos(f(x)) is -f'(x)*sin(f(x))
        return AutoDiffRev(np.cos(self.val), parents=[(self,-np.sin(self.val))])

    def __tan__(self):
        """ Takes tangent of an AutoDiff object and returns a AutoDiffRev object with specified value and parents.
        >>> c = tan(AutoDiffRev(2)**2)
        >>> abs(c.val[0]-1.1578212823495775)<1e-6
        True
        >>> c.grad[0]==0
        True
        """
        return AutoDiffRev(np.tan(self.val), parents=[(self,(1/np.cos(self.val))**2)])

    def __lt__(self, other):
        """ Comparison between self and other: less than
        the default gradient is zero
        >>> (AutoDiffRev(2)<AutoDiffRev(3))[0]
        False
        """        
        try:
            return np.less(self.val, other.val) and np.less(self.grad, other.grad)
        except AttributeError:
            return np.less(self.val, other)

    def __gt__(self, other):
        """ Comparison between self and other: great than
        the default gradient is zero
        >>> (AutoDiffRev(2)>AutoDiffRev(3))[0]
        False
        """    
        try:
            return np.greater(self.val, other.val) and np.greater(self.grad, other.grad)
        except AttributeError:
            return np.greater(self.val, other)

    def __le__(self, other):
        """ Comparison between self and other: less or equal
        the default gradient is zero
        >>> (AutoDiffRev(2)<=AutoDiffRev(3))[0]
        True
        """    
        try:
            return np.less_equal(self.val, other.val) and np.less_equal(self.grad, other.grad)
        except AttributeError:
            return np.less_equal(self.val, other)

    def __ge__(self, other):
        """ Comparison between self and other: great or equal
        the default gradient is zero
        >>> (AutoDiffRev(2)>=AutoDiffRev(3))[0]
        False
        """    
        try:
            return np.greater_equal(self.val, other.val) and np.greater_equal(self.grad, other.grad)
        except AttributeError:
            return np.greater_equal(self.val, other)

    def __eq__(self, other):
        """ Comparison between self and other: equal
        the default gradient is zero
        >>> (AutoDiffRev(2)==AutoDiffRev(2))
        True
        """    
        try:
            return np.array_equal(self.val, other.val) and np.array_equal(self.grad, other.grad)
        except AttributeError:
            return np.array_equal(self.val, other)
    
    def __hash__(self):
        """ Return the id, useful in dictionary whose key is AutoDiffRev object
        """
        return id(self)

    def __ne__(self, other):
        """ Comparison between self and other: not equal 
        the default gradient is zero
        >>> (AutoDiffRev(2)!=AutoDiffRev(3))
        True
        """    
        try:
            return not np.array_equal(self.val, other.val) or not np.array_equal(self.grad, other.grad)
        except AttributeError:
            return not np.array_equal(self.val, other)

    def __arcsin__(self):
        """ Takes inverse sine of an AutoDiffRev object and returns a AutoDiffRev object with specified value and parents.
        >>> func= arcsin(AutoDiffRev(0.5))
        >>> abs(func.val[0] - 0.5235987755982988) < 1e-6
        True
        """
        return AutoDiffRev(np.arcsin(self.val), parents=[(self,1/ np.sqrt(1 - self.val ** 2))])

    def __arccos__(self):
        """ Takes inverse cosine of an AutoDiffRev object and returns a AutoDiffRev object with specified value and parents.
        >>> func= arccos(AutoDiffRev(0.5))
        >>> abs(func.val[0] - 1.0471975511965976) < 1e-6
        True
        """
        return AutoDiffRev(np.arccos(self.val), parents=[(self,-1/ np.sqrt(1 - self.val ** 2))])    

    def __arctan__(self):
        """ Takes inverse tangent of an AutoDiffRev object and returns a AutoDiffRev object with specified value and parents.
        >>> func= arctan(AutoDiffRev(0.5))
        >>> abs(func.val[0] - 0.46364760900080615) < 1e-6
        True
        """
        return AutoDiffRev(np.arctan(self.val), parents=[(self,1 / (1 + self.val ** 2))])

    def __sqrt__(self):
        """ Takes the square root of an AutoDiffRev object and returns a AutoDiffRev object with specified value and parents.
        >>> func= sqrt(AutoDiffRev(6))
        >>> abs(func.val[0] - 2.449489742783178) < 1e-6
        True
        """
        if self.val <0:
            raise ValueError
        return AutoDiffRev(np.sqrt(self.val), parents=[(self,0.5 / np.sqrt(self.val))])

    def backward(self, grad = 1.0):
        '''Backward the node gradient
        >>> x = AutoDiffRev(1)
        >>> f = 2*sin(x)
        >>> f.backward()
        >>> (x.grad[0]- 1.08060461)<1e-6
        True
        '''
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
        ''' Clear the node and its' previous nodes' gradient, do this after backward
        >>> x = AutoDiffRev(1)
        >>> f = 2*sin(x)
        >>> f.backward()
        >>> f.clear_grad()
        >>> (x.grad==0 and f.grad==0)[0]
        True
        '''
        def _clear_grad(node):
            if node.parents is None: return
            for p,s in node.parents:
                p.grad =np.zeros((len(p.val)))
                _clear_grad(p)
        self.grad = np.zeros((len(self.val)))
        _clear_grad(self)

    def get_grad(self,funcs):
        ''' Get d_func/d_self
        >>> x = AutoDiffRev(1)
        >>> f = 2*sin(x)
        >>> (abs(x.get_grad(f)- 1.08060461)<1e-6)[0]
        True
        '''
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
    ''' ref: https://tomroth.com.au/backprop-toposort/
    Yield nodes in the opposite order that we topologically sort them.
    >>> x = AutoDiffRev(1)
    >>> f = 2*sin(x)
    >>> list(toposort(f))[0]==f
    True
    '''
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
    """ 
    If it is AutoDiffRev object, then
    takes the expontenial of an AutoDiffRev object and returns a AutoDiffRev object with specified value and parents.
    else just use numerical methods   
    >>> a = AutoDiffRev(1) 
    >>> c = exp(a)
    >>> c.val[0]
    2.718281828459045
    """
    try:
        return x.__exp__()
    except AttributeError:
        return np.exp(x)
    
def sin(x):
    """ 
    If it is AutoDiffRev object, then
    takes the sine of an AutoDiffRev object and returns a AutoDiffRev object with specified value and parents.
    else just use numerical methods   
    >>> a = AutoDiffRev(1) 
    >>> c = sin(a)
    >>> c.val[0]
    0.8414709848078965
    """
    try:
        return x.__sin__()
    except AttributeError:
        return np.sin(x)

def cos(x):
    """ 
    If it is AutoDiffRev object, then
    takes the cosine of an AutoDiffRev object and returns a AutoDiffRev object with specified value and parents.
    else just use numerical methods   
    >>> c = cos(AutoDiffRev(2)**2)
    >>> abs(c.val[0]+0.6536436208636119)<1e-6 
    True
    >>> c.grad[0]==0
    True
    """
    try:
        return x.__cos__()
    except AttributeError:
        return np.cos(x)

def tan(x):
    """ 
    If it is AutoDiffRev object, then
    takes the tangent of an AutoDiffRev object and returns a AutoDiffRev object with specified value and parents.
    else just use numerical methods   
    >>> c = tan(AutoDiffRev(2)**2)
    >>> abs(c.val[0]-1.1578212823495775)<1e-6
    True
    >>> c.grad[0]==0
    True
    """
    try:
        return x.__tan__()
    except AttributeError:
        return np.tan(x)

def arcsin(x):
    """ 
    If it is AutoDiffRev object, then
    takes the arcsin of an AutoDiffRev object and returns a AutoDiffRev object with specified value and parents.
    else just use numerical methods     
    >>> func= arcsin(AutoDiffRev(0.5))
    >>> abs(func.val[0] - 0.5235987755982988) < 1e-6
    True
    """
    try:
        return x.__arcsin__()
    except AttributeError:
        return np.arcsin(x)

def arccos(x):
    """ 
    If it is AutoDiffRev object, then
    takes the arccos of an AutoDiffRev object and returns a AutoDiffRev object with specified value and parents.
    else just use numerical methods   
    >>> func= arccos(AutoDiffRev(0.5))
    >>> abs(func.val[0] - 1.0471975511965976) < 1e-6
    True
    """
    try:
        return x.__arccos__()
    except AttributeError:
        return np.arccos(x)

def arctan(x):
    """ 
    If it is AutoDiffRev object, then
    takes the arctan of an AutoDiffRev object and returns a AutoDiffRev object with specified value and parents.
    else just use numerical methods
    >>> func= arctan(AutoDiffRev(0.5))
    >>> abs(func.val[0] - 0.46364760900080615) < 1e-6
    True
    """
    try:
        return x.__arctan__()
    except AttributeError:
        return np.arctan(x)

def sinh(x):
    """ 
    If it is AutoDiffRev object, then
    takes the sinh of an AutoDiffRev object and returns a AutoDiffRev object with specified value and parents.
    else just use numerical methods
    >>> func= sinh(AutoDiffRev(0))
    >>> abs(func.val[0] - 0) < 1e-6
    True
    """
    try:
        return (x.__exp__() - (-x).__exp__()) / 2
    except AttributeError:
        return np.sinh(x)

def cosh(x):
    """ 
    If it is AutoDiffRev object, then
    takes the cosh of an AutoDiffRev object and returns a AutoDiffRev object with specified value and parents.
    else just use numerical methods
    >>> func= cosh(AutoDiffRev(0))
    >>> abs(func.val[0] - 1) < 1e-6
    True
    """
    try:
        return (x.__exp__() + (-x).__exp__()) / 2
    except AttributeError:
        return np.cosh(x)

def tanh(x):
    """ 
    If it is AutoDiffRev object, then
    takes the tanh of an AutoDiffRev object and returns a AutoDiffRev object with specified value and parents.
    else just use numerical methods
    >>> func= tanh(AutoDiffRev(0))
    >>> abs(func.val[0] - 0) < 1e-6
    True
    """
    try:
        return (x.__exp__() - (-x).__exp__()) / (x.__exp__() + (-x).__exp__())
    except AttributeError:
        return np.tanh(x)

def logistic(x):
    """ 
    If it is AutoDiffRev object, then
    takes the logistic of an AutoDiffRev object and returns a AutoDiffRev object with specified value and parents.
    else just use numerical methods
    >>> func= logistic(AutoDiffRev(0))
    >>> abs(func.val[0] - 0.5) < 1e-6
    True
    """
    try:
        return 1 / (1 + (-x).__exp__())
    except AttributeError:
        return 1 / (1 + np.exp(-x))

def sqrt(x):
    """ 
    If it is AutoDiffRev object, then
    takes the square root of an AutoDiffRev object and returns a AutoDiffRev object with specified value and parents.
    else just use numerical methods
    >>> func= sqrt(AutoDiffRev(6))
    >>> abs(func.val[0] - 2.449489742783178) < 1e-6
    True
    """
    try:
        return x.__sqrt__()
    except AttributeError:
        if x<0:
            raise ValueError("Square root not defined for negative values")  
        return np.sqrt(x)
    except ValueError:
        raise ValueError("Square root not defined for negative values")  

def log(x,base=np.exp(1)):
    """ 
    If it is AutoDiffRev object, then
    takes the log of an AutoDiffRev object and returns a AutoDiffRev object with specified value and parents.
    else just use numerical methods
    >>> func= log(2,2)
    >>> abs(func - 1) < 1e-6
    True
    """
    if base ==1 or base<0:
        raise ValueError('log base cannot <0 or ==1')
    try:
        return AutoDiffRev(np.log(x.val)/np.log(base),parents=[(x,1/(x.val*np.log(base)))])
    except:
        return np.log(x)/np.log(base)

