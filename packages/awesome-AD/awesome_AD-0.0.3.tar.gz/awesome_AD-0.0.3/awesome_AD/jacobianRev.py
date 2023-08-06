import numpy as np
import sys,os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from awesome_AD.autoDiffRev import *

def JacobianRev(func_list,var_list):
    """ Get the Jacobian matrix from AutoDiffRev function lists and varible lists
    >>> x = AutoDiffRev(1)
    >>> y = AutoDiffRev(2)
    >>> J = JacobianRev([3 * x**3 + 2 * y**3, 2*x+4*y], [x, y])
    >>> J[0][0] == 9 and J[0][1] == 24 and J[1][0] == 2 and J[1][1] == 4
    True
    """
    if not all(isinstance(x, (AutoDiffRev)) for x in func_list):
        raise TypeError('the func_list input must be list of autoDiffRev object')

    if not all(isinstance(x, (AutoDiffRev)) for x in var_list):
        raise TypeError('the variable input must be list of autoDiffRev object')

    if len(var_list)>1 and len(var_list[0].val)>1:
        raise TypeError('We currently do not support multiple vector inputs in Jacobian!')
    elif len(var_list)>1:
        jacobian_matrix = np.zeros((len(func_list), len(var_list)))
        for i in range(len(var_list)):
            jacobian_matrix[:,i]=var_list[i].get_grad(func_list).flatten()
    else:
        jacobian_matrix =  var_list[0].get_grad(func_list) 
  
    return jacobian_matrix
