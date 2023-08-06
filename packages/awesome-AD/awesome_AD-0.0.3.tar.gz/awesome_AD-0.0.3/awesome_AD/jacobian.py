import numpy as np
import sys,os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from awesome_AD.autoDiff import AutoDiff,exp,sin,cos,tan

def Jacobian(func_list,var_list):
    """ Get the Jacobian matrix from AutoDiff function lists and varible lists
    >>> x = AutoDiff(1, der = 1,var_num=2,idx=0)
    >>> y = AutoDiff(2, der = 1,var_num=2,idx=1)
    >>> J = Jacobian([3 * x**3 + 2 * y**3, 2*x+4*y], [x, y])
    >>> J[0][0] == 9 and J[0][1] == 24 and J[1][0] == 2 and J[1][1] == 4
    True
    """
    if all(isinstance(x, (int,float)) for x in var_list):
        autodiff_list =[]
        var_num = len(var_list)
        for i in range(var_num):
            autodiff_list.append(AutoDiff(var_list[i],der=1,var_num=var_num,idx=i))

    elif all(isinstance(x, (AutoDiff)) for x in var_list):
        if len(var_list)>1 and len(var_list[0].val)>1:
            raise TypeError('We currently do not support multiple vector inputs in Jacobian!')
        else:
            autodiff_list = var_list
            var_num = max(len(var_list[0].val),len(var_list))
    else:
        raise TypeError('We only supports var_list = list of AutoDiff or int number or float number')

    jacobian_matrix = np.zeros((len(func_list), var_num))
    for i in range(len(func_list)):
        if isinstance (func_list[i],AutoDiff):
            jacobian_matrix[i,:]= func_list[i].der.flatten()
        elif callable(func_list[i]):
            jacobian_matrix[i,:]= func_list[i](*autodiff_list).der.flatten()
    return jacobian_matrix

'''
# demo 1: scalar input, one function
def f(x):
    return x**2
x = AutoDiff(3)
print(Jacobian([f],[x]))

f = x**2
print(Jacobian([f],[x]))

# demo 2: multiple scalar inputs, vector function
x = AutoDiff(2, var_num = 2, idx = 0)
y = AutoDiff(3, var_num = 2, idx = 1)
# f = 3 * x**3 + 2 * y**3
def f1(x,y):
    return 3 * x**3 + 2 * y**3
def f2(x,y):
    return 2*x+4*y

print(Jacobian([f1,f2],[x,y]))

# demo 3: vector numerical input, vector function, we will turn the variables to AutoDiff automatically
print(Jacobian([f1,f2],[2,3]))

# demo 4: vector AutoDiff input, vector function
def f3(x):
    return x**3
def f4(x):
    return x**2

x = AutoDiff([2,3])
print(Jacobian([f3,f4],[x]))
'''
